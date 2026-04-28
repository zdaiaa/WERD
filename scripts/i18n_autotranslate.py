#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
I18N_DIR = ROOT / "i18n"
LOCALES_PATH = I18N_DIR / "locales.json"
SOURCE_EN = "en-US"
SOURCE_ZH = "zh-Hans"
ZH_HANT = "zh-Hant"
MODEL = os.getenv("OPENAI_I18N_MODEL", "gpt-5-mini")
OPENAI_TIMEOUT_SECONDS = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "90"))

GLOSSARY = {
    "WealthX": "WealthX",
    "WERD": "WERD",
    "Flow": "Flow",
    "Flows": "Flows",
    "iCloud": "iCloud",
    "iOS": "iOS",
    "App Store": "App Store",
    "Cashflow Map": "Cashflow Map",
}

FORCE_COPY_KEYS = {
    "app_version",
    "app_store_url",
    "canonical_url",
    "privacy_contact_email",
    "privacy_date",
    "site_url",
    "support_url",
    "terms_url",
}


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def split_meta(data: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, Any]]:
    meta = data.get("_meta", {})
    core: Dict[str, str] = {}
    for key, value in data.items():
        if key == "_meta":
            continue
        if isinstance(value, str):
            core[key] = value
    return core, meta if isinstance(meta, dict) else {}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_hashes(meta: Dict[str, Any]) -> Dict[str, str]:
    raw = meta.get("source_hashes")
    if not isinstance(raw, dict):
        return {}
    return {str(key): str(value) for key, value in raw.items()}


def chunks(items: Dict[str, str], size: int = 60) -> Iterable[Dict[str, str]]:
    batch: Dict[str, str] = {}
    for key, value in items.items():
        batch[key] = value
        if len(batch) >= size:
            yield batch
            batch = {}
    if batch:
        yield batch


def apply_glossary(text: str) -> str:
    for source, target in GLOSSARY.items():
        text = text.replace(source, target)
    return text


def openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required when translations are needed")
    from openai import OpenAI

    return OpenAI(api_key=api_key, timeout=OPENAI_TIMEOUT_SECONDS, max_retries=2)


def call_openai_translate(client: Any, src_lang: str, dst_lang: str, items: Dict[str, str]) -> Dict[str, str]:
    system = (
        "You are a senior product localization editor for a concise Apple-style product website. "
        "Translate values naturally for the target locale. Keep keys unchanged. "
        "Keep brand names, URLs, email addresses, version numbers, and glossary terms unchanged. "
        "Return only one valid JSON object with the same keys."
    )
    payload = {
        "task": "translate_i18n_values",
        "source_language": src_lang,
        "target_language": dst_lang,
        "glossary": GLOSSARY,
        "items": items,
        "rules": [
            "Do not add claims that are not present in the source.",
            "Do not translate URLs, email addresses, version numbers, WealthX, WERD, iCloud, iOS, App Store, Flow, or Flows.",
            "Use a calm product-marketing tone, not literal machine translation.",
            "Keep privacy wording conservative and do not imply zero risk.",
        ],
    }
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )
    content = response.choices[0].message.content or "{}"
    translated = json.loads(content)

    missing = set(items) - set(translated)
    if missing:
        raise RuntimeError(f"{dst_lang}: translation response missing keys: {sorted(missing)[:8]}")

    return {key: apply_glossary(str(translated[key])) for key in items}


def translate_batch(src_lang: str, dst_lang: str, items: Dict[str, str]) -> Dict[str, str]:
    if not items:
        return {}

    client = openai_client()
    output: Dict[str, str] = {}
    for batch in chunks(items):
        last_error: Optional[Exception] = None
        for attempt in range(3):
            try:
                output.update(call_openai_translate(client, src_lang, dst_lang, batch))
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                delay = 1.6 ** attempt
                print(f"[warn] {dst_lang}: retry {attempt + 1}/3 after {exc}; sleep {delay:.1f}s")
                time.sleep(delay)
        if last_error is not None:
            raise RuntimeError(f"{dst_lang}: translation failed: {last_error}") from last_error
    return output


def source_for_locale(code: str, configured_source: str) -> str:
    if code == ZH_HANT:
        return SOURCE_ZH
    if configured_source in {SOURCE_EN, SOURCE_ZH}:
        return configured_source
    return SOURCE_EN


def build_target(src_lang: str, dst_lang: str, src_full: Dict[str, Any], dst_full: Dict[str, Any]) -> Tuple[Dict[str, Any], bool, Dict[str, int]]:
    src_core, _ = split_meta(src_full)
    dst_core, dst_meta = split_meta(dst_full)
    hashes = source_hashes(dst_meta)
    pending = dst_meta.get("pending_translation") is True

    next_full: Dict[str, Any] = dict(dst_full)
    for key in list(next_full.keys()):
        if key != "_meta" and key not in src_core:
            next_full.pop(key, None)
    next_full.setdefault("_meta", {})
    if not isinstance(next_full["_meta"], dict):
        next_full["_meta"] = {}

    needs_translate: Dict[str, str] = {}
    seed_hashes: Dict[str, str] = {}
    force_updates = 0

    for key, source_value in src_core.items():
        source_hash = sha(source_value)
        if key in FORCE_COPY_KEYS:
            if next_full.get(key) != source_value:
                force_updates += 1
            next_full[key] = source_value
            seed_hashes[key] = source_hash
            continue

        current_value = dst_core.get(key)
        if pending or current_value is None or not str(current_value).strip():
            needs_translate[key] = source_value
            continue
        if hashes.get(key) is None:
            seed_hashes[key] = source_hash
            continue
        if hashes.get(key) != source_hash:
            needs_translate[key] = source_value

    translated = translate_batch(src_lang, dst_lang, needs_translate)
    for key, value in translated.items():
        next_full[key] = value
        seed_hashes[key] = sha(src_core[key])

    for key, source_hash in seed_hashes.items():
        next_full["_meta"].setdefault("source_hashes", {})
        next_full["_meta"]["source_hashes"][key] = source_hash

    next_full["_meta"].update(
        {
            "generated_by": "scripts/i18n_autotranslate.py",
            "locale": dst_lang,
            "source_lang": src_lang,
            "target_lang": dst_lang,
            "pending_translation": False,
            "updated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    )

    changed = json.dumps(next_full, ensure_ascii=False, sort_keys=True) != json.dumps(
        dst_full, ensure_ascii=False, sort_keys=True
    )
    stats = {
        "translated": len(needs_translate),
        "seeded": len(seed_hashes) - len(needs_translate),
        "force": force_updates,
    }
    return next_full, changed, stats


def validate_locale_config(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    locales = config.get("locales")
    if not isinstance(locales, list):
        raise RuntimeError("i18n/locales.json must contain a locales array")
    out: List[Dict[str, Any]] = []
    seen = set()
    for item in locales:
        if not isinstance(item, dict) or not isinstance(item.get("code"), str):
            raise RuntimeError("Each locale entry must contain a string code")
        code = item["code"]
        if code in seen:
            raise RuntimeError(f"Duplicate locale code: {code}")
        seen.add(code)
        out.append(item)
    required = {SOURCE_EN, SOURCE_ZH, ZH_HANT}
    missing = required - seen
    if missing:
        raise RuntimeError(f"Missing required locale files in locales.json: {sorted(missing)}")
    return out


def validate_output_files(locale_entries: List[Dict[str, Any]]) -> None:
    for entry in locale_entries:
        code = entry["code"]
        path = I18N_DIR / f"{code}.json"
        data = load_json(path)
        src_lang = source_for_locale(code, str(entry.get("source", SOURCE_EN)))
        if code in {SOURCE_EN, SOURCE_ZH}:
            continue
        source = load_json(I18N_DIR / f"{src_lang}.json")
        src_core, _ = split_meta(source)
        dst_core, _ = split_meta(data)
        missing = sorted(set(src_core) - set(dst_core))
        if missing:
            raise RuntimeError(f"{path.name} is missing keys: {missing[:10]}")


def main() -> None:
    config = load_json(LOCALES_PATH)
    locale_entries = validate_locale_config(config)

    source_files = {
        SOURCE_EN: load_json(I18N_DIR / f"{SOURCE_EN}.json"),
        SOURCE_ZH: load_json(I18N_DIR / f"{SOURCE_ZH}.json"),
    }
    if not source_files[SOURCE_EN] or not source_files[SOURCE_ZH]:
        raise RuntimeError("Missing source locale files: en-US.json and zh-Hans.json are required")

    pending_writes: List[Tuple[Path, Dict[str, Any], Dict[str, int]]] = []
    for entry in locale_entries:
        code = entry["code"]
        if code in {SOURCE_EN, SOURCE_ZH}:
            continue
        src_lang = source_for_locale(code, str(entry.get("source", SOURCE_EN)))
        dst_path = I18N_DIR / f"{code}.json"
        next_data, changed, stats = build_target(src_lang, code, source_files[src_lang], load_json(dst_path))
        if changed:
            pending_writes.append((dst_path, next_data, stats))
            print(f"[plan] {dst_path.name}: {stats}")
        else:
            print(f"[skip] {dst_path.name}: no changes")

    for path, data, _ in pending_writes:
        save_json(path, data)
        print(f"[write] {path.name}")

    validate_output_files(locale_entries)


if __name__ == "__main__":
    main()

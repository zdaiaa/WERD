#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional

from openai import OpenAI

# ----------------------------
# Paths
# ----------------------------
ROOT = Path(__file__).resolve().parents[1]
I18N_DIR = ROOT / "i18n"

SOURCE_ZH = I18N_DIR / "zh.json"
SOURCE_EN = I18N_DIR / "en.json"

# ----------------------------
# Strategy
# ----------------------------
# 双轨策略：
# - zh.json 仅用于生成 zh-Hant.json
# - en.json 用于生成除 zh/en/zh-Hant 之外的所有语言文件
ZH_TRACK_TARGET = "zh-Hant"

# 永远不翻译 / 固定写法（按需扩展）
GLOSSARY = {
    "WealthX": "WealthX",
    "Flow": "Flow",
    "Flows": "Flows",
    "iCloud": "iCloud",
    "SF Symbols": "SF Symbols",
}

MODEL = os.getenv("OPENAI_I18N_MODEL", "gpt-5-mini")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# Non-Translatable / Force-Copy Rules (方案B增强)
# ----------------------------
# 这些 key 的值应当在所有语言中保持一致（永远从 en.json 强制覆盖）
# 这些 key 的值应当在所有语言中保持一致（永远从 en.json 强制覆盖）
FORCE_COPY_KEYS_FROM_EN = {
    "privacy_date",
    # 你还可以继续加：版本号、价格、URL等
}

def is_lang_label_key(k: str) -> bool:
    return k.startswith("lang_")

def is_force_copy_item(k: str, v: Any) -> bool:
    # 语言名称：永远固定（来自 en）
    if is_lang_label_key(k):
        return True
    # 手动列入：永远固定（来自 en）
    if k in FORCE_COPY_KEYS_FROM_EN:
        return True
    # ✅ 自动识别：任何 ISO 日期值都固定（来自 en）
    if is_iso_date_value(v):
        return True
    return False

def is_iso_date_value(v: Any) -> bool:
    """
    识别 YYYY-MM-DD（严格 10 位），用于类似 privacy_date / release_date 等全局日期字段
    """
    if not isinstance(v, str):
        return False
    s = v.strip()
    if len(s) != 10:
        return False
    if s[4] != "-" or s[7] != "-":
        return False
    y, m, d = s[:4], s[5:7], s[8:10]
    if not (y.isdigit() and m.isdigit() and d.isdigit()):
        return False
    mm = int(m)
    dd = int(d)
    return 1 <= mm <= 12 and 1 <= dd <= 31

# ----------------------------
# Helpers
# ----------------------------
def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: Dict[str, Any]) -> None:
    # 保持稳定输出（减少 diff 噪音）
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def apply_glossary(text: str) -> str:
    for k, v in GLOSSARY.items():
        text = text.replace(k, v)
    return text

def split_meta(d: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, Any]]:
    """把可翻译的 key/value（str）与 _meta 分离"""
    meta = d.get("_meta", {})
    core: Dict[str, str] = {}
    for k, v in d.items():
        if k == "_meta":
            continue
        if isinstance(v, str):
            core[k] = v
    return core, meta if isinstance(meta, dict) else {}

def get_source_hashes(dst_meta: Dict[str, Any]) -> Dict[str, str]:
    hashes = dst_meta.get("source_hashes")
    if not isinstance(hashes, dict):
        return {}
    out: Dict[str, str] = {}
    for k, v in hashes.items():
        if isinstance(k, str) and isinstance(v, str):
            out[k] = v
    return out

def sync_deletions(src: Dict[str, str], dst_full: Dict[str, Any]) -> bool:
    """
    规则：源里删了 key，目标也删（保留 _meta）
    同时清理 _meta.source_hashes 中已删 key 的 hash
    返回：是否发生了任何删除/清理（用于决定是否需要 save）
    """
    changed = False

    meta = dst_full.get("_meta")
    hashes: Dict[str, str] = {}
    if isinstance(meta, dict):
        hashes = get_source_hashes(meta)

    for k in list(dst_full.keys()):
        if k == "_meta":
            continue
        if k not in src:
            dst_full.pop(k, None)
            if k in hashes:
                hashes.pop(k, None)
            changed = True

    if isinstance(meta, dict):
        if meta.get("source_hashes") != hashes:
            meta["source_hashes"] = hashes
            dst_full["_meta"] = meta
            changed = True

    return changed

def build_plan(
    src: Dict[str, str],
    dst: Dict[str, str],
    dst_meta: Dict[str, Any],
) -> Tuple[Dict[str, str], List[str]]:
    """
    返回 (needs_translate, needs_hash_seed)

    翻译规则：
    - dst 缺 key：翻译
    - dst[key] 为空：翻译
    - 如果 old_hash 存在 且 与 src_hash 不同：重翻
    - 如果 old_hash 不存在 但 dst 已有翻译：不翻译，只补 hash（防止首次接入全量重翻）
    """
    dst_hashes = get_source_hashes(dst_meta)

    needs_translate: Dict[str, str] = {}
    needs_hash_seed: List[str] = []

    for k, v in src.items():
        src_hash = sha(v)
        old_hash = dst_hashes.get(k)

        if k not in dst:
            needs_translate[k] = v
            continue

        cur = dst.get(k)
        if not isinstance(cur, str) or cur.strip() == "":
            needs_translate[k] = v
            continue

        if old_hash is None:
            needs_hash_seed.append(k)
            continue

        if old_hash != src_hash:
            needs_translate[k] = v

    return needs_translate, needs_hash_seed

def _call_openai_translate(src_lang: str, dst_lang: str, items: Dict[str, str]) -> Dict[str, str]:
    system = (
        "You are a professional product localization expert for an Apple-style product website. "
        "Translate naturally for the target locale: concise, clear, idiomatic, not literal. "
        "Keep brand names and glossary terms unchanged. Keep URLs/emails/phone numbers unchanged. "
        "Return ONLY a valid JSON object mapping the same keys to translated strings."
    )

    user_payload = {
        "task": "translate_i18n",
        "source_language": src_lang,
        "target_language": dst_lang,
        "glossary": GLOSSARY,
        "items": items,
        "extra_rules": [
            "Keep keys unchanged; translate only values.",
            "Apple-like tone: minimal, confident, not exaggerated.",
            "Preserve punctuation style for the locale.",
            "Keep email/URLs/phone numbers unchanged.",
            "Do not translate product/brand names such as WealthX and glossary terms.",
        ],
        "output": "JSON object only",
    }

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
        # ⚠️ gpt-5-mini 这类模型可能不支持 temperature=0.2（你之前已经踩坑）
        # 所以这里不显式设置 temperature，保持默认
    )

    text = resp.choices[0].message.content.strip()
    data = json.loads(text)

    out: Dict[str, str] = {}
    for k, v in data.items():
        out[str(k)] = apply_glossary(str(v))
    return out

def translate_batch(src_lang: str, dst_lang: str, items: Dict[str, str]) -> Dict[str, str]:
    """
    批量翻译：输入 JSON，输出必须是 JSON（key 不翻译，value 翻译）
    带简单重试（应对临时网络/429）
    """
    if not items:
        return {}

    max_retries = 3
    backoff = 1.5
    last_err: Optional[Exception] = None

    for i in range(max_retries):
        try:
            return _call_openai_translate(src_lang, dst_lang, items)
        except Exception as e:
            last_err = e
            sleep_s = backoff ** i
            print(f"[warn] translate retry {i+1}/{max_retries} for {dst_lang}: {e}. sleep {sleep_s:.1f}s")
            time.sleep(sleep_s)

    raise RuntimeError(f"translate failed for {dst_lang}: {last_err}")

def upsert_meta_hashes(dst_full: Dict[str, Any], updates: Dict[str, str], src_lang: str, dst_lang: str) -> None:
    """
    把 source_hashes 写入 _meta（updates: key -> source_text）
    """
    meta = dst_full.get("_meta")
    if not isinstance(meta, dict):
        meta = {}

    meta.setdefault("source_hashes", {})
    if not isinstance(meta["source_hashes"], dict):
        meta["source_hashes"] = {}

    for k, src_text in updates.items():
        meta["source_hashes"][k] = sha(src_text)

    meta["generated_by"] = "i18n_autotranslate.py"
    meta["source_lang"] = src_lang
    meta["target_lang"] = dst_lang
    meta["updated_at_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    dst_full["_meta"] = meta

def apply_force_copy(authoritative_en_core: Dict[str, str], dst_full: Dict[str, Any]) -> bool:
    """
    强制字段永远从 en.json 覆盖到目标语言：
    - lang_*
    - FORCE_COPY_KEYS_FROM_EN
    - ✅ 任意 ISO 日期值（YYYY-MM-DD）
    返回：是否发生变化
    """
    changed = False
    for k, v in authoritative_en_core.items():
        if not is_force_copy_item(k, v):
            continue
        if dst_full.get(k) != v:
            dst_full[k] = v
            changed = True
    return changed

def process_target_file(
    *,
    src_lang: str,
    dst_lang: str,
    src_path: Path,
    dst_path: Path,
    authoritative_en_core: Dict[str, str],
) -> None:
    """
    关键增强（方案B）：
    - 在翻译前强制同步 privacy_date & lang_*（来自 en.json）
    - 强制字段不参与 build_plan/translate_batch（避免被翻译覆盖）
    - 强制字段也写入 source_hashes，确保 en.json 更新能触发全量同步
    - 删除同步后重新 split
    - 即使只发生 deletions / hash seed / force copy，也要 save_json
    """
    src_full = load_json(src_path)
    src_core, _ = split_meta(src_full)

    dst_full = load_json(dst_path)

    # 0) ✅ 强制 copy（从 en）
    force_changed = apply_force_copy(authoritative_en_core, dst_full)

    # 1) ✅ 同步删除（基于该目标语言的源轨：en 轨或 zh 轨）
    deleted_changed = sync_deletions(src_core, dst_full)

    # 2) ✅ 删除后重新 split
    dst_core, dst_meta = split_meta(dst_full)

    # 3) ✅ 排除强制字段，不参与翻译计划（但仍保留在文件里）
    src_for_translate = {k: v for k, v in src_core.items() if not is_force_copy_item(k, authoritative_en_core.get(k, v))}
    dst_for_plan = {k: v for k, v in dst_core.items() if not is_force_copy_item(k, authoritative_en_core.get(k, v))}

    needs_translate, needs_hash_seed = build_plan(src_for_translate, dst_for_plan, dst_meta)

    # 4) 如需翻译则翻译并写回
    translated_any = False
    if needs_translate:
        translated = translate_batch(src_lang, dst_lang, needs_translate)
        for k, v in translated.items():
            dst_full[k] = v
        translated_any = True

    # 5) meta hash 更新：seed + translated + force-copy keys 都要写
    seed_updates: Dict[str, str] = {}

    for k in needs_hash_seed:
        seed_updates[k] = src_for_translate[k]

    for k, v in needs_translate.items():
        seed_updates[k] = v

    # ✅ 强制字段的 hash 以 en 为准（注意：这里会覆盖旧 hash）
    for k, v in authoritative_en_core.items():
        if is_force_copy_item(k, v):
            seed_updates[k] = v

    meta_changed = False
    if seed_updates:
        before = json.dumps(dst_full.get("_meta", {}), ensure_ascii=False, sort_keys=True)
        upsert_meta_hashes(dst_full, seed_updates, src_lang, dst_lang)
        after = json.dumps(dst_full.get("_meta", {}), ensure_ascii=False, sort_keys=True)
        meta_changed = (before != after)

    if force_changed or deleted_changed or translated_any or meta_changed:
        save_json(dst_path, dst_full)
        print(
            f"[write] {dst_path.name}: "
            f"force={force_changed} "
            f"translated={len(needs_translate)} "
            f"seed={len(needs_hash_seed)} "
            f"deleted={deleted_changed}"
        )
    else:
        print(f"[skip] {dst_path.name}: no changes")

def list_target_langs_from_folder() -> List[str]:
    """
    使用 i18n 目录现有文件名作为目标语言集合：
    - 你新增一个 i18n/xx.json，就会自动被纳入管理
    """
    langs: List[str] = []
    if not I18N_DIR.exists():
        return langs
    for p in I18N_DIR.glob("*.json"):
        langs.append(p.stem)  # fr.json -> "fr"
    return sorted(set(langs))

def main() -> None:
    if not SOURCE_EN.exists():
        raise FileNotFoundError(f"Missing {SOURCE_EN}")
    if not SOURCE_ZH.exists():
        raise FileNotFoundError(f"Missing {SOURCE_ZH}")

    # ✅ 读取 en 作为“全局权威源”，用于强制同步字段
    en_full = load_json(SOURCE_EN)
    authoritative_en_core, _ = split_meta(en_full)

    # A) zh -> zh-Hant（同时也会强制同步 en 的 privacy_date/lang_*）
    process_target_file(
        src_lang="zh",
        dst_lang=ZH_TRACK_TARGET,
        src_path=SOURCE_ZH,
        dst_path=I18N_DIR / f"{ZH_TRACK_TARGET}.json",
        authoritative_en_core=authoritative_en_core,
    )

    # B) en -> other langs
    targets = list_target_langs_from_folder()
    skip = {"zh", "en", ZH_TRACK_TARGET}
    for lang in targets:
        if lang in skip:
            continue
        process_target_file(
            src_lang="en",
            dst_lang=lang,
            src_path=SOURCE_EN,
            dst_path=I18N_DIR / f"{lang}.json",
            authoritative_en_core=authoritative_en_core,
        )

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
I18N_DIR = ROOT / "i18n"

SOURCE_ZH = I18N_DIR / "zh.json"
SOURCE_EN = I18N_DIR / "en.json"

# 双轨策略：
# - zh.json 仅用于生成 zh-Hant.json
# - en.json 用于生成除 zh/en/zh-Hant 之外的所有语言文件
ZH_TRACK_TARGET = "zh-Hant"

# 永远不翻译 / 固定写法（按需扩展）
GLOSSARY = {
    "WealthX": "WealthX",
    "Flow": "Flow",
    "Flows": "Flows",
}

MODEL = os.getenv("OPENAI_I18N_MODEL", "gpt-4.1-mini")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


def build_needs_translate(
    src: Dict[str, str],
    dst: Dict[str, str],
    dst_meta: Dict[str, Any],
) -> Dict[str, str]:
    """
    规则：
    - dst 缺 key：翻译
    - 源文字变了（hash 不同）：重翻
    - dst[key] 为空：翻译
    """
    dst_hashes = (dst_meta.get("source_hashes") or {})
    if not isinstance(dst_hashes, dict):
        dst_hashes = {}

    needs: Dict[str, str] = {}
    for k, v in src.items():
        src_hash = sha(v)
        old_hash = dst_hashes.get(k)

        if k not in dst:
            needs[k] = v
        elif not isinstance(dst.get(k), str) or dst.get(k, "").strip() == "":
            needs[k] = v
        elif old_hash != src_hash:
            needs[k] = v

    return needs


def sync_deletions(src: Dict[str, str], dst_full: Dict[str, Any]) -> None:
    """规则 1：源里删了 key，目标也删（保留 _meta）"""
    for k in list(dst_full.keys()):
        if k == "_meta":
            continue
        if k not in src:
            dst_full.pop(k, None)


def translate_batch(src_lang: str, dst_lang: str, items: Dict[str, str]) -> Dict[str, str]:
    """
    批量翻译：输入 JSON，输出必须是 JSON（key 不翻译，value 翻译）
    JSON mode 需要你在提示里明确要求输出 JSON。 [oai_citation:0‡OpenAI平台](https://platform.openai.com/docs/api-reference/runs)
    """
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
        ],
        "output": "JSON object only",
    }

    # 用 Chat Completions + JSON mode 保证可 parse（更稳）
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    text = resp.choices[0].message.content.strip()
    data = json.loads(text)

    out: Dict[str, str] = {}
    for k, v in data.items():
        out[str(k)] = apply_glossary(str(v))
    return out


def target_langs_from_folder() -> list[str]:
    """只看 i18n 目录现有的 *.json（按你要求）"""
    langs = []
    for p in I18N_DIR.glob("*.json"):
        langs.append(p.stem)
    # 去重排序
    return sorted(set(langs))


def process_one_target(target_lang: str, src_lang: str, src_path: Path) -> None:
    src_full = load_json(src_path)
    src, _ = split_meta(src_full)

    dst_path = I18N_DIR / f"{target_lang}.json"
    dst_full = load_json(dst_path)
    dst, dst_meta = split_meta(dst_full)

    # 规则 1：同步删除
    sync_deletions(src, dst_full)

    # 规则 2：新增/改动 -> needs translate
    needs = build_needs_translate(src, dst, dst_meta)
    if not needs:
        print(f"[skip] {target_lang}: nothing to translate")
        return

    print(f"[translate] {src_lang} -> {target_lang}: {len(needs)} keys")
    translated = translate_batch(src_lang, target_lang, needs)

    # merge 写回（只写字符串 key）
    for k, v in translated.items():
        dst_full[k] = v

    # 更新 meta hash（用于下次判断是否改动）
    meta = dst_full.get("_meta") if isinstance(dst_full.get("_meta"), dict) else {}
    meta.setdefault("source_hashes", {})
    if not isinstance(meta["source_hashes"], dict):
        meta["source_hashes"] = {}

    for k, src_text in needs.items():
        meta["source_hashes"][k] = sha(src_text)

    meta["generated_by"] = "i18n_autotranslate.py"
    meta["source_lang"] = src_lang
    meta["target_lang"] = target_lang
    dst_full["_meta"] = meta

    save_json(dst_path, dst_full)
    time.sleep(0.2)  # 轻微限速


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY env var")

    # 只看目录里已有语言文件
    langs = target_langs_from_folder()

    # zh -> zh-Hant
    if ZH_TRACK_TARGET in langs:
        process_one_target(ZH_TRACK_TARGET, "zh-Hans", SOURCE_ZH)

    # en -> others（排除 zh/en/zh-Hant）
    for lang in langs:
        if lang in ("zh", "en", "zh-Hant"):
            continue
        process_one_target(lang, "en", SOURCE_EN)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, List

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

MODEL = os.getenv("OPENAI_I18N_MODEL", "gpt-5-mini")
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


def get_source_hashes(dst_meta: Dict[str, Any]) -> Dict[str, str]:
    hashes = dst_meta.get("source_hashes")
    if not isinstance(hashes, dict):
        return {}
    # 确保都是 str
    out: Dict[str, str] = {}
    for k, v in hashes.items():
        if isinstance(k, str) and isinstance(v, str):
            out[k] = v
    return out


def sync_deletions(src: Dict[str, str], dst_full: Dict[str, Any]) -> None:
    """
    规则 1：源里删了 key，目标也删（保留 _meta）
    同时清理 _meta.source_hashes 中已删 key 的 hash（保持 meta 干净）
    """
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

    if isinstance(meta, dict):
        meta["source_hashes"] = hashes
        dst_full["_meta"] = meta


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

        # 已有翻译
        if old_hash is None:
            # 首次接入：不强制重翻，先补 hash
            needs_hash_seed.append(k)
            continue

        if old_hash != src_hash:
            needs_translate[k] = v

    return needs_translate, needs_hash_seed


def translate_batch(src_lang: str, dst_lang: str, items: Dict[str, str]) -> Dict[str, str]:
    """
    批量翻译：输入 JSON，输出必须是 JSON（key 不翻译，value 翻译）
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
            "Keep email/URLs/phone numbers unchanged.",
            "Do not translate product/brand names such as WealthX and glossary terms."
        ],
        "output": "JSON object only"
    }

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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
from pathlib import Path
from typing import Dict, Tuple

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
I18N_DIR = ROOT / "i18n"

SOURCE_ZH = I18N_DIR / "zh.json"
SOURCE_EN = I18N_DIR / "en.json"

# 双轨：中文 → 繁中；英文 → 其它
ZH_TRACK = {"zh-Hant": "zh-Hant"}
EN_TRACK = {
    "de": "de",
    "fr": "fr",
    "ja": "ja",
    "ko": "ko",
    "es": "es",
    "it": "it",
    "id": "id",
    "hi": "hi",
    "pl": "pl",
    "pt": "pt",
    "sv": "sv",
}

# 你可以在这里维护“永远不翻译/固定写法”的词表（按需扩展）
GLOSSARY = {
    "WealthX": "WealthX",
    "Flow": "Flow",
    "Flows": "Flows",
}

MODEL = os.getenv("OPENAI_I18N_MODEL", "gpt-4.1-mini")  # 你也可以换更强的模型
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_json(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict[str, str]) -> None:
    # 保持 key 排序，减少 diff 噪音
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def diff_keys(src: Dict[str, str], dst: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    返回 (needs_translate, kept)
    needs_translate: dst 缺失 或 与 src 改动相关（我们用简单策略：src 值变了就重翻）
    kept: 保留 dst 里已有的翻译
    """
    needs = {}
    kept = dict(dst)

    for k, v in src.items():
        if k not in dst:
            needs[k] = v
        else:
            # 如果源文案改了：我们标记重翻（你也可以改成“只新增不重翻”）
            # 这里无法直接判断“源是否改过”，所以用一个很实用的做法：
            # 在 dst 里存一个隐藏字段 _meta_source_hash 也行，但先简化。
            # 简化策略：如果 dst[k] 为空也重翻
            if not isinstance(dst.get(k), str) or dst.get(k).strip() == "":
                needs[k] = v

    return needs, kept


def apply_glossary(text: str) -> str:
    for k, v in GLOSSARY.items():
        text = text.replace(k, v)
    return text


def translate_batch(src_lang: str, dst_lang: str, items: Dict[str, str]) -> Dict[str, str]:
    """
    用 OpenAI 做一次批量翻译（key 不翻译，value 翻译）
    """
    # 让模型“按 App Store / 产品网站语气本地化”，避免硬翻
    system = (
        "You are a professional product localization expert for an Apple-style product website. "
        "Translate naturally for the target locale, concise, clear, and idiomatic. "
        "Do NOT translate brand names or glossary terms. Keep punctuation style appropriate."
    )

    # 用 JSON 输入输出，减少格式问题
    user = {
        "task": "translate_i18n",
        "source_language": src_lang,
        "target_language": dst_lang,
        "glossary": GLOSSARY,
        "items": items,
        "rules": [
            "Keep keys unchanged; translate only values.",
            "Keep email/URLs/phone numbers unchanged.",
            "Keep 'WealthX' unchanged.",
            "If a value contains colon labels like 'Email:' keep the label idiomatic in target language.",
            "Keep tone similar to Apple marketing pages: minimal, confident, not exaggerated."
        ],
        "output_format": "JSON object mapping the same keys to translated strings"
    }

    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
        ],
        # 让输出稳定为 JSON（如果你用的模型支持严格 JSON，可以再加严）
    )

    text = resp.output_text.strip()
    # 兜底：有些模型会包 ```json
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        text = text.replace("json", "", 1).strip()

    data = json.loads(text)
    # glossary 再保险一次
    return {k: apply_glossary(str(v)) for k, v in data.items()}


def generate_from_source(source_path: Path, targets: Dict[str, str], src_lang: str) -> None:
    src = load_json(source_path)

    for lang_code in targets.keys():
        dst_path = I18N_DIR / f"{lang_code}.json"
        dst = load_json(dst_path)

        needs, kept = diff_keys(src, dst)
        if not needs:
            print(f"[skip] {lang_code}: nothing to translate")
            continue

        print(f"[translate] {src_lang} -> {lang_code}: {len(needs)} keys")
        translated = translate_batch(src_lang, lang_code, needs)

        # merge：保留旧翻译 + 覆盖新翻译
        kept.update(translated)
        save_json(dst_path, kept)

        time.sleep(0.2)  # 轻微限速


def main():
    if not os.getenv("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"):
        raise RuntimeError("Missing OPENAI_API_KEY env var")

    generate_from_source(SOURCE_ZH, ZH_TRACK, "zh-Hans")
    generate_from_source(SOURCE_EN, EN_TRACK, "en")


if __name__ == "__main__":
    main()

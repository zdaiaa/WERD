# scripts/parse_hist_all.py
import re, io, os, json, sys
import datetime as dt
import requests
from zoneinfo import ZoneInfo
from datetime import timedelta
from iex_parser import Parser, TOPS_1_6  # pip install iex_parser

INDEX_URLS = [
    "https://www.iexexchange.io/resources/trading/market-data",
    "https://www.iextrading.com/trading/market-data/",
]
EASTERN = ZoneInfo("America/New_York")

# 生成分片（按首字母 A..Z 和 0-9）——如不需要可改为 False
ENABLE_SHARDS = True

def last_us_trading_day(now_utc: dt.datetime | None = None) -> dt.date:
    if now_utc is None:
        now_utc = dt.datetime.now(dt.timezone.utc)
    d_et = now_utc.astimezone(EASTERN).date()
    wd = d_et.weekday()  # Mon=0..Sun=6
    if wd == 0:  # Mon -> Fri
        return d_et - timedelta(days=3)
    if wd in (1,2,3,4):  # Tue..Fri
        return d_et - timedelta(days=1)
    return d_et - timedelta(days=wd - 4)  # Weekend -> Fri

def find_hist_link_for_day(ymd: str) -> str | None:
    for idx in INDEX_URLS:
        try:
            html = requests.get(idx, timeout=30).text
            links = re.findall(r'href="([^"]+\.pcap\.gz)"', html, flags=re.I)
            wanted = [u for u in links if ymd in u and "TOPS" in u.upper()]
            for u in wanted:
                if u.startswith("http"): return u
                base = idx.split("/resources")[0].split("/trading")[0].rstrip("/")
                return base + ("" if u.startswith("/") else "/") + u
        except Exception:
            continue
    return None

def extract_all_closes(blob: bytes, trade_day: dt.date) -> dict[str, float]:
    """返回当日所有股票的 venue-only 收盘价（最后一笔）"""
    start = dt.datetime.combine(trade_day, dt.time(9,30), tzinfo=EASTERN).astimezone(dt.timezone.utc)
    end   = dt.datetime.combine(trade_day, dt.time(16,0), tzinfo=EASTERN).astimezone(dt.timezone.utc)
    closes: dict[str, float] = {}
    with Parser(io.BytesIO(blob), TOPS_1_6) as reader:
        for msg in reader:
            if msg.get("type") != "trade_report":
                continue
            ts = msg["timestamp"]
            if not (start <= ts <= end):  # 仅盘中
                continue
            sym = msg["symbol"].decode().upper()
            price = float(msg["price"])
            closes[sym] = price  # 覆盖为“最后一笔”
    return closes

def shard_key(symbol: str) -> str:
    c = symbol[:1].upper()
    if "A" <= c <= "Z": return c
    if "0" <= c <= "9": return "0-9"
    return "other"

def main():
    trade_day = last_us_trading_day()
    ymd = trade_day.strftime("%Y%m%d")
    link = find_hist_link_for_day(ymd)
    if not link:
        print(f"NO_UPDATE: No HIST TOPS link found for {ymd}")
        sys.exit(78)

    print("Downloading:", link)
    blob = requests.get(link, timeout=180).content

    closes = extract_all_closes(blob, trade_day)
    if not closes:
        print("NO_UPDATE: parsed 0 symbols")
        sys.exit(78)

    # 紧凑格式：减少重复字段，显著降低体积
    #
    # {
    #   "date": "YYYY-MM-DD",
    #   "source": "IEX HIST (T+1) — ...",
    #   "prices": { "AAPL": 227.12, "NVDA": 125.34, ... }
    # }
    attrib = ("IEX HIST (T+1) — Data provided for free by IEX. "
              "By accessing or using IEX Historical Data, you agree to the IEX Historical Data Terms of Use.")
    compact = {
        "date": trade_day.strftime("%Y-%m-%d"),
        "source": attrib,
        "prices": {k: round(v, 2) for k, v in sorted(closes.items())}
    }

    os.makedirs("docs", exist_ok=True)
    per_day = f"docs/eod-{trade_day.strftime('%Y-%m-%d')}.json"
    with open(per_day, "w", encoding="utf-8") as f:
        json.dump(compact, f, ensure_ascii=False, separators=(",",":"))
    with open("docs/latest.json", "w", encoding="utf-8") as f:
        json.dump(compact, f, ensure_ascii=False, separators=(",",":"))
    print(f"Wrote {per_day} and docs/latest.json with {len(closes)} symbols")

    if ENABLE_SHARDS:
        shard_dir = "docs/shards"
        os.makedirs(shard_dir, exist_ok=True)
        buckets = {}
        for sym, px in compact["prices"].items():
            buckets.setdefault(shard_key(sym), {})[sym] = px
        for key, mapping in buckets.items():
            shard_obj = {"date": compact["date"], "source": compact["source"], "prices": mapping}
            with open(os.path.join(shard_dir, f"{key}.json"), "w", encoding="utf-8") as f:
                json.dump(shard_obj, f, ensure_ascii=False, separators=(",",":"))
        print(f"Wrote {len(buckets)} shard files to {shard_dir}/")

if __name__ == "__main__":
    main()

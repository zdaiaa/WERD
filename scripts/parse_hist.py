# scripts/parse_hist.py
import re, io, os, json, sys
import datetime as dt
import requests
from zoneinfo import ZoneInfo
from datetime import timedelta
from iex_parser import Parser, TOPS_1_6  # pip install iex_parser

# IEX 站点上含 HIST 下载链接的页面（备用两个，都扫一遍）
INDEX_URLS = [
    "https://www.iexexchange.io/resources/trading/market-data",
    "https://www.iextrading.com/trading/market-data/",
]
EASTERN = ZoneInfo("America/New_York")

def last_us_trading_day(now_utc: dt.datetime | None = None) -> dt.date:
    if now_utc is None:
        now_utc = dt.datetime.now(dt.timezone.utc)
    d_et = now_utc.astimezone(EASTERN).date()
    wd = d_et.weekday()  # Mon=0..Sun=6
    if wd == 0:  # Mon -> Fri
        return d_et - timedelta(days=3)
    if wd in (1,2,3,4):  # Tue..Fri -> prev day
        return d_et - timedelta(days=1)
    # weekend -> last Fri
    return d_et - timedelta(days=wd - 4)

def load_symbols() -> list[str]:
    path = "symbols.txt"
    if os.path.exists(path):
        syms = [s.strip().upper() for s in open(path, "r", encoding="utf-8").read().splitlines() if s.strip()]
        if syms: return syms
    env = os.getenv("SYMBOLS", "")
    syms = [s.strip().upper() for s in env.split(",") if s.strip()]
    if not syms:
        print("ERROR: No symbols provided. Create symbols.txt or set SYMBOLS env.", file=sys.stderr)
        sys.exit(2)
    return syms

def find_hist_link_for_day(ymd: str) -> str | None:
    for idx in INDEX_URLS:
        try:
            html = requests.get(idx, timeout=30).text
            links = re.findall(r'href="([^"]+\.pcap\.gz)"', html, flags=re.I)
            wanted = [u for u in links if ymd in u and "TOPS" in u.upper()]
            for u in wanted:
                if u.startswith("http"):
                    return u
                # 补全相对链接
                base = idx.split("/resources")[0].split("/trading")[0].rstrip("/")
                return base + ("" if u.startswith("/") else "/") + u
        except Exception:
            continue
    return None

def extract_closes(blob: bytes, trade_day: dt.date, symbols: set[str]) -> dict[str, float]:
    start = dt.datetime.combine(trade_day, dt.time(9,30), tzinfo=EASTERN).astimezone(dt.timezone.utc)
    end   = dt.datetime.combine(trade_day, dt.time(16,0), tzinfo=EASTERN).astimezone(dt.timezone.utc)
    closes: dict[str, float] = {}
    with Parser(io.BytesIO(blob), TOPS_1_6) as reader:
        for msg in reader:
            if msg.get("type") != "trade_report":
                continue
            ts = msg["timestamp"]
            if not (start <= ts <= end):
                continue
            sym = msg["symbol"].decode().upper()
            if sym not in symbols:
                continue
            price = float(msg["price"])
            closes[sym] = price  # 遍历即时间序，覆盖=最后一笔
    return closes

def main():
    symbols = load_symbols()
    wanted = set(symbols)
    trade_day = last_us_trading_day()
    ymd = trade_day.strftime("%Y%m%d")
    link = find_hist_link_for_day(ymd)
    if not link:
        print(f"NO_UPDATE: No HIST TOPS link found for {ymd}")
        sys.exit(78)  # 用 78 表示“未更新”

    print("Downloading:", link)
    blob = requests.get(link, timeout=180).content  # pcap.gz（可直接给解析器）

    closes = extract_closes(blob, trade_day, wanted)
    # 仅当有至少1只目标股票成功解析到 close 时才写文件
    out = []
    attrib = ("IEX HIST (T+1) — Data provided for free by IEX. "
              "By accessing or using IEX Historical Data, you agree to the IEX Historical Data Terms of Use.")
    for s in symbols:
        if s in closes:
            out.append({
                "symbol": s,
                "date": trade_day.strftime("%Y-%m-%d"),
                "close": round(closes[s], 2),
                "adj_close": None,
                "volume": None,
                "source": attrib
            })

    if not out:
        print("NO_UPDATE: No closes parsed for requested symbols")
        sys.exit(78)

    os.makedirs("docs", exist_ok=True)
    # 按日期留档 + latest.json
    per_day = f"docs/eod-{trade_day.strftime('%Y-%m-%d')}.json"
    with open(per_day, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",",":"))
    with open("docs/latest.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",",":"))
    print(f"Wrote {per_day} and docs/latest.json with {len(out)} symbols")

if __name__ == "__main__":
    main()

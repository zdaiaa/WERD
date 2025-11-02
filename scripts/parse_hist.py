# scripts/parse_hist.py
import re, io, os, json, datetime as dt
import requests
from zoneinfo import ZoneInfo
from datetime import timedelta
from iex_parser import Parser, TOPS_1_6  # pip install iex_parser

IEX_HIST_INDEX = "https://www.iexexchange.io/resources/trading/market-data"  # 含 HIST 下载链接的页
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

def find_hist_links(ymd: str) -> list[str]:
    html = requests.get(IEX_HIST_INDEX, timeout=30).text
    links = re.findall(r'href="([^"]+\.pcap\.gz)"', html, flags=re.I)
    wanted = [u for u in links if ymd in u and "TOPS" in u.upper()]
    out = []
    for u in wanted:
        if u.startswith("http"):
            out.append(u)
        else:
            out.append("https://www.iexexchange.io" + ("" if u.startswith("/") else "/") + u)
    if not out:
        raise SystemExit(f"No HIST TOPS link for {ymd}")
    return out

def extract_closes(blob: bytes, trade_day: dt.date, symbols: set[str]) -> dict[str, float]:
    start = dt.datetime.combine(trade_day, dt.time(9,30), tzinfo=EASTERN).astimezone(dt.timezone.utc)
    end   = dt.datetime.combine(trade_day, dt.time(16,0), tzinfo=EASTERN).astimezone(dt.timezone.utc)
    closes: dict[str, float] = {}
    with Parser(io.BytesIO(blob), TOPS_1_6) as reader:
        for msg in reader:
            if msg.get("type") != "trade_report":
                continue
            ts = msg["timestamp"]
            if not (start <= ts <= end):  # 盘中时间窗
                continue
            sym = msg["symbol"].decode().upper()
            if sym not in symbols:
                continue
            price = float(msg["price"])
            closes[sym] = price  # 顺序即时间序，覆盖=最后一笔
    return closes

def main():
    # 需要的股票列表：环境变量 SYMBOLS="AAPL,NVDA,TSLA"
    symbols = set(s.strip().upper() for s in os.getenv("SYMBOLS","").split(",") if s.strip())
    if not symbols:
        raise SystemExit("SYMBOLS env required, e.g. AAPL,NVDA,TSLA")

    trade_day = last_us_trading_day()
    ymd = trade_day.strftime("%Y%m%d")
    url = find_hist_links(ymd)[0]
    blob = requests.get(url, timeout=120).content

    closes = extract_closes(blob, trade_day, symbols)

    # 生成 EODDTO 兼容的 JSON
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
    os.makedirs("docs", exist_ok=True)
    with open("docs/latest.json", "w") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",",":"))

    print(f"Wrote docs/latest.json for {trade_day} with {len(out)} symbols")

if __name__ == "__main__":
    main()

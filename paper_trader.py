#!/usr/bin/env python3
"""
Moon Reversal Paper Trader — 模拟交易器

用法:
  python3 paper_trader.py              # 检查本周信号
  python3 paper_trader.py --backtest   # 跑完整回测
  python3 paper_trader.py --journal    # 查看交易日志
  python3 paper_trader.py --status     # 当前持仓状态
"""

import json, sys, os, datetime, argparse
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from strategies import MoonReversalStrategy

JOURNAL_PATH = os.path.join(SCRIPT_DIR, "trade_journal.json")
BINANCE_MONTHLY = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1M&limit=48"
BINANCE_WEEKLY = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1w&limit=208"


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'V5-PaperTrader/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def parse_candle(raw, fmt='monthly'):
    return {
        'date': datetime.datetime.fromtimestamp(raw[0] // 1000).strftime(
            '%Y-%m' if fmt == 'monthly' else '%Y-%m-%d'),
        'open': float(raw[1]),
        'high': float(raw[2]),
        'low': float(raw[3]),
        'close': float(raw[4]),
    }


def load_journal():
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH) as f:
            return json.load(f)
    return {'trades': [], 'stats': {'total_trades': 0, 'wins': 0, 'losses': 0, 'total_pnl': 0.0}}


def save_journal(j):
    with open(JOURNAL_PATH, 'w') as f:
        json.dump(j, f, indent=2, ensure_ascii=False)


def run_backtest():
    """完整回测"""
    months_raw = fetch(BINANCE_MONTHLY)
    weeks_raw = fetch(BINANCE_WEEKLY)
    
    months = [parse_candle(m, 'monthly') for m in months_raw]
    weeks = [parse_candle(w, 'weekly') for w in weeks_raw]
    
    strat = MoonReversalStrategy()
    trades = []
    last_month = None
    
    # Build month lookup
    month_map = {m['date']: m for m in months}
    
    for w in weeks:
        ym = w['date'][:7]
        # Feed PREVIOUS month when we cross boundary
        if last_month and ym != last_month and last_month in month_map:
            strat.feed_monthly(month_map[last_month])
        last_month = ym
        
        signal = strat.feed_weekly(w)
        if signal:
            trades.append(signal)
    
    # Print
    print(f"\n{'='*65}")
    print(f"Moon Reversal 回测")
    print(f"数据: {months[0]['date']} → {weeks[-1]['date']}")
    print(f"{'='*65}\n")
    
    sells = [t for t in trades if t['action'] == 'SELL']
    wins = [t for t in sells if t['pnl_pct'] > 0]
    
    if not sells:
        print("无交易记录")
        return
    
    print(f"交易: {len(sells)}笔 | 胜率: {len(wins)/len(sells)*100:.0f}%\n")
    
    for t in trades:
        if t['action'] == 'BUY':
            print(f"🟢 {t['date']}  BUY  @ ${t['price']:,.0f}  |  {t['reason']}")
        else:
            e = "✅" if t['pnl_pct'] > 0 else "❌"
            print(f"🔴 {t['date']}  SELL @ ${t['price']:,.0f}  |  {t['pnl_pct']:+.1f}% {e}  |  {t['reason']}")
    
    total = sum(t['pnl_pct'] for t in sells)
    print(f"\n累计: {total:+.1f}%")


def check_signal():
    """检查本周信号 + 当前持仓"""
    months_raw = fetch(BINANCE_MONTHLY)
    weeks_raw = fetch(BINANCE_WEEKLY)
    
    months = [parse_candle(m, 'monthly') for m in months_raw]
    weeks = [parse_candle(w, 'weekly') for w in weeks_raw]
    
    month_map = {m['date']: m for m in months}
    
    strat = MoonReversalStrategy()
    last_month = None
    last_signal = None
    
    for w in weeks:
        ym = w['date'][:7]
        if last_month and ym != last_month and last_month in month_map:
            strat.feed_monthly(month_map[last_month])
        last_month = ym
        signal = strat.feed_weekly(w)
        if signal:
            last_signal = signal
    
    print(f"\n{'='*50}")
    print(f"Moon Reversal — 当前状态")
    print(f"{'='*50}")
    
    # Use last COMPLETED month for entry gate
    completed_month = months[-2] if len(months) >= 2 else months[-1]
    current_month = months[-1]
    
    print(f"\n📅 最新周线: {weeks[-1]['date']}")
    print(f"   O:{weeks[-1]['open']:,.0f} H:{weeks[-1]['high']:,.0f} L:{weeks[-1]['low']:,.0f} C:{weeks[-1]['close']:,.0f}")
    
    print(f"\n📅 上月(已完成): {completed_month['date']}")
    prev_red = completed_month['close'] < completed_month['open']
    prev_ret = (completed_month['close'] - completed_month['open']) / completed_month['open'] * 100
    print(f"   O:{completed_month['open']:,.0f} C:{completed_month['close']:,.0f}  ({prev_ret:+.1f}%)")
    print(f"   状态: {'🔴 熊月 ← 入场门开' if prev_red else '🟢 牛月 ← 不入场'}")
    
    print(f"\n📅 本月(进行中): {current_month['date']}")
    cur_ret = (current_month['close'] - current_month['open']) / current_month['open'] * 100
    print(f"   O:{current_month['open']:,.0f} C:{current_month['close']:,.0f}  ({cur_ret:+.1f}%)")
    
    is_today_red = weeks[-1]['close'] < weeks[-1]['open']
    print(f"\n📅 本周: {'🔴 红周' if is_today_red else '🟢 绿周'} | 涨跌 {(weeks[-1]['close']-weeks[-1]['open'])/weeks[-1]['open']*100:+.1f}%")
    
    print(f"\n{'='*50}")
    print(f"🎯 入场判断")
    print(f"{'='*50}")
    
    if strat.in_position:
        print(f"\n📈 已在持仓中 (模拟)")
        print(f"   入场: ${strat.entry_price:,.0f} @ {strat.entry_date}")
        pnl = (weeks[-1]['close'] - strat.entry_price) / strat.entry_price * 100
        print(f"   浮盈: {pnl:+.1f}%")
        print(f"   最高: ${strat.highest:,.0f}")
        if strat.trail_active:
            print(f"   ⚡ 追踪止损已激活! 止损价: ${strat.highest*0.96:,.0f}")
    elif prev_red:
        print(f"\n✅ 上月是熊月 → 入场门已开")
        if not is_today_red:
            print(f"\n🔥 本周就是绿周线！应该买入 (模拟)")
            print(f"   入场价: ${weeks[-1]['close']:,.0f}")
            print(f"   Kelly仓位: {strat.kelly*100:.0f}%")
        else:
            print(f"\n⏳ 本周红周线，继续等本月首根绿周")
    else:
        print(f"\n⏸️ 上月非熊月，无信号，继续等待")
    
    # Show last signals
    if last_signal:
        print(f"\n{'='*50}")
        print(f"📋 最近信号")
        print(f"{'='*50}")
        print(f"   {last_signal['action']} @ ${last_signal['price']:,.0f} ({last_signal['date']})")
        print(f"   {last_signal['reason']}")


def show_journal():
    j = load_journal()
    print(f"\n📒 交易日志: {len(j['trades'])}笔\n")
    for t in j['trades']:
        e = "✅" if t.get('pnl', 0) > 0 else "❌"
        print(f"  {t['date']} {t['action']} @ ${t['price']:,.0f} {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Moon Reversal Paper Trader')
    parser.add_argument('--backtest', action='store_true', help='Run full backtest')
    parser.add_argument('--journal', action='store_true', help='Show trade journal')
    parser.add_argument('--status', action='store_true', help='Check current signal')
    args = parser.parse_args()

    if args.backtest:
        run_backtest()
    elif args.journal:
        show_journal()
    else:
        check_signal()

# 🌙 Moon Reversal Strategy · V5

> *"Wait for the bear to exhaust, then ride the reversal."*

A low-frequency BTC quantitative strategy using **monthly + weekly dual timeframe** analysis.  
Buy when the bear bleeds out. Exit with a trailing stop. That's it.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Status](https://img.shields.io/badge/status-paper%20trading-yellow)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 📈 Backtest Results (4YR / 2022–2026)

| Metric | Value |
|--------|-------|
| 📊 Total Trades | **15** |
| 🎯 Win Rate | **87%** (13W / 2L) |
| 💰 Cumulative Return | **+60.8%** |
| 📈 Best Trade | **+21.2%** |
| 📉 Worst Trade | **-13.8%** |
| ⏱️ Frequency | ~3 months/trade |
| 🎲 Kelly Fraction | 74.6% → Half-Kelly **37.3%** |

### Equity Curve

![Equity Curve](equity_curve.png)

### Trade Markers on BTC Weekly

![BTC Trades](btc_trades.png)

### P&L Distribution & Win Rate

![P&L Distribution](pnl_distribution.png)

### Drawdown

![Drawdown](drawdown.png)

---

## 🧠 Strategy Rules

```
ENTRY:  Monthly candle closes RED (bear month)
        → Next month's FIRST green weekly close = BUY

EXIT:   2 consecutive red weekly closes
        OR trailing stop activated: +5% profit → trail -4% from high

SIZING: Kelly Criterion → 74.6% optimal
        Using Half-Kelly: 37.3% of pool per trade
```

### Why it works

Most traders chase breakouts. This strategy does the opposite:

1. **Patience** — wait for a full month of bearish price action
2. **Confirmation** — enter only when weekly momentum flips green
3. **Protection** — trailing stop kicks in at +5%, locking profits automatically
4. **Math** — Kelly sizing prevents overbetting, half-Kelly adds conservatism

The trailing stop is the secret sauce: without it, win rate drops to 45%. With it, **87%**.

---

## 🗂️ Modules

```
V5-MoonReversal/
├── strategies/
│   └── __init__.py        🌙 MoonReversal strategy core
├── paper_trader.py         🔍 Manual signal check + backtest
├── weekly_runner.py        🤖 Weekly automated runner (cron)
├── observer.py             📡 Performance tracking + anomaly alerts
├── reporter.py             📊 Visual report generator (4 charts)
├── trade_journal.json      📒 Simulated trade history (gitignored)
└── analysis/               📝 Historical DCA/RSI research
```

---

## 🚀 Quick Start

```bash
# Install deps
python3 -m venv .venv && source .venv/bin/activate
pip install pandas matplotlib

# Check current signal
python3 paper_trader.py

# Run full backtest
python3 paper_trader.py --backtest

# Generate visual report
python3 reporter.py

# Weekly automated check
python3 weekly_runner.py
```

---

## 🔔 Automation

- **Weekly cron**: Every Monday 9:00 AM HKT → checks signal + runs observer → delivers to Telegram
- **Observer alerts**: win rate deviation, consecutive losses, drawdown breach → automatic warning

---

## 📋 中文说明

### 策略逻辑

月线收红（收盘 < 开盘）→ 标记为熊月 → 下月第一根绿周线收盘买入 →  
连续两根红周线卖出，或浮盈超过 +5% 后激活追踪止损（从高点 -4%）。

### 为什么有效

1. 等熊市耗尽再进场，而不是追涨
2. 周线动量确认后才开仓，过滤假反转
3. 追踪止损在 +5% 自动锁利，不让浮盈吐回
4. Kelly 公式控制仓位，半 Kelly 更保守

追踪止损是关键：不加它胜率只有 45%，加了直接拉到 87%。

---

## 🧪 Status

- ⚗️ **Paper trading only** — no real capital deployed
- 📡 **Weekly signal** auto-delivered via Telegram every Monday
- 🎓 Built for learning, designed for real deployment when ready

---

*Built with ❤️ by [Uname58](https://github.com/Uname58)*

# 🌙 Moon Reversal Strategy · V5

> *"Wait for the bear to exhaust, then ride the reversal."*  
> *「等熊市耗尽，再顺势而上。」*

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Status](https://img.shields.io/badge/status-paper%20trading-yellow)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

**Language** · [English](#-english) | [简体中文](#-简体中文)

---

# 🇬🇧 English

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

![Equity Curve](equity_curve.png)
![BTC Trades](btc_trades.png)
![P&L Distribution](pnl_distribution.png)
![Drawdown](drawdown.png)

---

## 🧠 Strategy

```
ENTRY:  Monthly RED candle → next month's first GREEN weekly close = BUY

EXIT:   2 consecutive RED weekly closes
        OR +5% profit activates trailing stop (-4% from high)

SIZING: Kelly 74.6% → Half-Kelly 37.3% (conservative)
```

### Why It Works

1. **Patience** — wait for a full month of bearish action before even looking
2. **Confirmation** — enter only when weekly momentum flips green (no guessing bottoms)
3. **Protection** — trailing stop locks profits automatically at +5%
4. **Math** — Kelly prevents overbetting; half-Kelly adds a safety margin

> 💡 The trailing stop is the secret: without it → 45% win rate. With it → **87%**.

---

## 🗂️ Modules

```
V5-MoonReversal/
├── strategies/
│   └── __init__.py        🌙 Strategy core
├── paper_trader.py         🔍 Signal check + backtest
├── weekly_runner.py        🤖 Weekly cron runner
├── observer.py             📡 Performance tracking + alerts
├── reporter.py             📊 Visual report (4 charts)
├── trade_journal.json      📒 Trade history (gitignored)
└── analysis/               📝 Historical DCA/RSI research
```

## 🚀 Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pandas matplotlib

python3 paper_trader.py              # Current signal
python3 paper_trader.py --backtest   # Full backtest
python3 reporter.py                  # Generate charts
python3 weekly_runner.py             # Weekly report
```

## 🔔 Automation

- ⏰ **Weekly cron** — Monday 9:00 AM HKT → signal check + observer → Telegram
- 🛡️ **Observer alerts** — win rate deviation · consecutive losses · drawdown breach

---

# 🇨🇳 简体中文

## 📈 回测结果（4年 / 2022–2026）

| 指标 | 数值 |
|------|------|
| 📊 总交易 | **15 笔** |
| 🎯 胜率 | **87%**（13胜 / 2负） |
| 💰 累计回报 | **+60.8%** |
| 📈 最大盈利 | **+21.2%** |
| 📉 最大亏损 | **-13.8%** |
| ⏱️ 频率 | ~3个月/笔 |
| 🎲 Kelly 仓位 | 74.6% → 半Kelly **37.3%** |

![Equity Curve](equity_curve.png)
![BTC Trades](btc_trades.png)
![P&L Distribution](pnl_distribution.png)
![Drawdown](drawdown.png)

---

## 🧠 策略逻辑

```
入场：月线收红（熊月）→ 次月首根绿周线收盘 = 买入

离场：连续两根红周线
      或浮盈 > +5% 激活追踪止损（从高点 -4%）

仓位：Kelly 74.6% → 半Kelly 37.3%（偏保守）
```

### 为什么有效

1. **耐心** — 等满一整月熊市才关注，不追涨杀跌
2. **确认** — 周线动量翻绿才进场，不猜底
3. **保护** — 追踪止损 +5% 自动锁利，利润不吐回
4. **数学** — Kelly 公式控仓，半 Kelly 更安全

> 💡 追踪止损是胜负手：不加 → 胜率 45%。加了 → **87%**。

---

## 🗂️ 模块

```
V5-MoonReversal/
├── strategies/
│   └── __init__.py        🌙 策略核心
├── paper_trader.py         🔍 手动查信号 / 回测
├── weekly_runner.py        🤖 每周自动运行
├── observer.py             📡 绩效追踪 + 异常告警
├── reporter.py             📊 可视化报告（4张图）
├── trade_journal.json      📒 模拟交易记录（gitignore）
└── analysis/               📝 历史 DCA/RSI 分析
```

## 🚀 快速开始

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pandas matplotlib

python3 paper_trader.py              # 查当前信号
python3 paper_trader.py --backtest   # 完整回测
python3 reporter.py                  # 生成图表
python3 weekly_runner.py             # 周报
```

## 🔔 自动化

- ⏰ **每周一早 9:00** — 自动查信号 + 跑观察层 → 推送到 Telegram
- 🛡️ **异常告警** — 胜率暴跌 · 连续亏损 · 回撤超标 → 自动提醒

---

## 🧪 Status · 状态

| | EN | CN |
|---|---|---|
| Phase | ⚗️ Paper trading | ⚗️ 模拟训练中 |
| Capital | ❌ No real funds | ❌ 无实盘资金 |
| Signal | 📡 Weekly via Telegram | 📡 每周 Telegram 推送 |
| Goal | Deploy when ready | 打磨到能上线为止 |

---

*Built with ❤️ by [Uname58](https://github.com/Uname58)*

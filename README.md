# 🌙 Moon Reversal Strategy · V5

> *"Wait for the bear to exhaust, then ride the reversal."*  
> *「等熊市耗尽，再顺势而上。」*

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Status](https://img.shields.io/badge/status-paper%20trading-yellow)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Assets](https://img.shields.io/badge/assets-20%20coins-blue)]()

---

## 📈 Backtest Results

### BTC (8YR / 2018–2026)

| Metric | Value |
|--------|-------|
| 📊 Total Trades | **36** |
| 🎯 Win Rate | **75%** |
| 💰 Cumulative Return | **+67.2%** |
| 📈 CAGR | **+6.6%** |
| 📉 Sharpe | **1.36** |
| 📉 Max Drawdown | **-41.5%** |

### Multi-Asset (4YR / same params)

| Coin | Trades | Win Rate | Return | Sharpe | MaxDD | RA Score* |
|------|--------|----------|--------|--------|-------|-----------|
| AVAX | 22 | 91% | **+152.9%** | 1.67 | -38.8% | 3.94 |
| SOL | 21 | 86% | **+130.2%** | 1.64 | -38.1% | 3.42 |
| FIL | 25 | 92% | **+122.8%** | 1.56 | -30.7% | 4.00 |
| NEAR | 25 | 80% | **+112.2%** | 1.54 | -43.6% | 2.57 |
| INJ | 20 | 80% | **+110.5%** | 1.61 | -37.0% | 2.99 |
| BTC | 15 | 87% | +72.5% | 1.58 | -33.5% | 2.16 |
| ETH | 20 | 75% | +39.2% | 1.35 | -41.5% | 0.94 |

*\*RA Score = Return ÷ |MaxDD| — higher is better risk-adjusted*

**18/20 coins profitable. 14/20 beat buy & hold.** The pattern is a genuine market structure phenomenon, not a BTC artifact.

---

## 🧠 Strategy

```
ENTRY:  Monthly RED candle → next month's first GREEN weekly close = BUY

EXIT:   2 consecutive RED weekly closes
        OR +5% profit activates trailing stop (-4% from high)

SIZING: 50% capital max per position, max 2 concurrent positions
        Priority: RA Score (risk-adjusted return)
```

### Why It Works

1. **Patience** — wait for a full month of bearish action before even looking
2. **Confirmation** — enter only when weekly momentum flips green (no guessing bottoms)
3. **Protection** — trailing stop locks profits automatically at +5%
4. **Math** — RA-ranked position allocation prevents over-concentration

> 💡 The trailing stop is the secret: without it → 45% win rate. With it → **87%** (4YR BTC).

---

## 🗂️ Project Structure

```
V5-MoonReversal/
├── cli_runner.py              🖥️  Unified CLI (signal / backtest / validate)
├── reporter_v2.py             📊  Trade-level 4-chart dashboard (multi-coin)
├── batch_backtest.py          🔬  20-coin batch backtest
├── config.py                  ⚙️  Centralized params (no magic numbers)
│
├── engine/                    ⚡ Execution layer
│   ├── signal_engine.py       多币信号引擎（参数化symbol）
│   ├── backtest_engine.py     复利权益曲线 + 费用/滑点
│   └── execution_simulator.py 手续费/滑点/跳空建模
│
├── strategies/
│   └── __init__.py            🌙 MoonReversalStrategy
│
├── analytics/                 📐 Analysis layer
│   ├── metrics.py             14项量化指标
│   ├── regime.py              牛/熊/震荡/恐慌分类
│   └── benchmarks.py          BTC/ETH买入持有对比
│
├── validation/                🛡️  Robustness
│   ├── walk_forward.py        训练→冻结→测试管线
│   ├── monte_carlo.py         10k bootstrap模拟
│   └── sensitivity.py         参数网格搜索
│
├── reporting/reporter.py      📈  连续权益曲线图表
│
├── paper_trading/             📋  Live tracking
│   ├── weekly_check.py        每周信号检查（BTC/ETH/SOL）
│   ├── moon_scan.py           20币信号扫描
│   ├── select5.py             精选5 + RA排名 + 仓位规则
│   └── journal.py             纸交日志
│
└── reports/                   📁  回测图表输出
```

---

## 🚀 Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pandas matplotlib

# Current signals (BTC/ETH/SOL)
python3 cli_runner.py signal

# Full backtest (BTC)
python3 cli_runner.py backtest

# Validation suite
python3 cli_runner.py validate

# 20-coin batch backtest
python3 batch_backtest.py

# Multi-coin trade-level charts
python3 reporter_v2.py

# Weekly scan
python3 paper_trading/moon_scan.py

# Select 5 + position rules
python3 paper_trading/select5.py
```

---

## 🔔 Automation (HKT)

| Time | Job | Content |
|------|-----|---------|
| Daily 08:00 | Market Briefing | BTC/ETH/SOL + US stocks + F&G |
| Daily 21:00 | Market Briefing | Same, evening |
| Mon 09:00 | V5 Weekly Check | BTC/ETH/SOL signal + journal |
| Mon 09:00 | 20-Coin Scan | Full watchlist buy signals |
| Mon 09:00 | Select 5 Report | Top 5 + RA rank + position sizing |

---

## 🧪 Status

| | EN | CN |
|---|---|---|
| Phase | ⚗️ Paper trading | ⚗️ 纸交验证中 |
| Capital | ❌ No real funds | ❌ 无实盘资金 |
| Assets | BTC/ETH/SOL + 17 alts | 20币监控 |
| Signal | 📡 Weekly via Telegram | 📡 每周 Telegram 推送 |
| Goal | Deploy when ready | 打磨到能上线为止 |

---

*Built with ❤️ by [Uname58](https://github.com/Uname58)*

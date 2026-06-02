# Moon Reversal Strategy — V5 量化交易系统

BTC 熊月反转策略，基于月线 + 周线双时间框架。

## 策略规则

- **入场**：月线收红(熊月) → 下月首根绿周线收盘买入
- **离场**：连续2根红周线 或 浮盈>+5% 激活追踪止损(-4%从高点)
- **仓位**：Kelly 74.6% (半Kelly 37.3%)

## 回测 (4年 / 2022-2026)

| 指标 | 数值 |
|------|------|
| 交易次数 | 15 |
| 胜率 | 87% |
| 累计回报 | +60.8% |
| 最大盈利 | +21.2% |
| 最大亏损 | -13.8% |
| 频率 | ~3月/笔 |

## 模块

```
strategies/         策略核心
paper_trader.py     手动查信号 / 回测
weekly_runner.py    每周自动运行
observer.py         绩效追踪 + 自适应
```

## 用法

```bash
python3 paper_trader.py           # 当前信号
python3 paper_trader.py --backtest # 完整回测
python3 weekly_runner.py          # 周报
```

## 状态

🧪 模拟训练中 — 无实盘资金
📡 每周一早9点 Telegram 自动推送信号

"""
Moon Reversal Strategy — 熊月反转策略

规则:
  1. 月线收红(close < open) → 标记熊月
  2. 熊月后首根绿周线(close > open)收盘买入
  3. 离场:
     a. 连续2根红周线
     b. OR 浮盈>+5%后激活追踪止损(从高点-4%)
  4. Kelly 仓位: 74.6% (半Kelly: 37.3%)
"""

import json, datetime
from typing import Optional

class MoonReversalStrategy:
    def __init__(self, kelly_fraction: float = 0.373):
        """
        kelly_fraction: 仓位比例 (默认半Kelly 37.3%)
        """
        self.kelly = kelly_fraction
        self.reset()

    def reset(self):
        self.in_position = False
        self.entry_price = 0.0
        self.entry_date = ""
        self.highest = 0.0
        self.trail_active = False
        self.red_week_count = 0
        self.last_month_red = False
        self.last_month = None
        self.entry_allowed = False

    def _is_green(self, candle: dict) -> bool:
        return candle['close'] > candle['open']

    def _is_red(self, candle: dict) -> bool:
        return candle['close'] < candle['open']

    def feed_monthly(self, month: dict):
        """每月调用一次，检测是否熊月"""
        if self._is_red(month):
            self.entry_allowed = True  # 下月允许进场
        else:
            self.entry_allowed = False

    def feed_weekly(self, week: dict) -> Optional[dict]:
        """
        每周调用一次，返回 None 或交易信号 dict:
          {'action': 'BUY'/'SELL', 'price': float, 'date': str, 'reason': str}
        """
        if not self.in_position:
            # === ENTRY ===
            if self.entry_allowed and self._is_green(week):
                self.in_position = True
                self.entry_price = week['close']
                self.entry_date = week['date']
                self.highest = week['close']
                self.trail_active = False
                self.red_week_count = 0
                self.entry_allowed = False
                return {
                    'action': 'BUY',
                    'price': week['close'],
                    'date': week['date'],
                    'reason': f'熊月后首绿周 | Kelly仓位 {self.kelly*100:.0f}%',
                }
            # Reset entry permission if month changed without entry
            if self._is_green(week):
                self.entry_allowed = False
        else:
            # === EXIT CHECKS ===
            # Update high
            if week['high'] > self.highest:
                self.highest = week['high']

            # Trailing stop activation
            if not self.trail_active:
                profit_pct = (self.highest - self.entry_price) / self.entry_price * 100
                if profit_pct >= 5.0:
                    self.trail_active = True

            # Check exits
            exit_reason = None
            exit_price = None

            # Exit 1: 2 consecutive red weeks
            if self._is_red(week):
                self.red_week_count += 1
                if self.red_week_count >= 2:
                    exit_reason = '连续2红周'
                    exit_price = week['close']
            else:
                self.red_week_count = 0

            # Exit 2: Trailing stop hit (-4% from high)
            if self.trail_active and exit_reason is None:
                trail_price = self.highest * 0.96
                if week['low'] <= trail_price:
                    exit_reason = f'追踪止损({self.highest:.0f}→{trail_price:.0f})'
                    exit_price = trail_price

            if exit_reason:
                pnl = (exit_price - self.entry_price) / self.entry_price * 100
                result = {
                    'action': 'SELL',
                    'price': exit_price,
                    'date': week['date'],
                    'reason': exit_reason,
                    'pnl_pct': round(pnl, 2),
                }
                self.reset()
                return result

        return None

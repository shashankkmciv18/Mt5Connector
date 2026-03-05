"""
Example: How to add a custom strategy and firm
"""

# ==============================================================================
# EXAMPLE 1: Adding a Custom Firm
# ==============================================================================

# Edit firms/firm_profiles.py and add your firm:

"""
FIRM_PROFILES = {
    # ...existing firms...
    
    'alpha_capital_100k': {
        'name': 'Alpha Capital 100K Challenge',
        'max_daily_loss_percent': 4.0,           # 4% daily loss
        'max_total_drawdown_percent': 8.0,       # 8% total DD
        'profit_target_percent': 10.0,           # 10% target
        'min_trading_days': 5,                   # Need 5 trading days
        'challenge_days_limit': 60,              # 60 day limit
        'drawdown_type': 'trailing',             # Trailing DD
        'max_lot_per_trade': 50.0,               # Max 50 lots per trade
        'max_total_lots': 200.0,                 # Max 200 total open
    },
}
"""

# Then use it:
# python main.py --firm alpha_capital_100k --balance 100000


# ==============================================================================
# EXAMPLE 2: Custom Configuration
# ==============================================================================

# Edit CONFIG in main.py for your specific needs:

CONFIG_EXAMPLE = {
    'firm_key': 'ftmo_50k',                  # FTMO 50K challenge
    'starting_balance': 50000.0,             # Your starting balance
    'magic_filter': 888999,                  # Only monitor EA with magic 888999
    'auto_close_on_breach': True,            # Auto-close on violation
    'poll_interval': 0.5,                    # Check twice per second
    'log_level': 'DEBUG',                    # Verbose logging
}


# ==============================================================================
# EXAMPLE 3: Running Different Scenarios
# ==============================================================================

# Scenario 1: Conservative trader on FundedNext
"""
python main.py \\
    --firm funded_next_25k \\
    --balance 25000 \\
    --interval 2.0 \\
    --log-level INFO
"""

# Scenario 2: Aggressive trader with auto-close safety
"""
python main.py \\
    --firm e8_100k \\
    --balance 100000 \\
    --auto-close \\
    --interval 0.5 \\
    --log-level WARNING
"""

# Scenario 3: EA testing with magic filter
"""
python main.py \\
    --firm tft_50k \\
    --balance 50000 \\
    --magic 12345 \\
    --interval 1.0
"""


# ==============================================================================
# EXAMPLE 4: Programmatic Usage (Advanced)
# ==============================================================================

"""
If you want to use the components in your own Python scripts:
"""

from core.mt5_connector import MT5Connector
from core.prop_rule_engine import PropRuleEngine
from firms.firm_profiles import get_firm_profile

# Connect to MT5
mt5 = MT5Connector()
if mt5.connect():
    # Get account state
    account = mt5.get_account_state()
    print(f"Balance: ${account['balance']:.2f}")
    print(f"Equity: ${account['equity']:.2f}")

    # Load firm rules
    firm = get_firm_profile('ftmo_10k')

    # Create rule engine
    engine = PropRuleEngine(firm, starting_balance=10000.0)

    # Check rules
    positions = mt5.get_open_positions()
    trades = mt5.get_closed_trades_today()
    violation = engine.check_rules(account, positions, trades)

    if violation:
        print(f"VIOLATION: {violation.value}")
    else:
        # Get status
        status = engine.get_status_report(account)
        print(f"Status: {status['status']}")
        print(f"Profit: ${status['profit']:.2f}")

    mt5.disconnect()


# ==============================================================================
# EXAMPLE 5: Custom Rule Logic
# ==============================================================================

"""
If you need custom rules beyond the standard ones, you can extend PropRuleEngine:
"""

from core.prop_rule_engine import PropRuleEngine, RuleViolation
from enum import Enum

class CustomRuleViolation(Enum):
    MAX_OPEN_TRADES = "Too many open trades"
    NEWS_TRADING = "Trading during news"

class CustomPropRuleEngine(PropRuleEngine):
    def __init__(self, firm_profile, starting_balance, max_open_trades=5):
        super().__init__(firm_profile, starting_balance)
        self.max_open_trades = max_open_trades

    def check_custom_rules(self, open_positions):
        """Check additional custom rules"""
        # Rule: Max open trades
        if len(open_positions) > self.max_open_trades:
            return CustomRuleViolation.MAX_OPEN_TRADES

        # Rule: Don't trade during news (example - implement your logic)
        # if is_news_time():
        #     return CustomRuleViolation.NEWS_TRADING

        return None


# ==============================================================================
# EXAMPLE 6: Multiple Account Monitoring
# ==============================================================================

"""
To monitor multiple accounts, you could run separate instances:
"""

# Terminal 1: Account A
# python main.py --firm funded_next_6k --balance 6000

# Terminal 2: Account B
# python main.py --firm ftmo_10k --balance 10000


# ==============================================================================
# EXAMPLE 7: Simulation Mode (Without MT5)
# ==============================================================================

"""
For testing without MT5, create a mock connector:
"""

class MockMT5Connector:
    def __init__(self):
        self.connected = False
        self.balance = 10000.0
        self.equity = 10000.0

    def connect(self):
        self.connected = True
        return True

    def get_account_state(self):
        return {
            'balance': self.balance,
            'equity': self.equity,
            'margin': 0.0,
            'free_margin': self.equity,
            'profit': self.equity - self.balance,
            'leverage': 100,
            'login': 12345,
            'server': 'MockServer',
            'currency': 'USD'
        }

    def get_open_positions(self):
        return []

    def get_closed_trades_today(self):
        return []

    def disconnect(self):
        self.connected = False

# Use in testing:
# mt5 = MockMT5Connector()
# ... rest of your code


# ==============================================================================
# EXAMPLE 8: Logging Analysis
# ==============================================================================

"""
Analyze your logs to find patterns:
"""

import re
from pathlib import Path

def analyze_logs(log_file):
    """Extract key metrics from log file"""
    with open(log_file, 'r') as f:
        content = f.read()

    # Extract balance changes
    balances = re.findall(r'Balance: \$([0-9.]+)', content)

    # Extract violations
    violations = re.findall(r'VIOLATION: (.+)', content)

    return {
        'balances': [float(b) for b in balances],
        'violations': violations,
        'min_balance': min(float(b) for b in balances) if balances else 0,
        'max_balance': max(float(b) for b in balances) if balances else 0,
    }

# Usage:
# stats = analyze_logs('logs/prop_monitor_20260306_103000.log')
# print(f"Balance range: ${stats['min_balance']:.2f} - ${stats['max_balance']:.2f}")


# ==============================================================================
# EXAMPLE 9: Web Dashboard Integration
# ==============================================================================

"""
To expose data to a web dashboard, you could add a simple API:
"""

from flask import Flask, jsonify
import threading

app = Flask(__name__)
current_status = {}

@app.route('/status')
def get_status():
    return jsonify(current_status)

def run_web_api():
    app.run(port=5000)

# In your main monitoring loop:
# web_thread = threading.Thread(target=run_web_api, daemon=True)
# web_thread.start()
#
# # Update global status
# current_status = rule_engine.get_status_report(account_state)


# ==============================================================================
# EXAMPLE 10: Notification Integration
# ==============================================================================

"""
Add Telegram notifications:
"""

import requests

def send_telegram_alert(message, bot_token, chat_id):
    """Send Telegram message"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=data)

# In violation handler:
# if violation:
#     message = f"🚨 <b>RULE VIOLATION</b>\n{violation.value}"
#     send_telegram_alert(message, YOUR_BOT_TOKEN, YOUR_CHAT_ID)


print(__doc__)


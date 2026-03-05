# Prop Firm Rule Engine — MT5 + Python

Real-time prop firm challenge rule monitor. Connects to your running MT5 terminal and enforces firm rules on your live/demo account.

---

## Features

✅ Real-time monitoring of MT5 account  
✅ Enforces max daily loss and total drawdown rules  
✅ Supports 15+ prop firms (FTMO, FundedNext, E8, TFT, etc.)  
✅ Static and trailing drawdown calculations  
✅ Automatic position closing on rule breach (optional)  
✅ Trading days and profit target tracking  
✅ Detailed logging to files  
✅ EA magic number filtering  

---

## Project Structure

```
Simulator/
├── main.py                         ← Entry point — run this
├── requirements.txt
├── logs/                           ← Log files written here
├── core/
│   ├── mt5_connector.py            ← All MT5 API interaction
│   └── prop_rule_engine.py         ← Rule monitoring & enforcement
└── firms/
    └── firm_profiles.py            ← Firm configs (FTMO, TFT, E8, etc.)
```

---

## Setup

**Requirements:**
- Python 3.8+ (64-bit)
- MetaTrader 5 terminal installed
- MT5 account (demo or live)

**Installation:**

```bash
# Install dependencies
pip install -r requirements.txt
```

---

## Quick Start

### 1. List Available Firms

```bash
python main.py --list-firms
```

### 2. Configure Your Challenge

Edit the `CONFIG` section in `main.py`:

```python
CONFIG = {
    'firm_key': 'funded_next_6k',        # Choose your firm
    'starting_balance': 6000.0,          # Your challenge starting balance
    'magic_filter': None,                # Optional: EA magic number
    'auto_close_on_breach': False,       # Auto-close on rule violation
    'poll_interval': 1.0,                # Check every second
    'log_level': 'INFO',                 # Logging verbosity
}
```

### 3. Start Monitoring

**Make sure MT5 is running and logged in**, then:

```bash
python main.py
```

---

## Command Line Options

```bash
python main.py --list-firms              # List all firms
python main.py --firm ftmo_10k           # Use specific firm
python main.py --balance 10000           # Set starting balance
python main.py --magic 12345             # Filter by EA magic
python main.py --auto-close              # Auto-close on breach
python main.py --interval 2.0            # Change check interval
python main.py --log-level DEBUG         # Debug logging
```

---

## Supported Firms

| Key | Firm | Daily Loss | Total DD | Profit Target | DD Type |
|-----|------|------------|----------|---------------|---------|
| `funded_next_6k` | FundedNext 6K | 5% | 10% | 10% | Static |
| `funded_next_15k` | FundedNext 15K | 5% | 10% | 10% | Static |
| `ftmo_10k` | FTMO 10K | 5% | 10% | 10% | Static |
| `ftmo_25k` | FTMO 25K | 5% | 10% | 10% | Static |
| `tft_50k` | The Funded Trader 50K | 5% | 8% | 8% | Trailing |
| `e8_25k` | E8 Funding 25K | 5% | 8% | 8% | Trailing |
| `myfundedfx_10k` | MyFundedFX 10K | 5% | 10% | 8% | Static |

...and more! See `firms/firm_profiles.py` for full list.

---

## Rules Monitored

1. **Max Daily Loss** — equity must not drop more than X% from day's opening balance
2. **Max Total Drawdown** — equity must not drop more than X% (static/trailing)
3. **Profit Target** — detects when target is hit with enough trading days
4. **Min Trading Days** — tracks distinct days with closed trades
5. **Challenge Expiry** — flags if calendar deadline exceeded
6. **Lot Size Limits** — per-trade and total open lots (if configured)

---

## Example Output

```
======================================================================
  PROP FIRM CHALLENGE MONITOR STARTED
======================================================================
Firm: FundedNext Express 6K
Starting Balance: $6000.00
Poll Interval: 1.0s
Auto-close on breach: False
======================================================================

======================================================================
  FundedNext Express 6K - Challenge Status: ACTIVE
======================================================================
Balance: $6150.00 | Equity: $6180.00
Profit: $150.00 (2.50%) / Target: $600.00
----------------------------------------------------------------------
Daily Loss: $0.00 (0.00%) / Limit: $300.00
Total DD: $0.00 (0.00%) / Limit: $600.00
----------------------------------------------------------------------
Trading Days: 2/0 | Elapsed: 3/30 days
======================================================================
```

---

## Troubleshooting

**"Failed to connect to MT5"**
- Make sure MT5 is running
- Make sure you're logged into an account
- Check MT5 → Tools → Options → Expert Advisors → "Allow automated trading"

**"Cannot import MetaTrader5"**
- Install: `pip install MetaTrader5`
- Must use 64-bit Python

---

## License

MIT License

## Disclaimer

This tool is for monitoring purposes only. Always verify with your prop firm's official dashboard. Trade at your own risk.


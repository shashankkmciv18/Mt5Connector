# Quick Start Guide

## Running the Prop Firm Monitor

### Step 1: Install Dependencies

Make sure you have MetaTrader 5 installed and Python 64-bit.

```bash
pip install -r requirements.txt
```

### Step 2: List Available Firms

```bash
python main.py --list-firms
```

Output:
```
================================================================================
  Available Prop Firm Profiles
================================================================================
Key                       Firm Name                           DD Type   
--------------------------------------------------------------------------------
funded_next_6k            FundedNext Express 6K               Static    
ftmo_10k                  FTMO 10K Challenge                  Static    
tft_50k                   The Funded Trader 50K               Trailing  
e8_25k                    E8 Funding 25K                      Trailing  
... and more
================================================================================
```

### Step 3: Configure Your Challenge

Edit `main.py` CONFIG section:

```python
CONFIG = {
    'firm_key': 'funded_next_6k',           # Your firm
    'starting_balance': 6000.0,             # Your starting balance
    'magic_filter': None,                   # Optional EA magic number
    'auto_close_on_breach': False,          # Auto-close positions?
    'poll_interval': 1.0,                   # Check every N seconds
    'log_level': 'INFO',                    # DEBUG, INFO, WARNING, ERROR
}
```

### Step 4: Start MT5

1. Open MetaTrader 5
2. Login to your account
3. Make sure "Allow automated trading" is enabled:
   - Tools → Options → Expert Advisors → Check "Allow automated trading"

### Step 5: Run the Monitor

```bash
python main.py
```

The monitor will:
- ✅ Connect to MT5
- ✅ Track your equity in real-time
- ✅ Check rules every second
- ✅ Print status every 60 seconds
- ✅ Alert on violations
- ✅ Log everything to `logs/` folder

### Example Output

```
2026-03-06 10:15:30 | INFO | Connecting to MetaTrader 5...
2026-03-06 10:15:30 | INFO | Connected to MT5 - Account: 12345678
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

### Command Line Options

```bash
# Use different firm
python main.py --firm ftmo_10k --balance 10000

# Filter by EA magic number
python main.py --magic 12345

# Enable auto-close on breach
python main.py --auto-close

# Faster checks (every 0.5 seconds)
python main.py --interval 0.5

# Debug logging
python main.py --log-level DEBUG
```

---

## Rules Explained

### 1. Max Daily Loss (5%)
- Your equity cannot drop more than 5% from today's starting balance
- Resets every day at midnight (server time)
- Example: Start with $6000 → Max loss today = $300

### 2. Max Total Drawdown (10%)
- **Static**: Calculated from initial balance
  - Example: $6000 → Max DD = $600 (equity can't go below $5400)
- **Trailing**: Calculated from peak balance
  - Example: Reach $6500 → Max DD = $650 (equity can't go below $5850)

### 3. Profit Target (10%)
- Balance must reach starting + 10%
- Example: $6000 → Target = $6600
- May require minimum trading days

### 4. Trading Days
- Days with at least 1 closed trade
- Some firms require minimum (e.g., FTMO = 4 days)

### 5. Time Limit
- Most challenges: 30 days
- Some (TFT): 60 days

---

## Stopping the Monitor

Press `Ctrl+C` to stop. You'll see a final status report.

---

## Logs

Check `logs/` folder for detailed logs:
- Connection events
- Rule checks
- Violations
- All account state changes

---

## Troubleshooting

**"Failed to connect to MT5"**
- Is MT5 running?
- Are you logged in?
- Check: Tools → Options → Expert Advisors → "Allow automated trading"

**"Cannot import MetaTrader5"**
- Windows: Must use 64-bit Python
- Mac/Linux: Use MetaTrader5 package for your platform

**"Wrong firm settings"**
- Verify `starting_balance` matches your actual challenge
- Check firm rules match (some firms vary by region)

---

## Need Help?

Check the full README.md for more details.


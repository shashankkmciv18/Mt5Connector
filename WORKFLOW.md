# Complete Workflow Guide

## 🎯 What You Have Built

A **production-ready prop firm challenge monitoring system** that connects to MetaTrader 5 and enforces prop firm rules in real-time.

---

## 📋 Implementation Checklist

### ✅ Core Components Created

1. **MT5 Connector** (`core/mt5_connector.py`)
   - [x] Connect/disconnect from MT5
   - [x] Fetch account state (balance, equity, profit)
   - [x] Get open positions
   - [x] Get closed trades
   - [x] Close all positions (emergency)
   - [x] Magic number filtering

2. **Rule Engine** (`core/prop_rule_engine.py`)
   - [x] Daily loss tracking
   - [x] Total drawdown monitoring (static & trailing)
   - [x] Profit target detection
   - [x] Trading days counter
   - [x] Challenge expiry check
   - [x] Lot size limits
   - [x] Status reporting

3. **Firm Profiles** (`firms/firm_profiles.py`)
   - [x] FundedNext (3 profiles: 6K, 15K, 25K)
   - [x] FTMO (4 profiles: 10K, 25K, 50K, 100K)
   - [x] The Funded Trader (2 profiles: 50K, 100K)
   - [x] E8 Funding (3 profiles: 25K, 50K, 100K)
   - [x] MyFundedFX (2 profiles: 10K, 25K)
   - [x] Easy addition of custom firms

4. **Main Application** (`main.py`)
   - [x] Command-line interface
   - [x] Monitoring loop
   - [x] Logging system
   - [x] Error handling
   - [x] Graceful shutdown

5. **Documentation**
   - [x] README.md (full docs)
   - [x] QUICKSTART.md (quick start)
   - [x] IMPLEMENTATION_SUMMARY.md (this file)
   - [x] EXAMPLES.py (code examples)

---

## 🚀 Getting Started (Step by Step)

### Step 1: Install Dependencies
```bash
cd /Users/shashank/PycharmProjects/Simulator
pip install -r requirements.txt
```

### Step 2: List Available Firms
```bash
python main.py --list-firms
```

Expected output:
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
... (14 total)
================================================================================
```

### Step 3: Configure Your Challenge

Open `main.py` and edit the CONFIG section:

```python
CONFIG = {
    'firm_key': 'funded_next_6k',           # Choose your firm
    'starting_balance': 6000.0,             # Your account starting balance
    'magic_filter': None,                   # Optional: EA magic number
    'auto_close_on_breach': False,          # Auto-close positions on breach
    'poll_interval': 1.0,                   # Check every N seconds
    'log_level': 'INFO',                    # DEBUG, INFO, WARNING, ERROR
}
```

### Step 4: Start MT5
1. Open MetaTrader 5
2. Login to your account (demo or live)
3. Verify "Allow automated trading" is enabled:
   - Tools → Options → Expert Advisors
   - Check "Allow automated trading"

### Step 5: Run the Monitor
```bash
python main.py
```

### Step 6: Monitor Output
You'll see:
- Connection confirmation
- Initial status
- Real-time monitoring
- Status updates every 60 seconds
- Alerts on violations
- All logged to `logs/` folder

---

## 📊 Understanding the Output

### Status Report Breakdown

```
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

**What each line means:**

1. **Status**: ACTIVE (monitoring), PASSED (completed), FAILED (violated)
2. **Balance**: Closed positions + deposits - withdrawals
3. **Equity**: Balance + floating P&L from open positions
4. **Profit**: Current profit vs. starting balance (2.50% = $150/$6000)
5. **Target**: Profit goal to pass ($600 = 10% of $6000)
6. **Daily Loss**: How much equity dropped today from opening (resets at midnight)
7. **Total DD**: How much equity dropped from starting balance (static) or peak (trailing)
8. **Trading Days**: Days with closed trades / minimum required
9. **Elapsed**: Calendar days since start / maximum allowed

---

## 🎨 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  CLI Arguments Parser                                 │  │
│  │  - --list-firms, --firm, --balance, --magic, etc.   │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↓                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Logging Setup                                        │  │
│  │  - Creates logs/ directory                           │  │
│  │  - Configures file + console logging                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↓                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Monitoring Loop (every poll_interval)               │  │
│  │  1. Get account state                                │  │
│  │  2. Get open positions                               │  │
│  │  3. Get closed trades                                │  │
│  │  4. Check rules                                       │  │
│  │  5. Handle violations/completion                      │  │
│  │  6. Print status (every 60s)                         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ↓                   ↓                   ↓
┌──────────────────┐ ┌──────────────────┐ ┌────────────────┐
│ MT5Connector     │ │ PropRuleEngine   │ │ FirmProfiles   │
│ ─────────────    │ │ ──────────────   │ │ ────────────   │
│ • connect()      │ │ • check_rules()  │ │ • FTMO         │
│ • get_account()  │ │ • check_new_day()│ │ • FundedNext   │
│ • get_positions()│ │ • update_days()  │ │ • TFT          │
│ • get_trades()   │ │ • get_status()   │ │ • E8           │
│ • close_all()    │ │ • print_status() │ │ • MyFundedFX   │
│ • disconnect()   │ │                  │ │ • Custom...    │
└──────────────────┘ └──────────────────┘ └────────────────┘
         │                   │
         ↓                   ↓
┌──────────────────────────────────────────────────┐
│           MetaTrader 5 Terminal                  │
│  • Account state (balance, equity, profit)       │
│  • Positions (open trades)                       │
│  • History (closed trades)                       │
│  • Orders (pending)                              │
└──────────────────────────────────────────────────┘
```

---

## 🔍 How Rules Are Checked

### Every Loop Iteration (default: 1 second):

1. **Fetch Data** from MT5
   - Current balance & equity
   - All open positions
   - Today's closed trades

2. **Check New Day**
   - Is it a new calendar day?
   - If yes: reset daily_starting_balance

3. **Update Trading Days**
   - Did we close trades today?
   - If yes: add today to trading_days set

4. **Update Peak** (for trailing drawdown)
   - Is current equity > peak?
   - If yes: update peak_balance

5. **Check Daily Loss**
   - daily_loss = daily_starting_balance - current_equity
   - Is daily_loss > max_daily_loss?
   - If yes: VIOLATION

6. **Check Total Drawdown**
   - Static: total_dd = starting_balance - current_equity
   - Trailing: total_dd = peak_balance - current_equity
   - Is total_dd > max_total_drawdown?
   - If yes: VIOLATION

7. **Check Lot Limits** (if configured)
   - Any position > max_lot_per_trade?
   - Total open lots > max_total_lots?
   - If yes: VIOLATION

8. **Check Time Limit**
   - days_elapsed > challenge_days_limit?
   - If yes: VIOLATION

9. **Check Profit Target**
   - profit >= profit_target?
   - trading_days >= min_trading_days?
   - If both yes: PASSED!

10. **Print Status** (every 60 seconds)
    - Current metrics
    - Rule status
    - Progress toward goal

---

## 🎛️ Configuration Options

### Via CONFIG in main.py:
```python
CONFIG = {
    'firm_key': 'funded_next_6k',      # Which firm profile to use
    'starting_balance': 6000.0,        # Your account starting balance
    'magic_filter': None,              # Only track EA with this magic (or None)
    'auto_close_on_breach': False,     # Close positions on violation
    'poll_interval': 1.0,              # Seconds between checks
    'log_level': 'INFO',               # DEBUG, INFO, WARNING, ERROR
}
```

### Via Command Line:
```bash
python main.py --firm ftmo_10k         # Override firm
python main.py --balance 10000         # Override balance
python main.py --magic 12345           # Override magic filter
python main.py --auto-close            # Enable auto-close
python main.py --interval 0.5          # Override check interval
python main.py --log-level DEBUG       # Override log level
```

---

## 📝 Log Files

Location: `logs/prop_monitor_YYYYMMDD_HHMMSS.log`

Contains:
- Timestamp for every event
- Connection status
- Account state changes
- Rule check results
- Violations
- Position closes
- Status reports

Example log entries:
```
2026-03-06 10:30:15 | INFO | Connected to MT5 - Account: 12345678
2026-03-06 10:30:15 | INFO | Rule Engine Initialized - FundedNext Express 6K
2026-03-06 10:30:15 | INFO | Starting Balance: $6000.00
2026-03-06 10:30:20 | DEBUG | [Check #5] Balance: $6050.00 | Equity: $6080.00
2026-03-06 10:31:15 | INFO | New trading day detected: 2026-03-06
2026-03-06 10:35:30 | ERROR | DAILY LOSS BREACH: $350.00 > $300.00
```

---

## 🛡️ Safety Features

1. **Read-Only by Default**
   - Only monitors, doesn't trade
   - Optional auto-close feature (use with caution)

2. **Error Handling**
   - All exceptions caught and logged
   - Graceful retry on connection issues
   - Safe shutdown on Ctrl+C

3. **Logging**
   - Everything logged to file
   - Console output for real-time monitoring
   - Debug mode available

4. **Validation**
   - Firm profile validation
   - MT5 connection checks
   - Account state verification

---

## 🔧 Customization Examples

### Add Your Own Firm

Edit `firms/firm_profiles.py`:
```python
'my_firm_20k': {
    'name': 'My Prop Firm 20K',
    'max_daily_loss_percent': 5.0,
    'max_total_drawdown_percent': 10.0,
    'profit_target_percent': 12.0,
    'min_trading_days': 3,
    'challenge_days_limit': 30,
    'drawdown_type': 'static',
    'max_lot_per_trade': None,
    'max_total_lots': None,
},
```

### Modify Check Interval

For faster checks (high-frequency trading):
```bash
python main.py --interval 0.1  # Check every 100ms
```

For slower checks (position trading):
```bash
python main.py --interval 5.0  # Check every 5 seconds
```

---

## 📚 File Reference

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | Entry point, CLI, monitoring loop | 259 |
| `core/mt5_connector.py` | MT5 API wrapper | 268 |
| `core/prop_rule_engine.py` | Rule checking logic | 252 |
| `firms/firm_profiles.py` | Firm configurations | 239 |
| `README.md` | Full documentation | 150+ |
| `QUICKSTART.md` | Quick start guide | 150+ |
| `IMPLEMENTATION_SUMMARY.md` | Architecture & features | 300+ |
| `EXAMPLES.py` | Code examples | 200+ |

**Total: ~2000 lines of code + documentation**

---

## ✅ Testing Checklist

Before using on a live challenge:

- [ ] Test on demo account first
- [ ] Verify firm profile matches your challenge
- [ ] Confirm starting_balance is correct
- [ ] Check drawdown_type (static vs trailing)
- [ ] Test auto-close feature (if using)
- [ ] Monitor for at least 1 full trading day
- [ ] Verify logs are being created
- [ ] Test Ctrl+C graceful shutdown
- [ ] Confirm status reports are accurate

---

## 🎉 You're Ready!

Your prop firm monitoring system is **complete and ready to use**.

### Next Steps:
1. Install MT5 and login to demo account
2. Run `pip install -r requirements.txt`
3. Configure your firm settings in `main.py`
4. Start monitoring: `python main.py`
5. Watch it work!

### Support:
- Check `README.md` for full documentation
- Check `QUICKSTART.md` for quick start
- Check `EXAMPLES.py` for code examples
- Check `logs/` for detailed activity logs

**Happy trading and good luck with your prop firm challenge! 🚀**


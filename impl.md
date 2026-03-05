# Prop Firm Rule Engine — MT5 + Python

Real-time prop firm challenge rule monitor. Connects to your running
MT5 terminal and enforces firm rules on your live/demo account.

---

## Project Structure

```
prop_firm_simulator/
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
- Python 64-bit


```bash
---

## Running

```bash
# List all supported firms
python main.py --list-firms

# Start monitoring (edit CONFIG in main.py first)
python main.py
```

---

## Configuration (`main.py` → CONFIG block)

| Key | Description |
|---|---|
| `firm_key` | Firm profile key (see `--list-firms`) |
| `magic_filter` | Only monitor trades with this EA magic number |
| `auto_close_on_breach` | Close all positions on rule violation |
| `poll_interval` | Check frequency in seconds (default: 1.0) |

---

## Supported Firms

| Key                      | Firm                   | DD Type |
|--------------------------|------------------------|---|
| `funded_next_6k`         | FundedNext 6k          | Static |

---

## Rules Monitored

1. **Max Daily Loss** — equity must not drop more than X% from day's opening balance
2. **Max Total Drawdown** — equity must not drop more than X% from account size (or peak equity for trailing firms)
3. **Lot Size Limits** — per-trade and total open lots enforced where applicable
4. **Profit Target** — detects when target is hit with enough trading days
5. **Min Trading Days** — tracks distinct days with closed trades
6. **Challenge Expiry** — flags if calendar deadline exceeded

---

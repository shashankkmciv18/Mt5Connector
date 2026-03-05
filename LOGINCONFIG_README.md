# LoginConfig DTO - Complete Guide

## ✅ Implementation Complete!

### What is LoginConfig?

A **Data Transfer Object (DTO)** for MT5 login credentials with validation, serialization, and multiple loading methods.

---

## 📁 Files Created

```
dto/
├── __init__.py              # Package initialization
├── LoginConfig.py           # LoginConfig DTO class
└── (future DTOs here)

LOGINCONFIG_EXAMPLES.py      # Usage examples
```

---

## 🎯 Features

✅ **Dataclass-based** - Clean, typed structure  
✅ **Validation** - Ensures valid login, password, server  
✅ **Password masking** - Secure string representation  
✅ **Multiple loading methods** - Direct, env vars, JSON file  
✅ **Serialization** - to_dict() / from_dict()  
✅ **Type hints** - Full typing support  
✅ **Factory function** - Convenient creation  

---

## 📦 LoginConfig Structure

```python
@dataclass
class LoginConfig:
    login: int              # MT5 account number
    password: str           # Account password
    server: str             # Broker server name
    timeout: int = 60000    # Connection timeout (ms)
```

---

## 🚀 Usage Methods

### Method 1: Direct Creation

```python
from dto.LoginConfig import LoginConfig

config = LoginConfig(
    login=12345678,
    password="MyPassword123",
    server="MetaQuotes-Demo",
    timeout=60000  # optional
)
```

### Method 2: Factory Function

```python
from dto.LoginConfig import create_login_config

config = create_login_config(
    login=12345678,
    password="MyPassword123",
    server="MetaQuotes-Demo"
)
```

### Method 3: Environment Variables ⭐ RECOMMENDED

```bash
# Set environment variables
export MT5_LOGIN=12345678
export MT5_PASSWORD=MyPassword123
export MT5_SERVER=MetaQuotes-Demo
export MT5_TIMEOUT=60000  # optional
```

```python
from dto.LoginConfig import load_from_env

config = load_from_env()  # Returns LoginConfig or None
```

### Method 4: JSON File

Create `config/mt5_login.json`:
```json
{
  "login": 12345678,
  "password": "MyPassword123",
  "server": "MetaQuotes-Demo",
  "timeout": 60000
}
```

```python
from dto.LoginConfig import load_from_file

config = load_from_file('config/mt5_login.json')
```

### Method 5: Save to File

```python
from dto.LoginConfig import save_to_file

config = create_login_config(12345678, "pass", "server")
save_to_file(config, 'config/mt5_login.json')
```

---

## 🔧 Integration with Main.py

### Option A: Direct Configuration

```python
# In main.py CONFIG:
CONFIG = {
    'firm_key': 'funded_next_6k',
    'starting_balance': 6000.0,
    # ... other settings ...
    
    'login_config': LoginConfig(
        login=12345678,
        password="YourPassword",
        server="YourBroker-Server"
    ),
}
```

### Option B: Environment Variables (Best for Security)

```python
CONFIG = {
    # ... other settings ...
    'login_config': load_from_env(),  # Auto-loads from env
}
```

```bash
# Then run:
export MT5_LOGIN=12345678
export MT5_PASSWORD=MyPassword123
export MT5_SERVER=MetaQuotes-Demo
python main.py
```

### Option C: JSON File

```python
CONFIG = {
    # ... other settings ...
    'login_config': load_from_file('config/mt5_login.json'),
}
```

### Option D: No Login (Connect to Running MT5)

```python
CONFIG = {
    # ... other settings ...
    'login_config': None,  # Will connect to already running MT5
}
```

---

## 🏦 Common Broker Servers

| Broker | Server Name |
|--------|-------------|
| MetaQuotes | MetaQuotes-Demo, MetaQuotes-Server |
| Alpari | Alpari-Demo, Alpari-Server |
| XM | XMGlobal-Demo, XMGlobal-Real |
| FTMO | FTMO-Demo, FTMO-Server |
| IC Markets | ICMarketsSC-Demo, ICMarketsSC-Live |
| FundedNext | FundedNext-Demo, FundedNext-Live |

---

## 🔒 Security Best Practices

### ✅ DO:
- Use environment variables for production
- Store JSON config files outside project
- Add `config/*.json` to `.gitignore`
- Use file permissions: `chmod 600 config/mt5_login.json`
- Different configs for demo/live/challenge accounts

### ❌ DON'T:
- Commit passwords to git
- Hardcode passwords in shared code
- Use same password for all accounts
- Store passwords in plain text on shared systems

---

## ✅ Validation

LoginConfig automatically validates:

```python
# ✓ Valid
config = LoginConfig(
    login=12345678,      # Must be positive integer
    password="Pass123",  # Must be non-empty
    server="Server-1",   # Must be non-empty
    timeout=60000        # Must be positive
)

# ✗ Invalid - raises ValueError
LoginConfig(login=-1, password="x", server="x")       # Negative login
LoginConfig(login=123, password="", server="x")       # Empty password
LoginConfig(login=123, password="x", server="")       # Empty server
LoginConfig(login=123, password="x", server="x", timeout=-1)  # Negative timeout
```

---

## 📝 Methods

### Instance Methods

```python
config = LoginConfig(12345678, "pass", "server")

# Convert to dictionary
data = config.to_dict()
# {'login': 12345678, 'password': 'pass', 'server': 'server', 'timeout': 60000}

# String representation (password masked)
print(config)
# LoginConfig(login=12345678, password='***', server='server', timeout=60000)
```

### Class Methods

```python
# Create from dictionary
data = {'login': 12345678, 'password': 'pass', 'server': 'server'}
config = LoginConfig.from_dict(data)
```

### Module Functions

```python
from dto.LoginConfig import (
    create_login_config,  # Factory function
    load_from_env,        # Load from environment
    load_from_file,       # Load from JSON
    save_to_file,         # Save to JSON
)
```

---

## 🧪 Testing

```bash
# Run examples
python LOGINCONFIG_EXAMPLES.py

# Quick test
python -c "from dto.LoginConfig import create_login_config; \
           print(create_login_config(123, 'pass', 'server'))"
```

---

## 📚 Example Files

### Example: .env file

```bash
# .env
MT5_LOGIN=12345678
MT5_PASSWORD=MySecurePassword123
MT5_SERVER=MetaQuotes-Demo
MT5_TIMEOUT=60000
```

### Example: config/mt5_demo.json

```json
{
  "login": 12345678,
  "password": "DemoPassword123",
  "server": "MetaQuotes-Demo",
  "timeout": 60000
}
```

### Example: config/mt5_challenge.json

```json
{
  "login": 98765432,
  "password": "ChallengePassword456",
  "server": "FTMO-Demo",
  "timeout": 60000
}
```

---

## 🔄 How MT5Connector Uses LoginConfig

```python
# In core/mt5_connector.py:

class MT5Connector:
    def __init__(self, login_config: Optional[LoginConfig] = None, ...):
        self.login_config = login_config
    
    def connect(self) -> bool:
        if self.login_config:
            # Login with credentials
            mt5.initialize(
                login=self.login_config.login,
                password=self.login_config.password,
                server=self.login_config.server,
                timeout=self.login_config.timeout
            )
        else:
            # Connect to already running MT5
            mt5.initialize()
```

---

## 🎯 Use Cases

### Use Case 1: Multiple Demo Accounts

```python
demo1 = load_from_file('config/demo1.json')
demo2 = load_from_file('config/demo2.json')
demo3 = load_from_file('config/demo3.json')

# Test on demo1
mt5 = MT5Connector(login_config=demo1)
```

### Use Case 2: Challenge vs Live Account

```python
# During challenge
challenge_config = load_from_file('config/ftmo_challenge.json')

# After passing
live_config = load_from_file('config/ftmo_live.json')
```

### Use Case 3: CI/CD Pipeline

```bash
# In CI/CD, set secrets as env vars
export MT5_LOGIN=${{ secrets.MT5_LOGIN }}
export MT5_PASSWORD=${{ secrets.MT5_PASSWORD }}
export MT5_SERVER=${{ secrets.MT5_SERVER }}

# Code automatically loads from env
python main.py  # Will use load_from_env()
```

---

## 📖 Complete Example

```python
from dto.LoginConfig import LoginConfig, load_from_env, create_login_config
from core.mt5_connector import MT5Connector
from core.prop_rule_engine import PropRuleEngine
from firms.firm_profiles import get_firm_profile

# Method 1: Environment variables
config = load_from_env()

# Method 2: Direct creation
if not config:
    config = create_login_config(
        login=12345678,
        password="MyPassword123",
        server="MetaQuotes-Demo"
    )

# Use with MT5Connector
mt5 = MT5Connector(login_config=config)

if mt5.connect():
    print(f"✓ Connected to MT5: {config}")
    
    # Start monitoring
    account = mt5.get_account_state()
    print(f"Balance: ${account['balance']:.2f}")
    
    mt5.disconnect()
else:
    print("✗ Failed to connect")
```

---

## ✅ Summary

You now have a complete LoginConfig DTO that:
- ✅ Stores MT5 credentials securely
- ✅ Validates all inputs
- ✅ Supports multiple loading methods
- ✅ Integrates with MT5Connector
- ✅ Masks passwords in logs
- ✅ Serializes to/from JSON
- ✅ Works with environment variables

**Next Steps:**
1. Choose your preferred method (env vars recommended)
2. Configure your MT5 credentials
3. Update main.py CONFIG
4. Start monitoring your prop firm challenge!

---

## 📁 Related Files

- `dto/LoginConfig.py` - DTO implementation
- `core/mt5_connector.py` - Uses LoginConfig
- `main.py` - CONFIG integration
- `LOGINCONFIG_EXAMPLES.py` - Usage examples
- `.gitignore` - Add config/*.json

---

**Happy Trading! 🚀**


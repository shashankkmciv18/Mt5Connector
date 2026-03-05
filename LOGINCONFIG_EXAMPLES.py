"""
LoginConfig Usage Examples
How to configure MT5 login credentials for the prop firm monitor
"""
from dto.LoginConfig import LoginConfig, create_login_config, load_from_env, load_from_file, save_to_file
import os


# ==============================================================================
# METHOD 1: Direct Configuration (in main.py CONFIG)
# ==============================================================================

def example1_direct_config():
    """Create LoginConfig directly"""
    config = LoginConfig(
        login=12345678,
        password="MyPassword123",
        server="MetaQuotes-Demo",
        timeout=60000  # optional, default is 60000ms
    )
    print(f"Method 1 - Direct: {config}")
    return config


# ==============================================================================
# METHOD 2: Using Factory Function
# ==============================================================================

def example2_factory():
    """Use factory function for cleaner syntax"""
    config = create_login_config(
        login=12345678,
        password="MyPassword123",
        server="MetaQuotes-Demo"
    )
    print(f"Method 2 - Factory: {config}")
    return config


# ==============================================================================
# METHOD 3: From Environment Variables (RECOMMENDED for security)
# ==============================================================================

def example3_from_env():
    """Load from environment variables"""
    # Set environment variables first:
    # export MT5_LOGIN=12345678
    # export MT5_PASSWORD=MyPassword123
    # export MT5_SERVER=MetaQuotes-Demo

    config = load_from_env()

    if config:
        print(f"Method 3 - Environment: {config}")
        return config
    else:
        print("Method 3 - No environment variables set")
        print("Set MT5_LOGIN, MT5_PASSWORD, MT5_SERVER to use this method")
        return None


# ==============================================================================
# METHOD 4: From JSON File
# ==============================================================================

def example4_from_file():
    """Load from JSON configuration file"""
    # Create a config.json file:
    # {
    #   "login": 12345678,
    #   "password": "MyPassword123",
    #   "server": "MetaQuotes-Demo",
    #   "timeout": 60000
    # }

    try:
        config = load_from_file('config/mt5_login.json')
        print(f"Method 4 - JSON File: {config}")
        return config
    except FileNotFoundError:
        print("Method 4 - File not found: config/mt5_login.json")
        print("Create this file with your credentials")
        return None


# ==============================================================================
# METHOD 5: Save to File for Later Use
# ==============================================================================

def example5_save_to_file():
    """Save configuration to file"""
    config = create_login_config(
        login=12345678,
        password="MyPassword123",
        server="MetaQuotes-Demo"
    )

    # Save to file (create directory if needed)
    os.makedirs('config', exist_ok=True)
    save_to_file(config, 'config/mt5_login.json')
    print("Method 5 - Saved to: config/mt5_login.json")


# ==============================================================================
# INTEGRATION WITH MAIN.PY
# ==============================================================================

def integration_example():
    """How to use in main.py"""

    print("\n" + "="*70)
    print("INTEGRATION WITH MAIN.PY")
    print("="*70)

    print("""
# In main.py, edit the CONFIG section:

CONFIG = {
    'firm_key': 'funded_next_6k',
    'starting_balance': 6000.0,
    'magic_filter': None,
    'auto_close_on_breach': False,
    'poll_interval': 1.0,
    'log_level': 'INFO',
    
    # Option A: Direct configuration
    'login_config': LoginConfig(
        login=12345678,
        password="YourPassword",
        server="YourBroker-Server"
    ),
    
    # Option B: From environment variables (RECOMMENDED)
    'login_config': load_from_env(),
    
    # Option C: From file
    'login_config': load_from_file('config/mt5_login.json'),
    
    # Option D: None (connect to already running MT5)
    'login_config': None,
}
    """)


# ==============================================================================
# COMMON BROKER SERVERS
# ==============================================================================

BROKER_SERVERS = {
    'MetaQuotes': [
        'MetaQuotes-Demo',
        'MetaQuotes-Server',
    ],
    'Alpari': [
        'Alpari-Demo',
        'Alpari-Server',
    ],
    'XM': [
        'XMGlobal-Demo',
        'XMGlobal-Real',
    ],
    'FTMO': [
        'FTMO-Demo',
        'FTMO-Server',
    ],
    'IC Markets': [
        'ICMarketsSC-Demo',
        'ICMarketsSC-Live',
    ],
    'FundedNext': [
        'FundedNext-Demo',
        'FundedNext-Live',
    ],
}


def show_broker_servers():
    """Display common broker servers"""
    print("\n" + "="*70)
    print("COMMON BROKER SERVERS")
    print("="*70)

    for broker, servers in BROKER_SERVERS.items():
        print(f"\n{broker}:")
        for server in servers:
            print(f"  - {server}")


# ==============================================================================
# SECURITY BEST PRACTICES
# ==============================================================================

def show_security_tips():
    """Display security best practices"""
    print("\n" + "="*70)
    print("SECURITY BEST PRACTICES")
    print("="*70)
    print("""
1. NEVER commit passwords to git
   - Add config/*.json to .gitignore
   - Use environment variables instead

2. Use environment variables for production:
   export MT5_LOGIN=12345678
   export MT5_PASSWORD=MyPassword123
   export MT5_SERVER=YourBroker-Server

3. Store sensitive files securely:
   - Use file permissions: chmod 600 config/mt5_login.json
   - Store in secure locations outside project

4. For demo accounts:
   - It's safer to hardcode in main.py
   - But still don't commit to public repos

5. Use different configs for different accounts:
   config/
     ├── mt5_demo.json
     ├── mt5_live.json
     └── mt5_challenge.json
    """)


# ==============================================================================
# VALIDATION EXAMPLES
# ==============================================================================

def example_validation():
    """Show validation in action"""
    print("\n" + "="*70)
    print("VALIDATION EXAMPLES")
    print("="*70)

    # Valid config
    try:
        valid = LoginConfig(
            login=12345678,
            password="ValidPass123",
            server="MetaQuotes-Demo"
        )
        print(f"✓ Valid: {valid}")
    except ValueError as e:
        print(f"✗ Error: {e}")

    # Invalid: negative login
    try:
        invalid = LoginConfig(login=-1, password="test", server="test")
    except ValueError as e:
        print(f"✓ Caught error: {e}")

    # Invalid: empty password
    try:
        invalid = LoginConfig(login=123, password="", server="test")
    except ValueError as e:
        print(f"✓ Caught error: {e}")

    # Invalid: empty server
    try:
        invalid = LoginConfig(login=123, password="test", server="")
    except ValueError as e:
        print(f"✓ Caught error: {e}")


# ==============================================================================
# MAIN DEMO
# ==============================================================================

if __name__ == '__main__':
    print("="*70)
    print("  LOGINCONFIG DTO - USAGE EXAMPLES")
    print("="*70)

    print("\n" + "-"*70)
    print("Creating LoginConfig objects:")
    print("-"*70)

    example1_direct_config()
    example2_factory()
    example3_from_env()

    print("\n" + "-"*70)
    print("Validation:")
    print("-"*70)
    example_validation()

    show_broker_servers()
    integration_example()
    show_security_tips()

    print("\n" + "="*70)
    print("For more examples, see:")
    print("  - dto/LoginConfig.py")
    print("  - main.py (CONFIG section)")
    print("="*70)


"""
Login Configuration DTO
Data Transfer Object for MT5 login credentials
"""
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv



@dataclass
class LoginConfig:
    """
    MT5 Login Configuration

    Attributes:
        login: MT5 account login number
        password: MT5 account password
        server: MT5 broker server name
        timeout: Connection timeout in milliseconds (default: 60000)
    """
    login: int
    password: str
    server: str
    timeout: int = 60000

    def __post_init__(self):
        """Validate login configuration"""
        if not isinstance(self.login, int) or self.login <= 0:
            raise ValueError("Login must be a positive integer")

        if not self.password:
            raise ValueError("Password cannot be empty")

        if not self.server:
            raise ValueError("Server cannot be empty")

        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'login': self.login,
            'password': self.password,
            'server': self.server,
            'timeout': self.timeout
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'LoginConfig':
        """Create LoginConfig from dictionary"""
        return cls(
            login=data['login'],
            password=data['password'],
            server=data['server'],
            timeout=data.get('timeout', 60000)
        )

    def __repr__(self) -> str:
        """String representation (password masked)"""
        return f"LoginConfig(login={self.login}, password='***', server='{self.server}', timeout={self.timeout})"


# Example usage and helper functions
def create_login_config(login: int, password: str, server: str, timeout: int = 60000) -> LoginConfig:
    """
    Factory function to create LoginConfig

    Args:
        login: MT5 account number
        password: Account password
        server: Broker server name
        timeout: Connection timeout in ms

    Returns:
        LoginConfig instance

    Example:
        >>> config = create_login_config(732600, "123456789aA!", "BlackBullMarkets-Demo")
        >>> print(config)
        LoginConfig(login=12345678, password='***', server='MetaQuotes-Demo', timeout=60000)
    """
    return LoginConfig(login=login, password=password, server=server, timeout=timeout)


def load_from_env() -> Optional[LoginConfig]:
    """
    Load login config from environment variables

    Environment variables:
        MT5_LOGIN: Account login number
        MT5_PASSWORD: Account password
        MT5_SERVER: Broker server name
        MT5_TIMEOUT: Connection timeout (optional, default 60000)

    Returns:
        LoginConfig if all required env vars are set, None otherwise
    """


    import os
    load_dotenv()  # loads variables from .env in project root login = os.getenv("MT5_LOGIN")

    login = os.getenv('MT5_LOGIN')
    password = os.getenv('MT5_PASSWORD')
    server = os.getenv('MT5_SERVER')
    timeout = int(os.getenv('MT5_TIMEOUT', '60000'))

    if login and password and server:
        return LoginConfig(
            login=int(login),
            password=password,
            server=server,
            timeout=timeout
        )

    return None


def load_from_file(filepath: str) -> LoginConfig:
    """
    Load login config from JSON file

    Args:
        filepath: Path to JSON config file

    Returns:
        LoginConfig instance

    Example JSON file:
        {
            "login": 12345678,
            "password": "MyPassword123",
            "server": "MetaQuotes-Demo",
            "timeout": 60000
        }
    """
    import json

    with open(filepath, 'r') as f:
        data = json.load(f)

    return LoginConfig.from_dict(data)


def save_to_file(config: LoginConfig, filepath: str):
    """
    Save login config to JSON file

    Args:
        config: LoginConfig instance
        filepath: Path to save JSON file
    """
    import json

    with open(filepath, 'w') as f:
        json.dump(config.to_dict(), f, indent=2)


# Example configurations (replace with your actual credentials)
def get_demo_config(broker: str = 'metaquotes') -> LoginConfig:
    """
    Get a demo config template (you must fill in actual credentials)

    Args:
        broker: Broker name ('metaquotes', 'alpari', 'xm')

    Returns:
        LoginConfig template (with invalid credentials - must be replaced)
    """
    configs = {
        'metaquotes': ('MetaQuotes-Demo', 'Demo account from MetaTrader'),
        'alpari': ('Alpari-Demo', 'Alpari demo server'),
        'xm': ('XMGlobal-Demo', 'XM Global demo server'),
    }

    server, description = configs.get(broker, ('MetaQuotes-Demo', 'Default demo'))

    print(f"⚠️  Template for {description}")
    print(f"   Server: {server}")
    print(f"   You must replace login and password with your actual credentials")

    # Return with placeholder values that will fail validation if used
    return LoginConfig(
        login=99999999,  # Replace with your actual login
        password="YOUR_PASSWORD_HERE",  # Replace with your password
        server=server
    )


if __name__ == '__main__':
    # Example usage
    print("=== LoginConfig DTO Examples ===\n")

    # Create config
    config = create_login_config(
        login=12345678,
        password="MySecurePassword123",
        server="MetaQuotes-Demo"
    )
    print(f"1. Created: {config}\n")

    # Convert to dict
    print(f"2. As dict: {config.to_dict()}\n")

    # Load from environment (if set)
    env_config = load_from_env()
    if env_config:
        print(f"3. From env: {env_config}\n")
    else:
        print("3. No env variables set (MT5_LOGIN, MT5_PASSWORD, MT5_SERVER)\n")

    # Example of validation
    try:
        invalid = LoginConfig(login=-1, password="test", server="test")
    except ValueError as e:
        print(f"4. Validation works: {e}\n")


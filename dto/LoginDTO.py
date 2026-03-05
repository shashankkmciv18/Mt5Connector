"""
Login Configuration DTO
Data Transfer Object for MT5 login credentials
"""
from dataclasses import dataclass
from typing import Optional


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
        >>> config = create_login_config(12345678, "MyPassword123", "MetaQuotes-Demo")
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


# Example configurations
DEMO_CONFIGS = {
    'metaquotes_demo': LoginConfig(
        login=0,  # Replace with your login
        password="",  # Replace with your password
        server="MetaQuotes-Demo"
    ),
    'alpari_demo': LoginConfig(
        login=0,
        password="",
        server="Alpari-Demo"
    ),
    'xm_demo': LoginConfig(
        login=0,
        password="",
        server="XMGlobal-Demo"
    ),
}

if __name__ == '__main__':
    # Example usage
    print("=== LoginConfig DTO Examples ===\n")

    # Create config
    config = load_from_env()
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


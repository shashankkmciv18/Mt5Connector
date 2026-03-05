"""
Prop Firm Profiles - Configuration for different prop firms
"""

# Firm profile template:
# {
#     'name': str,                           # Firm display name
#     'max_daily_loss_percent': float,       # Max daily loss as % of starting balance
#     'max_total_drawdown_percent': float,   # Max total drawdown as %
#     'profit_target_percent': float,        # Profit target as %
#     'min_trading_days': int,               # Minimum days with closed trades
#     'challenge_days_limit': int,           # Max calendar days for challenge
#     'drawdown_type': str,                  # 'static' or 'trailing'
#     'max_lot_per_trade': float or None,    # Max lots per single position
#     'max_total_lots': float or None,       # Max total open lots
# }

FIRM_PROFILES = {
    # ============================================================================
    # FundedNext
    # ============================================================================
    'funded_next_6k': {
        'name': 'FundedNext Express 6K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 10.0,
        'min_trading_days': 0,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'funded_next_15k': {
        'name': 'FundedNext Express 15K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 10.0,
        'min_trading_days': 0,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'funded_next_25k': {
        'name': 'FundedNext Express 25K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 10.0,
        'min_trading_days': 0,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    # ============================================================================
    # FTMO
    # ============================================================================
    'ftmo_10k': {
        'name': 'FTMO 10K Challenge',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 10.0,
        'min_trading_days': 4,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'ftmo_25k': {
        'name': 'FTMO 25K Challenge',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 10.0,
        'min_trading_days': 4,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'ftmo_50k': {
        'name': 'FTMO 50K Challenge',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 10.0,
        'min_trading_days': 4,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'ftmo_100k': {
        'name': 'FTMO 100K Challenge',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 10.0,
        'min_trading_days': 4,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    # ============================================================================
    # The Funded Trader (TFT)
    # ============================================================================
    'tft_50k': {
        'name': 'The Funded Trader 50K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 8.0,
        'profit_target_percent': 8.0,
        'min_trading_days': 5,
        'challenge_days_limit': 60,
        'drawdown_type': 'trailing',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'tft_100k': {
        'name': 'The Funded Trader 100K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 8.0,
        'profit_target_percent': 8.0,
        'min_trading_days': 5,
        'challenge_days_limit': 60,
        'drawdown_type': 'trailing',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    # ============================================================================
    # E8 Funding
    # ============================================================================
    'e8_25k': {
        'name': 'E8 Funding 25K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 8.0,
        'profit_target_percent': 8.0,
        'min_trading_days': 0,
        'challenge_days_limit': 30,
        'drawdown_type': 'trailing',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'e8_50k': {
        'name': 'E8 Funding 50K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 8.0,
        'profit_target_percent': 8.0,
        'min_trading_days': 0,
        'challenge_days_limit': 30,
        'drawdown_type': 'trailing',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'e8_100k': {
        'name': 'E8 Funding 100K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 8.0,
        'profit_target_percent': 8.0,
        'min_trading_days': 0,
        'challenge_days_limit': 30,
        'drawdown_type': 'trailing',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    # ============================================================================
    # MyFundedFX
    # ============================================================================
    'myfundedfx_10k': {
        'name': 'MyFundedFX 10K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 8.0,
        'min_trading_days': 3,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },

    'myfundedfx_25k': {
        'name': 'MyFundedFX 25K',
        'max_daily_loss_percent': 5.0,
        'max_total_drawdown_percent': 10.0,
        'profit_target_percent': 8.0,
        'min_trading_days': 3,
        'challenge_days_limit': 30,
        'drawdown_type': 'static',
        'max_lot_per_trade': None,
        'max_total_lots': None,
    },
}


def get_firm_profile(firm_key: str) -> dict:
    """
    Get firm profile by key

    Args:
        firm_key: Firm profile key

    Returns:
        Firm profile dictionary

    Raises:
        KeyError if firm not found
    """
    if firm_key not in FIRM_PROFILES:
        raise KeyError(f"Firm '{firm_key}' not found. Use --list-firms to see available firms.")

    return FIRM_PROFILES[firm_key]


def list_all_firms():
    """Print all available firm profiles"""
    print("\n" + "="*80)
    print("  Available Prop Firm Profiles")
    print("="*80)
    print(f"{'Key':<25} {'Firm Name':<35} {'DD Type':<10}")
    print("-"*80)

    for key, profile in sorted(FIRM_PROFILES.items()):
        dd_type = profile['drawdown_type'].capitalize()
        print(f"{key:<25} {profile['name']:<35} {dd_type:<10}")

    print("="*80)
    print(f"Total: {len(FIRM_PROFILES)} firm profiles")
    print("="*80 + "\n")


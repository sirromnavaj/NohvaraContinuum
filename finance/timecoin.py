import json

class TimeCoinSystem:
    """Handles NohvaraContinuum's Coin System, contributions, and conversions."""

    def __init__(self):
        self.coins = 0

    def earn_coins(self, amount):
        self.coins += amount

    def spend_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
        else:
            print("Not enough coins!")

    def get_balance(self):
        return self.coins
    def __init__(self, coin_file="finance_config.json"):
        self.coin_file = coin_file
        self.coins = self.load_coins()

    def load_coins(self):
        """Loads coin balances from file."""
        try:
            with open(self.coin_file, "r") as f:
                return json.load(f).get("coins", {
                    "time_coin": 0,
                    "k_coin": 0,
                    "mortal_coin": 0,
                    "divine_coin": 0,
                    "divine_king_coin": 0
                })
        except FileNotFoundError:
            return {"time_coin": 0, "k_coin": 0, "mortal_coin": 0, "divine_coin": 0, "divine_king_coin": 0}

    def save_coins(self):
        """Saves updated coin balances."""
        with open(self.coin_file, "w") as f:
            json.dump({"coins": self.coins}, f, indent=4)

    def earn_coin(self, coin_type, amount):
        """Earns coins and enforces 2x contribution rule."""
        if coin_type in self.coins:
            self.coins[coin_type] += amount
            contribution = amount * 2  # 2x contribution rule
            self.contribute_to_reserves(contribution)
            self.save_coins()
            return f"✅ Earned {amount} {coin_type}. Contributed {contribution} to reserves."
        return "⚠️ Invalid coin type."

    def contribute_to_reserves(self, amount):
        """Allocates contributions to system reserves."""
        reserve_system = ReserveManager()
        reserve_system.add_to_reserve(amount)

    def convert_coin_to_cash(self, coin_type, amount):
        """Converts coins to cash while enforcing taxation & reserve rules."""
        reserve_system = ReserveManager()
        
        if self.coins[coin_type] < amount:
            return "⚠️ Not enough coins for conversion."
        
        # Enforce reserve requirement (2x coin amount must be in reserves)
        required_reserve = amount * 2
        if reserve_system.get_reserve_balance() < required_reserve:
            return "⚠️ Reserve balance too low for conversion."

        # Apply 5% tax
        tax = amount * 0.05
        net_cash = amount - tax

        # Deduct from coin balance
        self.coins[coin_type] -= amount
        self.save_coins()

        # Deduct tax from reserves
        reserve_system.deduct_from_reserve(tax)

        return f"✅ Converted {amount} {coin_type} to cash. Tax deducted: {tax}. Net received: {net_cash} Ksh."

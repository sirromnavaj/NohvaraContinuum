import json

class ReserveManager:
    """Manages system reserves and taxation policies."""

    def __init__(self):
        self.reserves = 0

    def contribute_to_reserve(self, amount):
        self.reserves += amount

    def get_reserve_balance(self):
        return self.reserves
    def __init__(self, reserve_file="finance_config.json"):
        self.reserve_file = reserve_file
        self.reserves = self.load_reserves()

    def load_reserves(self):
        """Loads reserve balance from file."""
        try:
            with open(self.reserve_file, "r") as f:
                return json.load(f).get("reserves", 0)
        except FileNotFoundError:
            return 0

    def save_reserves(self):
        """Saves updated reserve balance."""
        with open(self.reserve_file, "w") as f:
            json.dump({"reserves": self.reserves}, f, indent=4)

    def add_to_reserve(self, amount):
        """Adds funds to reserves."""
        self.reserves += amount
        self.save_reserves()
        return f"✅ Added {amount} Ksh to system reserves. New balance: {self.reserves} Ksh."

    def deduct_from_reserve(self, amount):
        """Deducts tax from reserves."""
        if self.reserves < amount:
            return "⚠️ Insufficient reserve balance."
        
        self.reserves -= amount
        self.save_reserves()
        return f"✅ Deducted {amount} Ksh from reserves for tax purposes."
    
    def get_reserve_balance(self):
        """Returns current reserve balance."""
        return self.reserves

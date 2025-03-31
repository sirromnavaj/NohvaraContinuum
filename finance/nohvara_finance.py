import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from timecoin import TimeCoinSystem
from reserves import ReserveManager
from mpesa_parser import MPESAParser
from ai_finance import AIFinance

class NohvaraFinance:
    """Integrates AI-driven finance management, Time Coin, and reserves."""

    def __init__(self):
        self.reserves = ReserveManager()
        self.coin_system = TimeCoinSystem()

    def process_transaction(self, transaction):
        # Convert transaction amount to TimeCoins
        timecoins = int(transaction['amount']) / 100  
        self.coin_system.earn_coins(timecoins)

        # Apply tax & reserve contributions (example: 10% tax)
        tax = timecoins * 0.10
        self.reserves.contribute_to_reserve(tax)

        return f"Processed transaction: {transaction}, Tax: {tax}, Reserves: {self.reserves.get_reserve_balance()}"
    def __init__(self):
        self.parser = TransactionParser()
        self.timecoin = TimeCoinSystem()
        self.reserves = ReserveManager()
        self.ai_finance = AIFinance()

    def sync_transaction(self, message):
        """Processes transaction messages and updates the system."""
        txn_data = self.parser.extract_transaction(message)
        if txn_data:
            self.timecoin.earn_coin("time_coin", txn_data["amount"])
            self.reserves.add_to_reserve(txn_data["amount"] * 0.2)  # 20% reserve allocation
            self.ai_finance.update_spending_patterns(txn_data)
            return f"✅ Synced {txn_data['amount']} Ksh from {txn_data['source']} ({txn_data['type']})."
        return "⚠️ No valid transaction detected."

    def run_financial_protocols(self):
        """Runs full financial management system."""
        return {
            "Reserves": self.reserves.get_reserve_balance(),
            "Coin Status": self.timecoin.load_coins(),
            "AI Spending Prediction": self.ai_finance.predict_future_expenses(),
        }

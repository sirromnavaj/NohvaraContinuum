import json

class AIFinance:
    """Self-learning AI for financial transactions, spending analysis, and forecasting."""

    def __init__(self):
        self.transaction_history = []

    def learn_from_data(self, transaction):
        self.transaction_history.append(transaction)
        with open("finance_data.json", "w") as f:
            json.dump(self.transaction_history, f)

    def suggest_budget(self):
        # Analyze transaction history & suggest better spending habits
        return "Reduce spending on entertainment by 20%."
    def __init__(self, finance_file="finance_config.json"):
        self.finance_file = finance_file
        self.data = self.load_data()

    def load_data(self):
        """Loads financial data and learning models."""
        try:
            with open(self.finance_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"transactions": [], "spending_patterns": {}}

    def save_data(self):
        """Saves updated financial data."""
        with open(self.finance_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def update_spending_patterns(self, transaction):
        """Learns spending habits and updates budget recommendations."""
        txn_type = transaction["type"]
        if txn_type not in self.data["spending_patterns"]:
            self.data["spending_patterns"][txn_type] = 0
        self.data["spending_patterns"][txn_type] += transaction["amount"]
        self.save_data()

    def predict_future_expenses(self):
        """Forecasts future expenses based on past spending trends."""
        total_spent = sum(self.data["spending_patterns"].values())
        avg_expense = total_spent / max(len(self.data["spending_patterns"]), 1)
        return f"📊 Predicted monthly spending: {avg_expense:.2f} Ksh."

    def auto_learn_transaction_patterns(self, transaction):
        """Learns new transaction types and updates itself."""
        if transaction["type"] == "Unknown":
            new_type = input(f"New transaction detected: {transaction['amount']} Ksh. Enter category: ")
            self.data["spending_patterns"][new_type] = self.data["spending_patterns"].get(new_type, 0) + transaction["amount"]
            self.save_data()

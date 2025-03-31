import re

class TransactionParser:
    """Extracts financial transactions from any source (SMS, email, notifications)."""

    def __init__(self):
        # Patterns for detecting transaction amounts and categories
        self.transaction_patterns = [
            r"Ksh (\d+,\d+|\d+)",   # MPESA, Bank SMS (Kenya)
            r"\$(\d+\.\d+)",        # USD Transactions
            r"€(\d+,\d+|\d+)",      # Euro Transactions
            r"₹(\d+,\d+|\d+)",      # Indian Rupees
        ]

    def extract_transaction(self, message):
        """Parses financial messages to extract amount and type."""
        amount = None
        for pattern in self.transaction_patterns:
            match = re.search(pattern, message)
            if match:
                amount = float(match.group(1).replace(",", ""))  # Convert to number
                break

        if amount:
            txn_type = self.classify_transaction(message)
            return {"amount": amount, "type": txn_type, "source": self.detect_source(message)}

        return None

    def classify_transaction(self, message):
        """Classifies transactions as Income, Expense, Transfer, or Investment."""
        if any(word in message.lower() for word in ["received", "credited", "deposit"]):
            return "Income"
        elif any(word in message.lower() for word in ["paid", "debited", "purchase"]):
            return "Expense"
        elif any(word in message.lower() for word in ["transfer", "sent to", "sent from"]):
            return "Transfer"
        elif any(word in message.lower() for word in ["investment", "bought shares"]):
            return "Investment"
        else:
            return "Unknown"

    def detect_source(self, message):
        """Identifies the source of the transaction (MPESA, Bank, PayPal, etc.)."""
        if "MPESA" in message or "M-PESA" in message:
            return "MPESA"
        elif "BANK" in message or "DEPOSIT" in message:
            return "Bank"
        elif "PAYPAL" in message:
            return "PayPal"
        elif "CREDIT CARD" in message or "VISA" in message or "MASTERCARD" in message:
            return "Credit Card"
        else:
            return "Other"

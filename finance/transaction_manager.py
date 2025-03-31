from mpesa_parser import MPESAParser
from bank_parser import BankParser
# Add other parsers (PayPal, etc.)

class TransactionManager:
    def __init__(self, message):
        self.message = message

    def detect_source(self):
        if "MPESA" in self.message:
            return MPESAParser(self.message).parse()
        elif "Deposit" in self.message:
            return BankParser(self.message).parse()
        # Add more sources as needed
        return None

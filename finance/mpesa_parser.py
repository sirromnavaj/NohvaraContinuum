import json
import subprocess
import re

class MPESAParser:
    def __init__(self):
        self.pattern = re.compile(r"M-PESA\s+(.*)")  # Basic MPESA transaction pattern

    def get_mpesa_messages(self, count=10):
        """Fetches the latest MPESA messages using Termux API."""
        try:
            result = subprocess.run(
                ["termux-sms-list", "-l", str(count)],
                capture_output=True,
                text=True,
                check=True
            )
            messages = json.loads(result.stdout) if result.stdout else []
            return [msg["body"] for msg in messages if "M-PESA" in msg["body"]]
        except subprocess.CalledProcessError as e:
            print(f"❌ Error fetching SMS: {e}")
            return []

    def extract_transaction(self, msg):
        """Extracts transaction details from an MPESA SMS message."""
        match = self.pattern.search(msg)
        return match.group(1) if match else None

    def process_sms(self, count=10):
        """Processes SMS messages to extract MPESA transactions."""
        sms_messages = self.get_mpesa_messages(count)
        transactions = [self.extract_transaction(msg) for msg in sms_messages if self.extract_transaction(msg)]
        return transactions

if __name__ == "__main__":
    parser = MPESAParser()
    transactions = parser.process_sms()

    if transactions:
        print("✅ Parsed Transactions:")
        for txn in transactions:
            print(txn)
    else:
        print("❌ No valid MPESA transactions found.")

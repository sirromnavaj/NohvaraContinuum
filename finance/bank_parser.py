import re

class BankParser:
    def __init__(self, message):
        self.message = message

    def parse(self):
        # Example pattern: "Deposit: KSH 10,000 from ACC: 123456"
        match = re.search(r'Deposit: KSH (\d+,\d+) from ACC: (\d+)', self.message)
        if match:
            return {
                'type': 'deposit',
                'amount': match.group(1).replace(',', ''),
                'account': match.group(2)
            }
        return None

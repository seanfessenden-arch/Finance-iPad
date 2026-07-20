# services.py
from logger_config import ManagedLogger

class PaymentService:
    # This now safely evaluates because ManagedLogger class definition is complete
    @ManagedLogger.log
    def charge_customer(self, amount):
        print(f"Processing payment of ${amount}")
        return True

class UserService:
    @ManagedLogger.log
    def create_user(self, username):
        print(f"Creating user profile for {username}")
        return True


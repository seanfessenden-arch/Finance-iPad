#!/bin/python3
from logger_config import ManagedLogger
from services import PaymentService, UserService

def main():
    # Initialize the underlying logger system once at the start of your app
    ManagedLogger.init_logger(log_file="app.log")

    payment = PaymentService()
    user = UserService()

    print("--- Testing with logs ON ---")
    payment.charge_customer(100)
    user.create_user("alice")

    print("\n--- Testing with logs OFF ---")
    ManagedLogger.disable()
    payment.charge_customer(250)
    user.create_user("bob")

    print("\n--- Testing with logs ON AGAIN ---")
    ManagedLogger.enable()
    payment.charge_customer(500)

if __name__ == "__main__":
    main()


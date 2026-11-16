"""
Tier 2: Field Exercise - Algorithm Thinking (The ATM)

Demonstrates how to break down a high-level problem ("Withdraw money from an ATM")
into a resilient, step-by-step algorithm that handles normal paths and all failure states.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class BankAccount:
    account_number: str
    card_id: str
    pin: str
    balance: float
    daily_limit: float
    is_blocked: bool = False


class ATMTransactionError(Exception):
    pass


class ATM:
    def __init__(self, cash_available: float = 10000.0, bill_denomination: int = 20):
        self.cash_available = cash_available
        self.bill_denomination = bill_denomination
        self.inserted_card: Optional[str] = None
        self.authenticated_account: Optional[BankAccount] = None
        self.failed_pin_attempts: int = 0
        self.max_pin_attempts: int = 3
        self.card_retained: bool = False

    def insert_card(self, card_id: Optional[str]) -> Tuple[bool, str]:
        """Step 1 & 2: Insert card and verify readability."""
        if not card_id or len(card_id.strip()) == 0:
            return False, "Error: Card cannot be read. Please take your card."
        self.inserted_card = card_id
        self.failed_pin_attempts = 0
        self.authenticated_account = None
        self.card_retained = False
        return True, "Card accepted. Please enter your PIN."

    def validate_pin(self, entered_pin: str, account: BankAccount) -> Tuple[bool, str]:
        """Step 3: Authenticate PIN with retry counter and confiscation."""
        if not self.inserted_card:
            return False, "Error: No card inserted."
        if self.card_retained:
            return False, "Error: Card has been retained. Contact bank."
        if account.is_blocked:
            self.card_retained = True
            return False, "Error: Account is blocked. Card retained."

        if entered_pin == account.pin:
            self.authenticated_account = account
            self.failed_pin_attempts = 0
            return True, "PIN validated successfully. Please select a transaction."
        else:
            self.failed_pin_attempts += 1
            remaining = self.max_pin_attempts - self.failed_pin_attempts
            if remaining <= 0:
                self.card_retained = True
                account.is_blocked = True
                return False, "Error: 3 incorrect PIN attempts. Card retained for security."
            return False, f"Incorrect PIN. {remaining} attempt(s) remaining."

    def withdraw_cash(self, amount: float) -> Tuple[bool, str, float]:
        """
        Steps 4 to 9: Validate amount, verify balance, verify ATM cash,
        perform atomic update, and dispense cash.
        Returns: (success_boolean, message, dispensed_cash_amount)
        """
        if not self.authenticated_account:
            return False, "Error: No authenticated session.", 0.0

        # Step 5: Check denomination
        if amount <= 0 or amount % self.bill_denomination != 0:
            return (
                False,
                f"Error: Withdrawal amount must be a positive multiple of ${self.bill_denomination}.",
                0.0,
            )

        # Step 6a: Check daily limit
        if amount > self.authenticated_account.daily_limit:
            return (
                False,
                f"Error: Requested amount exceeds daily limit of ${self.authenticated_account.daily_limit:.2f}.",
                0.0,
            )

        # Step 6b: Check account balance
        if amount > self.authenticated_account.balance:
            return (
                False,
                f"Error: Insufficient funds. Available balance: ${self.authenticated_account.balance:.2f}.",
                0.0,
            )

        # Step 7: Check ATM internal cash
        if amount > self.cash_available:
            return (
                False,
                "Error: This ATM does not have sufficient cash. Transaction cancelled.",
                0.0,
            )

        # Step 8 & 9: Atomic transaction execution
        # Both the account balance and ATM cash reserve update simultaneously.
        self.authenticated_account.balance -= amount
        self.cash_available -= amount

        return (
            True,
            f"Success: Dispensed ${amount:.2f}. New account balance: ${self.authenticated_account.balance:.2f}.",
            amount,
        )

    def return_card(self) -> str:
        """Step 10: Eject card and clean up session."""
        if self.card_retained:
            self.inserted_card = None
            self.authenticated_account = None
            return "Card was retained by machine."
        if self.inserted_card:
            card = self.inserted_card
            self.inserted_card = None
            self.authenticated_account = None
            return f"Card {card} safely ejected. Please remember to take your card."
        return "No card present."


if __name__ == "__main__":
    atm = ATM(cash_available=500.0)
    account = BankAccount(
        account_number="ACC-1001",
        card_id="CARD-8832",
        pin="1234",
        balance=300.0,
        daily_limit=500.0
    )

    print("--- Scenario 1: Unreadable Card ---")
    ok, msg = atm.insert_card("")
    print(f"Status: {ok} | {msg}")

    print("\n--- Scenario 2: Incorrect PIN with lock ---")
    atm.insert_card("CARD-8832")
    for attempt in range(3):
        ok, msg = atm.validate_pin("9999", account)
        print(f"Attempt {attempt+1}: {msg}")

    print("\n--- Scenario 3: Successful Withdrawal ---")
    account.is_blocked = False  # Reset for demo
    atm = ATM(cash_available=500.0)
    atm.insert_card("CARD-8832")
    ok, msg = atm.validate_pin("1234", account)
    print(msg)
    ok, msg, dispensed = atm.withdraw_cash(100.0)
    print(msg)
    print(atm.return_card())

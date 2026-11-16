"""
Unit tests for Py-Section 1 Mission Project — The Digital Translator
"""

import unittest
from src.tier1_literal_assistant import LiteralAssistant, AmbiguousInstructionError
from src.tier2_atm import ATM, BankAccount
from src.tier3_calculator import SimpleCalculator
from src.tier4_data_translator import DataTranslator
from src.tier5_online_store import OnlineStoreDatabase, OnlineStoreApplication


class TestDigitalTranslator(unittest.TestCase):

    # Tier 1 Tests
    def test_tier1_vague_command_raises(self):
        assistant = LiteralAssistant()
        with self.assertRaises(AmbiguousInstructionError):
            assistant.execute_vague_command("Make me breakfast")

    def test_tier1_explicit_program_succeeds(self):
        assistant = LiteralAssistant()
        state = assistant.execute_explicit_program({
            "egg_count": 2,
            "bread_slices": 1,
            "burner_setting": 5,
            "serving_location": "Kitchen Table"
        })
        self.assertTrue(state.task_completed)
        self.assertEqual(state.burner_setting, 0)
        self.assertEqual(state.served_location, "Kitchen Table")

    # Tier 2 Tests
    def test_tier2_atm_card_unreadable(self):
        atm = ATM()
        ok, msg = atm.insert_card("")
        self.assertFalse(ok)
        self.assertIn("cannot be read", msg)

    def test_tier2_atm_pin_attempts_and_lock(self):
        atm = ATM()
        acct = BankAccount("A1", "C1", "1234", 500.0, 500.0)
        atm.insert_card("C1")
        atm.validate_pin("0000", acct)
        atm.validate_pin("0000", acct)
        ok, msg = atm.validate_pin("0000", acct)
        self.assertFalse(ok)
        self.assertTrue(atm.card_retained)
        self.assertTrue(acct.is_blocked)

    def test_tier2_atm_insufficient_funds(self):
        atm = ATM()
        acct = BankAccount("A1", "C1", "1234", 50.0, 500.0)
        atm.insert_card("C1")
        atm.validate_pin("1234", acct)
        ok, msg, dispensed = atm.withdraw_cash(100.0)
        self.assertFalse(ok)
        self.assertEqual(dispensed, 0.0)

    def test_tier2_atm_successful_withdrawal(self):
        atm = ATM(cash_available=1000.0)
        acct = BankAccount("A1", "C1", "1234", 500.0, 500.0)
        atm.insert_card("C1")
        atm.validate_pin("1234", acct)
        ok, msg, dispensed = atm.withdraw_cash(100.0)
        self.assertTrue(ok)
        self.assertEqual(dispensed, 100.0)
        self.assertEqual(acct.balance, 400.0)
        self.assertEqual(atm.cash_available, 900.0)

    # Tier 3 Tests
    def test_tier3_calculator_operations(self):
        calc = SimpleCalculator()
        self.assertEqual(calc.add(20, 5).output, 25)
        self.assertEqual(calc.subtract(20, 5).output, 15)
        self.assertEqual(calc.multiply(20, 5).output, 100)
        self.assertEqual(calc.divide(20, 5).output, 4.0)

    def test_tier3_division_by_zero_defensive(self):
        calc = SimpleCalculator()
        res = calc.divide(20, 0)
        self.assertFalse(res.is_success)
        self.assertIn("undefined", str(res.output))

    # Tier 4 Tests
    def test_tier4_data_translation(self):
        translator = DataTranslator()
        data = translator.inspect_customer_data("Victor", 30, 150000.50, True)
        self.assertEqual(data["name"]["value"], "Victor")
        self.assertEqual(data["age"]["value"], 30)
        self.assertEqual(data["balance_cents"]["value_cents"], 15000050)

    def test_tier4_misinterpretation_simulation(self):
        translator = DataTranslator()
        sims = translator.simulate_misinterpretation_scenarios(150000.50)
        self.assertIn("unit_mismatch_inflated", sims)
        self.assertIn("type_confusion_float_as_int", sims)

    # Tier 5 Tests
    def test_tier5_online_store_pipeline(self):
        db = OnlineStoreDatabase()
        app = OnlineStoreApplication(db, tax_rate=0.05)
        payload = {
            "customer_id": "CUST-1",
            "sku": "SKU-HEADPHONES",
            "quantity": 2,
            "shipping_address": "Main St",
            "payment_token": "TOK-123",
        }
        res = app.process_order_pipeline(payload)
        self.assertTrue(res["success"])
        self.assertEqual(res["subtotal"], 100000.0)
        self.assertEqual(res["total_charged"], 105000.0)
        self.assertIn(res["order_id"], db.orders)


if __name__ == "__main__":
    unittest.main()

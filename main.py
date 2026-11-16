#!/usr/bin/env python3
"""
Py-Section 1 Mission Project — The Digital Translator
Mission: mission-03 | Squad: Solo 434

Master CLI Demonstrator:
Executes and illustrates all five tiers of computational thinking.
"""

import sys
from src.tier1_literal_assistant import LiteralAssistant, AmbiguousInstructionError
from src.tier2_atm import ATM, BankAccount
from src.tier3_calculator import SimpleCalculator, display_pipeline
from src.tier4_data_translator import DataTranslator
from src.tier5_online_store import OnlineStoreDatabase, OnlineStoreApplication


def run_tier_1():
    print("\n" + "=" * 65)
    print(" TIER 1: THE LITERAL ASSISTANT (Vague vs. Explicit Instructions)")
    print("=" * 65)
    assistant = LiteralAssistant()

    print("\n[Step 1] Attempting vague human command: 'Make me breakfast.'")
    try:
        assistant.execute_vague_command("Make me breakfast.")
    except AmbiguousInstructionError as e:
        print(f"Machine Response:\n{e}")

    print("\n[Step 2] Executing fully qualified, deterministic program:")
    state = assistant.execute_explicit_program({
        "egg_count": 2,
        "bread_slices": 1,
        "burner_setting": 5,
        "serving_location": "Dining Table Place Setting #1"
    })
    for idx, log in enumerate(state.log, 1):
        print(f"  {idx:2d}. {log}")
    print(f"\nFinal State Verified: Complete = {state.task_completed}")


def run_tier_2():
    print("\n" + "=" * 65)
    print(" TIER 2: ALGORITHM THINKING (The ATM Algorithm)")
    print("=" * 65)
    atm = ATM(cash_available=400.0, bill_denomination=20)
    account = BankAccount(
        account_number="ACCT-9842",
        card_id="CARD-4411",
        pin="4321",
        balance=250.0,
        daily_limit=300.0
    )

    print("\n[Case A] Insert damaged / unreadable card:")
    ok, msg = atm.insert_card("")
    print(f"Result: {ok} -> {msg}")

    print("\n[Case B] PIN retry limit and retention:")
    atm.insert_card("CARD-4411")
    for attempt in range(1, 4):
        ok, msg = atm.validate_pin("0000", account)
        print(f"Attempt {attempt}: {msg}")

    print("\n[Case C] Normal Withdrawal with balance validation:")
    account.is_blocked = False
    atm = ATM(cash_available=500.0)
    atm.insert_card("CARD-4411")
    atm.validate_pin("4321", account)
    print("Testing amount ($300) > available balance ($250):")
    ok, msg, _ = atm.withdraw_cash(300.0)
    print(f"Result: {msg}")

    print("\nTesting successful amount ($100):")
    ok, msg, dispensed = atm.withdraw_cash(100.0)
    print(f"Result: {msg}")
    print(f"Dispenser: ${dispensed:.2f} dispensed.")
    print(f"Session cleanup: {atm.return_card()}")


def run_tier_3():
    print("\n" + "=" * 65)
    print(" TIER 3: INPUT -> PROCESSING -> OUTPUT (The Simple Calculator)")
    print("=" * 65)
    calc = SimpleCalculator()
    a, b = 20.0, 5.0
    display_pipeline(calc.add(a, b))
    display_pipeline(calc.subtract(a, b))
    display_pipeline(calc.multiply(a, b))
    display_pipeline(calc.divide(a, b))

    print("\n[Reasoning Challenge] Division by Zero (20 / 0):")
    display_pipeline(calc.divide(20.0, 0.0))


def run_tier_4():
    print("\n" + "=" * 65)
    print(" TIER 4: DATA TRANSLATOR (Representation & Misinterpretation)")
    print("=" * 65)
    translator = DataTranslator()
    data = translator.inspect_customer_data("Victor", 30, 150000.50, True)
    for field_name, details in data.items():
        print(f"\n[{field_name.upper()}]")
        for k, v in details.items():
            print(f"  {k:15s}: {v}")

    print("\n--- Reasoning Challenge: Data Representation Failure Modes ---")
    sims = translator.simulate_misinterpretation_scenarios(150000.50)
    for name, item in sims.items():
        print(f"\nScenario: {name}")
        print(f"  Details: {item['description']}")
        print(f"  Impact : {item['financial_impact']}")


def run_tier_5():
    print("\n" + "=" * 65)
    print(" TIER 5: ARCHITECTURE CHALLENGE (Online Store System)")
    print("=" * 65)
    db = OnlineStoreDatabase()
    app = OnlineStoreApplication(db)
    payload = {
        "customer_id": "CUST-VICTOR-30",
        "sku": "SKU-HEADPHONES",
        "quantity": 2,
        "shipping_address": "Suite 404, Silicon Way, CA",
        "payment_token": "TOK-AUTH-SUCCESS-771",
    }
    result = app.process_order_pipeline(payload)
    print("Pipeline Execution Trace:")
    for step in result["trace"]:
        print(f"  * {step}")
    print(f"\nFinal Result Output:")
    print(f"  Status : {result['status']}")
    print(f"  Order  : {result['order_id']}")
    print(f"  Message: {result['message']}")


def main():
    print("=" * 65)
    print(" PY-SECTION 1 MISSION PROJECT: THE DIGITAL TRANSLATOR")
    print(" Mission: mission-03 | Squad: Solo 434")
    print("=" * 65)
    run_tier_1()
    run_tier_2()
    run_tier_3()
    run_tier_4()
    run_tier_5()
    print("\n" + "=" * 65)
    print(" ALL TIERS EXECUTED SUCCESSFULLY.")
    print("=" * 65)


if __name__ == "__main__":
    main()

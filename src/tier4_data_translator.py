"""
Tier 4: Conceptual Challenge - Data Translator

Demonstrates how real-world customer information is translated into computer data,
encodings, binary bits, and what occurs when representation boundaries fail.
"""

import struct
from decimal import Decimal
from typing import Dict, Any


class DataTranslator:
    @staticmethod
    def inspect_customer_data(
        name: str = "Victor",
        age: int = 30,
        balance: float = 150000.50,
        active: bool = True
    ) -> Dict[str, Any]:
        """
        Deconstructs high-level human data into its digital/binary representations.
        """
        # 1. Text: "Victor" -> UTF-8 bytes -> Binary string
        utf8_bytes = name.encode("utf-8")
        name_binary = " ".join(f"{b:08b}" for b in utf8_bytes)
        name_hex = utf8_bytes.hex().upper()

        # 2. Integer: 30 -> 8-bit binary
        age_binary = f"{age:08b}"

        # 3. Floating-point number: 150000.50 -> IEEE 754 double precision (64-bit)
        double_packed = struct.pack(">d", balance)
        balance_binary = " ".join(f"{b:08b}" for b in double_packed)
        balance_hex = double_packed.hex().upper()

        # 4. Financial safe representation: Decimal / Scaled Integer (cents)
        balance_cents = int(Decimal(str(balance)) * 100)
        cents_binary = f"{balance_cents:032b}"

        # 5. Boolean: True -> 1 bit (stored as 1 byte in memory)
        bool_byte = 1 if active else 0
        bool_binary = f"{bool_byte:08b}"

        return {
            "name": {
                "value": name,
                "type": "String (Text)",
                "encoding": "UTF-8",
                "hex": name_hex,
                "binary": name_binary,
            },
            "age": {
                "value": age,
                "type": "Integer (Whole number)",
                "bytes": 1,
                "binary": age_binary,
            },
            "balance_float": {
                "value": balance,
                "type": "Float (IEEE 754 64-bit)",
                "hex": balance_hex,
                "binary": balance_binary,
            },
            "balance_cents": {
                "value_cents": balance_cents,
                "type": "Fixed-Point / Scaled Integer (Cents)",
                "binary": cents_binary,
            },
            "active": {
                "value": active,
                "type": "Boolean (Logical State)",
                "binary": bool_binary,
            },
        }

    @staticmethod
    def simulate_misinterpretation_scenarios(balance: float = 150000.50):
        """
        Demonstrates the Reasoning Challenge:
        What happens if the stored representation is interpreted incorrectly?
        """
        results = {}

        # Scenario A: Unit scaling mismatch (stored as cents, read as dollars)
        # Proper cents = 15000050
        proper_cents = int(Decimal(str(balance)) * 100)
        as_dollars_error = proper_cents  # Program forgot to divide by 100
        as_cents_error = balance / 100.0  # Program divided float balance by 100 again

        results["unit_mismatch_inflated"] = {
            "description": "System treats stored cents (15000050) as whole currency units",
            "resulting_balance": as_dollars_error,
            "financial_impact": "Customer artificially credited with $15,000,050.00!",
        }
        results["unit_mismatch_deflated"] = {
            "description": "System treats dollar input as cents and divides by 100",
            "resulting_balance": as_cents_error,
            "financial_impact": "Customer balance reduced to $1,500.00!",
        }

        # Scenario B: Low-level Type Confusion (Raw bits reinterpreted)
        # Pack the float 150000.50 into 8 bytes, then unpack as signed 64-bit integer
        raw_bytes = struct.pack(">d", balance)
        corrupted_int = struct.unpack(">q", raw_bytes)[0]
        results["type_confusion_float_as_int"] = {
            "description": "Raw 64-bit IEEE float bits parsed directly as a 64-bit signed integer",
            "raw_hex": raw_bytes.hex().upper(),
            "resulting_integer_value": corrupted_int,
            "financial_impact": f"Account shows balance of {corrupted_int} instead of $150,000.50!",
        }

        return results


if __name__ == "__main__":
    translator = DataTranslator()
    data = translator.inspect_customer_data()

    print("=== DATA TRANSLATOR: REAL-WORLD INFO TO DIGITAL REPRESENTATION ===")
    for key, info in data.items():
        print(f"\n[{key.upper()}]")
        for k, v in info.items():
            print(f"  {k:15s}: {v}")

    print("\n=== REASONING CHALLENGE: DATA MISINTERPRETATION SIMULATION ===")
    sims = translator.simulate_misinterpretation_scenarios()
    for name, sim in sims.items():
        print(f"\n[SCENARIO: {name}]")
        print(f"  Details: {sim['description']}")
        print(f"  Impact : {sim['financial_impact']}")

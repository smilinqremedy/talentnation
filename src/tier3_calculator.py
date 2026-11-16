"""
Tier 3: Practical Exercise - Input -> Processing -> Output (The Simple Calculator)

Reinforces the fundamental computer programming paradigm:
INPUT -> PROCESSING -> OUTPUT

Features addition, subtraction, multiplication, and defensive division logic.
"""

from dataclasses import dataclass
from typing import Union, Tuple


@dataclass
class CalculationResult:
    input_a: float
    input_b: float
    operation: str
    processing_description: str
    output: Union[float, str]
    is_success: bool


class SimpleCalculator:
    """
    Executes arithmetic using the explicit Input -> Processing -> Output model.
    """

    @staticmethod
    def add(a: float, b: float) -> CalculationResult:
        # Input: a, b
        # Processing: a + b
        result = a + b
        # Output: result
        return CalculationResult(
            input_a=a,
            input_b=b,
            operation="ADDITION (+)",
            processing_description=f"Combined value {a} with value {b}",
            output=result,
            is_success=True,
        )

    @staticmethod
    def subtract(a: float, b: float) -> CalculationResult:
        # Input: a, b
        # Processing: a - b
        result = a - b
        # Output: result
        return CalculationResult(
            input_a=a,
            input_b=b,
            operation="SUBTRACTION (-)",
            processing_description=f"Deducted value {b} from value {a}",
            output=result,
            is_success=True,
        )

    @staticmethod
    def multiply(a: float, b: float) -> CalculationResult:
        # Input: a, b
        # Processing: a * b
        result = a * b
        # Output: result
        return CalculationResult(
            input_a=a,
            input_b=b,
            operation="MULTIPLICATION (x)",
            processing_description=f"Scaled value {a} by a factor of {b}",
            output=result,
            is_success=True,
        )

    @staticmethod
    def divide(a: float, b: float) -> CalculationResult:
        # Input: dividend a, divisor b
        # Processing with Defensive Validation:
        if b == 0:
            # Defensive check: Impossible operation detected before hardware crash
            return CalculationResult(
                input_a=a,
                input_b=b,
                operation="DIVISION (/)",
                processing_description=(
                    "Defensive Check: Attempted division by zero detected. "
                    "Arithmetic division by zero is undefined. Operation aborted safely."
                ),
                output="ERROR: Division by zero is undefined.",
                is_success=False,
            )

        result = a / b
        return CalculationResult(
            input_a=a,
            input_b=b,
            operation="DIVISION (/)",
            processing_description=f"Partitioned dividend {a} into {b} equal parts",
            output=result,
            is_success=True,
        )


def display_pipeline(calc_res: CalculationResult):
    print("=" * 50)
    print(f"OPERATION: {calc_res.operation}")
    print(f"  [INPUT]      : number_1 = {calc_res.input_a}, number_2 = {calc_res.input_b}")
    print(f"  [PROCESSING] : {calc_res.processing_description}")
    print(f"  [OUTPUT]     : {calc_res.output} (Success: {calc_res.is_success})")
    print("=" * 50)


if __name__ == "__main__":
    calc = SimpleCalculator()
    num1, num2 = 20.0, 5.0

    print("--- Standard Operations with 20 and 5 ---")
    display_pipeline(calc.add(num1, num2))
    display_pipeline(calc.subtract(num1, num2))
    display_pipeline(calc.multiply(num1, num2))
    display_pipeline(calc.divide(num1, num2))

    print("\n--- Reasoning Challenge: Division by Zero (20 and 0) ---")
    display_pipeline(calc.divide(20.0, 0.0))

# Py-SECTION 1 MISSION PROJECT — THE DIGITAL TRANSLATOR

**Mission:** `mission-03`  
**Squad:** `Solo 434`  
**Author:** Fredrick Ocheche (`@ochechefredrick23`)

---

## Overview

This project embodies the **Digital Translator Mindset**: bridging human problem-solving and computer execution by systematically translating real-world intent into precise instructions, data representations, algorithms, and system architectures.

The repository provides both:
1. **Comprehensive Conceptual Write-Up ([`SOLUTION.md`](SOLUTION.md)):** Detailed theoretical analysis, workflows, Mermaid diagrams, failure-mode matrices, and reasoning challenges across Tiers 1 through 5, the Capstone Mental Model, and Final Reflection.
2. **Modular Python Implementations (`src/` & `main.py`):** Fully functional, tested Python implementations illustrating every tier in code.

---

## Project Structure

```text
mission-03-solo-434-py-section-1-mission-project-the-digital-transla/
├── README.md                      # Project overview, architecture, and instructions
├── SOLUTION.md                    # In-depth theoretical solutions for Tiers 1-5 & Reflection
├── main.py                        # Master CLI interactive runner executing all tiers
├── src/
│   ├── __init__.py
│   ├── tier1_literal_assistant.py # The Literal Assistant (Implicit vs. Explicit instructions)
│   ├── tier2_atm.py               # Algorithm Thinking (ATM state machine & failure handling)
│   ├── tier3_calculator.py        # Input -> Processing -> Output (Defensive Calculator)
│   ├── tier4_data_translator.py   # Data Translator (Binary encodings & misinterpretation)
│   └── tier5_online_store.py      # Architecture Challenge (End-to-end Online Store system)
└── tests/
    ├── __init__.py
    └── test_all_tiers.py          # Complete unit test suite (11 unit tests)
```

---

## Tier Summary

### [Tier 1 — The Literal Assistant](SOLUTION.md#tier-1--basic-understanding-the-literal-assistant)
- **Problem:** Human directive `"Make me breakfast"` is loaded with missing assumptions.
- **Solution:** A 34-step deterministic, parameter-complete recipe eliminating ambiguity.
- **Code:** `src/tier1_literal_assistant.py` (Raises `AmbiguousInstructionError` for vague directives; verifies kitchen state machine).

### [Tier 2 — Field Exercise: Algorithm Thinking](SOLUTION.md#tier-2--field-exercise-algorithm-thinking-the-atm)
- **Problem:** Breaking down *"Withdraw money from an ATM"* into an ordered, failure-resilient algorithm.
- **Failures Handled:** Damaged cards, incorrect PIN (with 3-attempt confiscation), insufficient funds, ATM cash shortages, and atomic transaction rollback.
- **Code:** `src/tier2_atm.py`

### [Tier 3 — Practical Exercise: Input → Processing → Output](SOLUTION.md#tier-3--practical-exercise-input--processing--output)
- **Problem:** Implementing the fundamental IPO computing model for addition, subtraction, multiplication, and division.
- **Reasoning Challenge:** Handling division by zero (`20 ÷ 0`) via defensive validation before hardware traps.
- **Code:** `src/tier3_calculator.py`

### [Tier 4 — Conceptual Challenge: Data Translator](SOLUTION.md#tier-4--conceptual-challenge-data-translator)
- **Problem:** Translating customer information (`Victor`, `30`, `150000.50`, `Yes`) into UTF-8, binary, integers, and fixed-point currency representations.
- **Reasoning Challenge:** Demonstrating the impact of data misinterpretation (type confusion, unit scaling mismatch, floating-point drift).
- **Code:** `src/tier4_data_translator.py`

### [Tier 5 — Architecture Challenge: Explain the Whole System](SOLUTION.md#tier-5--architecture-challenge-explain-the-whole-system-the-online-store)
- **Problem:** Tracing an online store purchase through all 6 architectural stages:
  `Customer Input -> Application/Program -> Instructions -> Data Processing -> Stored Data -> Result/Output`.
- **System Analysis:** Identifies hardware actions, software orchestration, transient vs. persistent data, and audit logging.
- **Code:** `src/tier5_online_store.py`

### [Capstone Mental Model & Final Reflection](SOLUTION.md#final-reflection)
- In-depth synthesis of:
  *"A computer does not understand the real world directly. It works with representations of information and follows instructions for processing those representations."*

---

## Quick Start & Execution

### 1. Run the Interactive CLI Demonstrator
To run the master demonstrator that executes all 5 tiers sequentially:

```bash
python3 main.py
```

### 2. Run Individual Modules
Each module in `src/` can be executed independently:

```bash
# Tier 1: Literal Assistant
python3 src/tier1_literal_assistant.py

# Tier 2: ATM Algorithm
python3 src/tier2_atm.py

# Tier 3: Calculator IPO
python3 src/tier3_calculator.py

# Tier 4: Data Translator
python3 src/tier4_data_translator.py

# Tier 5: Online Store Architecture
python3 src/tier5_online_store.py
```

### 3. Run the Unit Test Suite
To execute the automated test suite covering all modules:

```bash
python3 -m unittest discover -s tests
```

---

## Verification & Status

- **Unit Tests:** 11 / 11 tests passing.
- **Dependencies:** Standard Python 3 standard library only (`dataclasses`, `struct`, `decimal`, `unittest`).
- **Gitea Submission:** Ready for review and Squad mission evaluation.

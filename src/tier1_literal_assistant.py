"""
Tier 1: Basic Understanding - The Literal Assistant

Demonstrates why computers require precise, explicit instructions instead of
vague human directives like "Make me breakfast."
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


class AmbiguousInstructionError(ValueError):
    """Raised when an instruction lacks the required explicit parameters."""
    pass


@dataclass
class KitchenState:
    refrigerator_open: bool = False
    eggs_in_fridge: int = 6
    eggs_retrieved: int = 0
    bread_retrieved: int = 0
    eggs_whisked: bool = False
    toaster_active: bool = False
    toast_ready: bool = False
    pan_on_stove: bool = False
    burner_setting: int = 0  # 0 = off, 5 = medium, 10 = high
    pan_oiled: bool = False
    eggs_cooked: bool = False
    served_location: str = ""
    task_completed: bool = False
    log: List[str] = field(default_factory=list)

    def record(self, action: str):
        self.log.append(action)


class LiteralAssistant:
    def __init__(self):
        self.state = KitchenState()

    def execute_vague_command(self, command: str) -> None:
        """
        Demonstrates the failure mode when given a human-style vague command.
        """
        if command.strip().lower() == "make me breakfast":
            missing = [
                "Food item specification (eggs, cereal, toast?)",
                "Food ingredient locations (fridge shelf, pantry?)",
                "Quantity required (how many eggs, how many slices?)",
                "Equipment selection (skillet, toaster, spatula?)",
                "Preparation technique (scrambled, fried, boiled?)",
                "Cook time and heat setting thresholds",
                "Serving location and plating requirements",
                "Termination condition (how to confirm completion)"
            ]
            raise AmbiguousInstructionError(
                f"Cannot execute '{command}'. Missing parameters:\n - " + "\n - ".join(missing)
            )

    def execute_explicit_program(self, recipe_params: Dict[str, Any]) -> KitchenState:
        """
        Executes a sequence of fully specified, deterministic instructions.
        """
        s = self.state

        # Step 1: Open refrigerator
        s.refrigerator_open = True
        s.record("Opened refrigerator door to 60 degrees.")

        # Step 2: Check and retrieve eggs
        needed_eggs = recipe_params.get("egg_count", 2)
        if s.eggs_in_fridge < needed_eggs:
            raise RuntimeError(f"Insufficient eggs. Needed {needed_eggs}, found {s.eggs_in_fridge}.")
        s.eggs_in_fridge -= needed_eggs
        s.eggs_retrieved = needed_eggs
        s.record(f"Retrieved {needed_eggs} raw eggs from top door shelf.")

        # Step 3: Close refrigerator
        s.refrigerator_open = False
        s.record("Closed refrigerator door until latch clicked.")

        # Step 4: Retrieve bread
        needed_bread = recipe_params.get("bread_slices", 1)
        s.bread_retrieved = needed_bread
        s.record(f"Retrieved {needed_bread} slice(s) of bread from bread box.")

        # Step 5: Setup cookware
        s.pan_on_stove = True
        s.record("Placed 10-inch non-stick skillet on front-right stove burner.")

        # Step 6: Start toast
        s.toaster_active = True
        s.record(f"Inserted {needed_bread} slice into toaster at setting 3 and engaged lever.")

        # Step 7: Whisk eggs
        s.eggs_whisked = True
        s.record("Cracked eggs into ceramic bowl, discarded shells, whisked for 30 seconds.")

        # Step 8: Heat pan & oil
        s.burner_setting = recipe_params.get("burner_setting", 5)
        s.pan_oiled = True
        s.record(f"Turned burner to setting {s.burner_setting} and added 1 tsp cooking oil.")

        # Step 9: Cook eggs
        s.eggs_cooked = True
        s.burner_setting = 0  # Turn off
        s.record("Poured eggs into pan, stirred curds for 90 seconds, turned burner OFF.")

        # Step 10: Finish toast
        s.toaster_active = False
        s.toast_ready = True
        s.record("Toaster popped up; retrieved warm toast.")

        # Step 11: Plate and serve
        target_table = recipe_params.get("serving_location", "Dining Table Place Setting #1")
        s.served_location = target_table
        s.record(f"Transferred eggs and toast to clean plate; set down at {target_table}.")

        # Step 12: Verify termination
        assert s.burner_setting == 0, "Safety violation: Burner left on!"
        assert not s.toaster_active, "Safety violation: Toaster left active!"
        s.task_completed = True
        s.record("Task verified complete: all heat sources OFF, breakfast plated.")

        return s


if __name__ == "__main__":
    assistant = LiteralAssistant()
    print("--- Test 1: Vague Instruction ---")
    try:
        assistant.execute_vague_command("Make me breakfast.")
    except AmbiguousInstructionError as e:
        print(f"[REJECTED] {e}\n")

    print("--- Test 2: Precise Instruction Sequence ---")
    result = assistant.execute_explicit_program({
        "egg_count": 2,
        "bread_slices": 1,
        "burner_setting": 5,
        "serving_location": "Dining Table Place Setting #1"
    })
    for i, log_entry in enumerate(result.log, 1):
        print(f"{i:2d}. {log_entry}")
    print(f"\nFinal State: Completed = {result.task_completed}, Location = '{result.served_location}'")

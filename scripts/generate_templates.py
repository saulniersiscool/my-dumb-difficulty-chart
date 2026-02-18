"""
Generate template JSON files for all classes and chains.
Run this once to create the initial template files, then fill them in manually.
"""

import json
import os

CLASSES = [
    ("class_negative", "Class Negative"),
    ("class_0", "Class 0"),
    ("class_1", "Class 1"),
    ("class_2", "Class 2"),
    ("class_3", "Class 3"),
    ("class_4", "Class 4"),
    ("class_5", "Class 5"),
    ("class_6", "Class 6"),
    ("class_7", "Class 7"),
    ("class_8", "Class 8"),
    ("class_9", "Class 9"),
    ("class_10", "Class 10"),
    ("class_11", "Class 11"),
    ("class_12", "Class 12"),
    ("class_13", "Class 13"),
    ("class_14", "Class 14"),
    ("class_15", "Class 15"),
    ("class_16", "Class 16"),
    ("class_17", "Class 17"),
    ("class_18", "Class 18"),
    ("class_19", "Class 19"),
    ("class_20a", "Class 20A"),
    ("class_20b", "Class 20B"),
    ("class_21", "Class 21"),
    ("class_22", "Class 22"),
    ("class_secret", "Class Secret"),
]

CHAINS = [
    ("excavation_chain", "Excavation Chain"),
    ("gar_chain", "Gar Chain"),
    ("error_chain", "Error Chain"),
    ("death_chain", "Death Chain"),
]

EXAMPLE_DIFFICULTY = {
    "name": "Example Difficulty",
    "decal_id": "rbxassetid://0",
    "rating": 0,
    "overview": "A short description of this difficulty goes here."
}

def make_class_template(class_id, class_name):
    return {
        "class_id": class_id,
        "class_name": class_name,
        "description": "Description of this class goes here.",
        "difficulties": [
            EXAMPLE_DIFFICULTY
        ]
    }

def make_chain_template(chain_id, chain_name):
    return {
        "chain_id": chain_id,
        "chain_name": chain_name,
        "description": "Description of this chain goes here.",
        "difficulties": [
            EXAMPLE_DIFFICULTY
        ]
    }

def main():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    classes_dir = os.path.join(base_dir, "data", "classes")
    chains_dir = os.path.join(base_dir, "data", "chains")

    os.makedirs(classes_dir, exist_ok=True)
    os.makedirs(chains_dir, exist_ok=True)

    for class_id, class_name in CLASSES:
        filepath = os.path.join(classes_dir, f"{class_id}.json")
        if os.path.exists(filepath):
            print(f"  SKIP (already exists): {filepath}")
            continue
        with open(filepath, "w") as f:
            json.dump(make_class_template(class_id, class_name), f, indent=2)
        print(f"  Created: {filepath}")

    for chain_id, chain_name in CHAINS:
        filepath = os.path.join(chains_dir, f"{chain_id}.json")
        if os.path.exists(filepath):
            print(f"  SKIP (already exists): {filepath}")
            continue
        with open(filepath, "w") as f:
            json.dump(make_chain_template(chain_id, chain_name), f, indent=2)
        print(f"  Created: {filepath}")

    print(f"\nDone! Created {len(CLASSES)} class templates and {len(CHAINS)} chain templates.")
    print("Now open each file and replace the example difficulty with real data.")

if __name__ == "__main__":
    main()

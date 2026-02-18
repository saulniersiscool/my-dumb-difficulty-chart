"""
Compile all class and chain JSON source files into the /dist/ folder.

This script:
  1. Reads every class file from /data/classes/
  2. Reads every chain file from /data/chains/
  3. Sorts difficulties within each class/chain by rating (lowest to highest)
  4. Validates that no required fields are missing
  5. Outputs compiled per-class and per-chain files to /dist/
  6. Outputs an index.json with metadata about all classes and chains
  7. Optionally outputs an all.json with every difficulty combined

Usage:
  python compile.py
"""

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CLASSES_DIR = DATA_DIR / "classes"
CHAINS_DIR = DATA_DIR / "chains"
DIST_DIR = BASE_DIR / "dist"

REQUIRED_FIELDS = ["name", "decal_id", "rating", "overview"]

# ── Helpers ──────────────────────────────────────────────────────────

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def sort_rating_key(diff):
    """Convert rating to sortable value, handling special string ratings."""
    r = diff.get("rating")
    if r == "-inf":
        return -99999
    if r == "inf":
        return 99999
    if r in ("???", "N/A", "Unending", "251+"):
        return 99998
    try:
        return float(r)
    except (ValueError, TypeError):
        try:
            return float(str(r).split(' ')[0])
        except:
            return 99997

def validate_difficulty(diff, source_file, index):
    """Check that a difficulty entry has all required fields. Returns list of errors."""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in diff:
            errors.append(f'  [{source_file}] Difficulty #{index + 1} ("{diff.get("name", "UNNAMED")}"): missing field \'{field}\'')
        elif field == "name" and not diff[field].strip():
            errors.append(f"  [{source_file}] Difficulty #{index + 1}: 'name' is empty")
    return errors

def process_file(filepath):
    """Load a class/chain file, validate it, sort difficulties by rating."""
    data = load_json(filepath)
    filename = filepath.name
    errors = []

    difficulties = data.get("difficulties", [])

    # Remove example/placeholder entries
    difficulties = [
        d for d in difficulties
        if not (d.get("name") == "Example Difficulty" and d.get("rating") == 0)
    ]

    for i, diff in enumerate(difficulties):
        errors.extend(validate_difficulty(diff, filename, i))

    # Sort by rating
    difficulties.sort(key=sort_rating_key)
    data["difficulties"] = difficulties

    return data, errors

# ── Main ─────────────────────────────────────────────────────────────

def main():
    os.makedirs(DIST_DIR, exist_ok=True)

    all_errors = []
    all_difficulties = []
    index_classes = []
    index_chains = []

    # ── Process classes ───────────────────────────────────────────
    print("Processing classes...")
    class_files = sorted(CLASSES_DIR.glob("*.json"))

    for filepath in class_files:
        data, errors = process_file(filepath)
        all_errors.extend(errors)

        diff_count = len(data["difficulties"])
        print(f"  {data.get('class_name', filepath.stem)}: {diff_count} difficulties")

        # Add class tag to each difficulty for the combined file
        for d in data["difficulties"]:
            d_copy = dict(d)
            d_copy["class_id"] = data.get("class_id", filepath.stem)
            d_copy["class_name"] = data.get("class_name", filepath.stem)
            all_difficulties.append(d_copy)

        # Save compiled class file
        save_json(DIST_DIR / filepath.name, data)

        # Add to index
        index_classes.append({
            "class_id": data.get("class_id", filepath.stem),
            "class_name": data.get("class_name", filepath.stem),
            "description": data.get("description", ""),
            "difficulty_count": diff_count,
            "file": filepath.name
        })

    # ── Process chains ────────────────────────────────────────────
    print("\nProcessing chains...")
    chain_files = sorted(CHAINS_DIR.glob("*.json"))

    for filepath in chain_files:
        data, errors = process_file(filepath)
        all_errors.extend(errors)

        diff_count = len(data["difficulties"])
        print(f"  {data.get('chain_name', filepath.stem)}: {diff_count} difficulties")

        # Save compiled chain file into dist/chains/
        chains_dist = DIST_DIR / "chains"
        os.makedirs(chains_dist, exist_ok=True)
        save_json(chains_dist / filepath.name, data)

        # Add to index
        index_chains.append({
            "chain_id": data.get("chain_id", filepath.stem),
            "chain_name": data.get("chain_name", filepath.stem),
            "description": data.get("description", ""),
            "difficulty_count": diff_count,
            "file": f"chains/{filepath.name}"
        })

    # ── Build index.json ──────────────────────────────────────────
    all_difficulties.sort(key=sort_rating_key)

    index = {
        "total_difficulties": len(all_difficulties),
        "total_classes": len(index_classes),
        "total_chains": len(index_chains),
        "classes": index_classes,
        "chains": index_chains
    }
    save_json(DIST_DIR / "index.json", index)
    print(f"\nindex.json: {len(index_classes)} classes, {len(index_chains)} chains, {len(all_difficulties)} total difficulties")

    # ── Build all.json ────────────────────────────────────────────
    save_json(DIST_DIR / "all.json", {
        "total": len(all_difficulties),
        "difficulties": all_difficulties
    })
    print(f"all.json: {len(all_difficulties)} difficulties")

    # ── Report errors ─────────────────────────────────────────────
    if all_errors:
        print(f"\n⚠️  {len(all_errors)} validation error(s) found:")
        for err in all_errors:
            print(err)
        sys.exit(1)
    else:
        print("\n✅ No validation errors. Compiled successfully!")

if __name__ == "__main__":
    main()

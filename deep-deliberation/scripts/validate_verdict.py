#!/usr/bin/env python3
"""
Deep Deliberation Final Output Validator

Validates the combined Stage 6 (Judge verdict) + Stage 7 (Action Plan) output.
Judge contributes: Scorecard, Quantitative Rigor criterion, Winner.
Action Plan contributes: 4 time horizons, Decision Checkpoints, Flip Conditions.
"""

import sys
import argparse
from dataclasses import dataclass


@dataclass
class Result:
    success: bool
    error: str = ""


def validate_final_output(filepath: str) -> Result:
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return Result(False, f"File not found: {filepath}")

    # Stage 6 (Judge) checks
    if "Scorecard" not in content:
        return Result(False, "Missing 'Scorecard' section from judge.")

    if "quantitative rigor" not in content.lower():
        return Result(False, "Missing 'Quantitative Rigor' criterion in scorecard.")

    if "Winner" not in content:
        return Result(False, "Missing 'Winner' declaration from judge.")

    # Stage 7 (Action Plan) checks
    required_horizons = ["Next Week", "Next Month", "Next Quarter", "Next Year"]
    for horizon in required_horizons:
        if horizon not in content:
            return Result(False, f"Missing required time horizon: {horizon}")

    if "Decision Checkpoints" not in content:
        return Result(False, "Missing 'Decision Checkpoints' section.")

    if "Flip Conditions" not in content and "What Could Flip" not in content:
        return Result(False, "Missing 'Flip Conditions' section.")

    return Result(True)


def main():
    parser = argparse.ArgumentParser(description="Validate Deep Deliberation Final Output")
    parser.add_argument("filepath", help="Path to the combined verdict + action plan markdown file")
    args = parser.parse_args()

    result = validate_final_output(args.filepath)
    if result.success:
        print("Validation PASSED: Final output meets all structural requirements.")
        sys.exit(0)
    else:
        print(f"Validation FAILED: {result.error}", file=sys.stderr)
        sys.exit(10)


if __name__ == "__main__":
    main()

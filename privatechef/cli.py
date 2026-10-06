"""Command-line entry point for the demo pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import build_courier_lists, build_kitchen_summary, build_label_rows, load_orders


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate fictional PrivateChef operations outputs.")
    parser.add_argument("input", type=Path, help="JSON file containing orders")
    parser.add_argument("--output", type=Path, default=Path("generated"), help="Output directory")
    args = parser.parse_args()

    orders = load_orders(args.input)
    args.output.mkdir(parents=True, exist_ok=True)
    outputs = {
        "kitchen-summary.json": build_kitchen_summary(orders),
        "courier-lists.json": build_courier_lists(orders),
        "label-rows.json": build_label_rows(orders),
    }
    for filename, payload in outputs.items():
        (args.output / filename).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"Generated {len(outputs)} files in {args.output.resolve()}")


if __name__ == "__main__":
    main()

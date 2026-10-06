"""Validated transformations for a fictional meal-delivery workflow."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {"order_id", "delivery_date", "customer", "address", "phone", "items"}


def load_orders(path: str | Path) -> list[dict[str, Any]]:
    """Load and validate a JSON order list without changing the source file."""
    with Path(path).open(encoding="utf-8") as source:
        orders = json.load(source)
    if not isinstance(orders, list):
        raise ValueError("The input must be a JSON list.")

    seen_ids: set[str] = set()
    for index, order in enumerate(orders, start=1):
        if not isinstance(order, dict):
            raise ValueError(f"Order {index} must be an object.")
        missing = REQUIRED_FIELDS - order.keys()
        if missing:
            raise ValueError(f"Order {index} is missing: {', '.join(sorted(missing))}.")
        order_id = str(order["order_id"]).strip()
        if not order_id or order_id in seen_ids:
            raise ValueError(f"Order {index} has an empty or duplicate order_id.")
        seen_ids.add(order_id)
        if not isinstance(order["items"], list) or not order["items"]:
            raise ValueError(f"Order {order_id} must contain at least one item.")
        for item in order["items"]:
            if not isinstance(item, dict) or not {"name", "quantity"} <= item.keys():
                raise ValueError(f"Order {order_id} contains an invalid item.")
            if not isinstance(item["quantity"], int) or item["quantity"] <= 0:
                raise ValueError(f"Order {order_id} contains an invalid quantity.")
    return orders


def build_kitchen_summary(orders: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Aggregate menu quantities by delivery date for kitchen planning."""
    summary: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
    for order in orders:
        for item in order["items"]:
            summary[order["delivery_date"]][item["name"]] += item["quantity"]
    return {
        date: dict(sorted(items.items()))
        for date, items in sorted(summary.items())
    }


def build_courier_lists(orders: list[dict[str, Any]]) -> dict[str, list[dict[str, str]]]:
    """Create a date-grouped courier list with the operational contact fields."""
    grouped: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for order in orders:
        grouped[order["delivery_date"]].append(
            {
                "order_id": str(order["order_id"]),
                "customer": str(order["customer"]),
                "address": str(order["address"]),
                "phone": str(order["phone"]),
                "package_count": str(sum(item["quantity"] for item in order["items"])),
            }
        )
    return {date: rows for date, rows in sorted(grouped.items())}


def build_label_rows(orders: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Expand orders into one printable label record per ordered portion."""
    labels: list[dict[str, str]] = []
    for order in orders:
        for item in order["items"]:
            for portion in range(1, item["quantity"] + 1):
                labels.append(
                    {
                        "order_id": str(order["order_id"]),
                        "delivery_date": str(order["delivery_date"]),
                        "customer": str(order["customer"]),
                        "item": str(item["name"]),
                        "portion": f"{portion}/{item['quantity']}",
                    }
                )
    return labels

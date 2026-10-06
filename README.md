# PrivateChef operations automation

A privacy-safe, runnable Python demonstration of an operations workflow developed for weekly meal delivery. It turns validated orders into three practical outputs: a date-based kitchen summary, courier lists, and printable label rows.

## What this demonstrates

- deterministic order validation and transformation;
- kitchen totals grouped by delivery date and menu item;
- courier-ready customer and package lists;
- one label record per portion;
- automated tests and a command-line workflow;
- privacy-conscious publication using fictional sample data only.

## Run locally

Requires Python 3.10 or newer and has no third-party dependencies.

```bash
python -m unittest discover -s tests -v
python -m privatechef.cli examples/orders.json --output generated
```

The generated files are written to `generated/` and deliberately excluded from Git.

## Privacy note

All people, phone numbers, addresses and order identifiers in this repository are fictional. Live customer orders, business exports and label files are not included.

## Portfolio context

This repository is a sanitized technical sample. The production work also covered source-document processing, spreadsheet compatibility, kitchen handoff formats and printable courier documentation, but operational data and client-specific files remain private.

import unittest

from privatechef.pipeline import build_courier_lists, build_kitchen_summary, build_label_rows


ORDERS = [
    {
        "order_id": "DEMO-1",
        "delivery_date": "2026-10-12",
        "customer": "Minta Anna",
        "address": "Példa utca 1.",
        "phone": "+36 30 000 0001",
        "items": [
            {"name": "A menü", "quantity": 2},
            {"name": "B menü", "quantity": 1},
        ],
    },
    {
        "order_id": "DEMO-2",
        "delivery_date": "2026-10-12",
        "customer": "Teszt Béla",
        "address": "Próba tér 2.",
        "phone": "+36 30 000 0002",
        "items": [{"name": "A menü", "quantity": 1}],
    },
]


class PipelineTests(unittest.TestCase):
    def test_kitchen_summary_aggregates_portions(self):
        self.assertEqual(
            build_kitchen_summary(ORDERS),
            {"2026-10-12": {"A menü": 3, "B menü": 1}},
        )

    def test_courier_list_counts_packages(self):
        rows = build_courier_lists(ORDERS)["2026-10-12"]
        self.assertEqual(rows[0]["package_count"], "3")

    def test_label_rows_expand_quantities(self):
        labels = build_label_rows(ORDERS)
        self.assertEqual(len(labels), 4)
        self.assertEqual(labels[1]["portion"], "2/2")


if __name__ == "__main__":
    unittest.main()

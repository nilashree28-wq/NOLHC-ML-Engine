"""
Operator-console backend (technical report §13): pending queue + the thin
operator_api wrappers. The heavy loop logic is covered by the existing loop
tests; this checks the queue semantics and that the wrappers return the
shapes the UI expects without mutating committed data.
"""

from __future__ import annotations

import importlib
import sys
import tempfile
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


class PendingQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        from loop import pending_queue

        self.pq = pending_queue
        self._tmp = tempfile.TemporaryDirectory()
        self.pq.QUEUE_DIR = Path(self._tmp.name)
        self.pq.QUEUE_PATH = self.pq.QUEUE_DIR / "pending_queue.json"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_add_then_list(self) -> None:
        e = self.pq.add({"NA_Im": 1.0, "A_Im": 2.0}, reason="wide interval")
        self.assertIsNotNone(e)
        entries = self.pq.list_entries("open")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["reason"], "wide interval")
        self.assertEqual(entries[0]["status"], "open")

    def test_near_duplicate_is_merged_not_appended(self) -> None:
        self.pq.add({"NA_Im": 100.0}, reason="r")
        merged = self.pq.add({"NA_Im": 100.00001}, reason="r")
        self.assertIsNone(merged)  # de-duped
        entries = self.pq.list_entries("open")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["seen_count"], 2)

    def test_dismiss_removes_from_open(self) -> None:
        e = self.pq.add({"NA_Im": 1.0}, reason="r")
        self.assertTrue(self.pq.set_status(e["id"], "dismissed"))
        self.assertEqual(self.pq.list_entries("open"), [])

    def test_missing_file_is_empty_not_error(self) -> None:
        self.assertEqual(self.pq.list_entries("open"), [])


class OperatorApiShapeTests(unittest.TestCase):
    """Read-only calls only — nothing here writes to the committed dataset."""

    def test_dataset_status_shape(self) -> None:
        from loop import operator_api

        d = operator_api.dataset_status()
        self.assertIn("n_training_rows", d)
        self.assertIn("per_kpi_rows", d)
        self.assertIn("rounds", d)
        self.assertGreaterEqual(d["n_training_rows"], 129)
        self.assertIsInstance(d["rounds"], list)

    def test_pending_list_shape(self) -> None:
        from loop import operator_api

        d = operator_api.pending_list()
        self.assertIn("entries", d)
        self.assertIsInstance(d["entries"], list)

    def test_ingest_unknown_round_is_clean_error(self) -> None:
        from loop import operator_api

        d = operator_api.ingest_round("round_does_not_exist", "run_id,replication,seed\n")
        self.assertFalse(d["ok"])
        self.assertIn("No round", d["error"])


if __name__ == "__main__":
    unittest.main()

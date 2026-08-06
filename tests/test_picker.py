import datetime as dt
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "crazy-professor" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import picker


class VariationGuardLeastRecentlySeenTests(unittest.TestCase):
    NOW = dt.datetime(2026, 8, 6, tzinfo=dt.timezone.utc)

    @staticmethod
    def rows(*archetypes: str) -> list[dict]:
        return [{"archetype": archetype, "word": f"word-{i}"} for i, archetype in enumerate(archetypes)]

    def guarded_archetype(self, *history: str) -> str:
        selected, _, marker = picker.variation_guard(
            "first-principles-jester",
            "fresh-word",
            self.rows(*history),
            ["fresh-word"],
            self.NOW,
        )
        self.assertEqual(marker, "archetype")
        return selected

    def test_unseen_candidate_wins_over_seen_candidates(self):
        selected = self.guarded_archetype(
            "systems-alchemist",
            "labyrinth-librarian",
            "first-principles-jester",
            "first-principles-jester",
            "first-principles-jester",
        )
        self.assertEqual(selected, "radagast-brown")

    def test_oldest_seen_candidate_wins_when_all_candidates_seen(self):
        selected = self.guarded_archetype(
            "radagast-brown",
            "systems-alchemist",
            "labyrinth-librarian",
            "first-principles-jester",
            "first-principles-jester",
            "first-principles-jester",
        )
        self.assertEqual(selected, "radagast-brown")

    def test_most_recent_candidate_is_deprioritized(self):
        selected = self.guarded_archetype(
            "systems-alchemist",
            "radagast-brown",
            "labyrinth-librarian",
            "first-principles-jester",
            "first-principles-jester",
            "first-principles-jester",
        )
        self.assertEqual(selected, "systems-alchemist")
        self.assertNotEqual(selected, "labyrinth-librarian")


if __name__ == "__main__":
    unittest.main()

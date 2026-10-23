import datetime as dt
import random
import sys
from collections import Counter
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
            random.Random(0),
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


class RandomSourceTests(unittest.TestCase):
    """Since v0.15.1 picks come from a random source, not from the clock."""

    WORDS = [f"word-{i}" for i in range(50)]
    T1 = dt.datetime(2026, 10, 23, 8, 6, 42, tzinfo=dt.timezone.utc)
    T2 = dt.datetime(2026, 10, 23, 11, 10, 46, tzinfo=dt.timezone.utc)

    def pick(self, seed, ts=None, dial=60):
        return picker.pick_single(self.WORDS, [], ts or self.T1, dial=dial, rng=picker.make_rng(seed))

    def test_same_seed_same_pick(self):
        a, b = self.pick(7), self.pick(7)
        self.assertEqual((a["archetype"], a["word"], a["operator"]), (b["archetype"], b["word"], b["operator"]))

    def test_clock_no_longer_decides(self):
        # 08:06:42 and 11:10:46 both gave alchemist + escape under the old minute/second rule
        a, b = self.pick(7, self.T1), self.pick(7, self.T2)
        self.assertEqual((a["archetype"], a["operator"]), (b["archetype"], b["operator"]))
        voices = {self.pick(seed, self.T1)["archetype"] for seed in range(40)}
        self.assertEqual(len(voices), 4)

    def test_archetypes_roughly_uniform(self):
        rng = picker.make_rng(123)
        counts = Counter(picker.pick_archetype_operator(rng)[0] for _ in range(4000))
        for archetype in picker.ARCHETYPES:
            self.assertGreater(counts[archetype], 850)
            self.assertLess(counts[archetype], 1150)

    def test_high_dial_still_favors_wild_operators(self):
        rng = picker.make_rng(5)
        counts = Counter(picker.pick_archetype_operator(rng, dial=80)[1] for _ in range(3000))
        wild = counts["exaggeration"] + counts["escape"]
        self.assertGreater(wild / 3000, 0.6)

    def test_system_source_without_seed(self):
        self.assertIsInstance(picker.make_rng(), random.SystemRandom)

    def test_duet_pair_without_arg_is_a_diagonal(self):
        pair, err = picker.resolve_pair(None, picker.make_rng(3))
        self.assertIsNone(err)
        self.assertIn(pair, picker.TENSION_DIAGONALS)


if __name__ == "__main__":
    unittest.main()

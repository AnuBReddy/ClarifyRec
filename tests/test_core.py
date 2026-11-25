import unittest
from clarifyrec.nlp import extract_preferences
from clarifyrec.preference import PreferenceProfile
from clarifyrec.strategies import ImmediateUpdater, WeightedUpdater, ClarifyRec

class ClarifyRecTests(unittest.TestCase):
    def test_extracts_positive_and_negative_preferences(self):
        p = extract_preferences("I like romance but don't want a tragic ending")
        self.assertIn("romance", p["likes"])
        self.assertEqual(p["constraints"][0]["value"], "not tragic")

    def test_ambiguous_phrase_detected(self):
        p = extract_preferences("I want something lighter")
        self.assertTrue(p["ambiguous"])
        self.assertEqual(p["ambiguous"][0]["phrase"], "lighter")

    def test_mixed_utterance_preserves_clear_preference_while_clarifying(self):
        engine = ClarifyRec()
        result = engine.process("I like romance, but nothing too heavy")
        self.assertEqual(result["status"], "clarification_pending")
        self.assertIn("romance", result["profile"]["likes"])
        self.assertNotIn("serious", result["profile"]["dislikes"])

    def test_clear_correction_does_not_trigger_clarification(self):
        engine = ClarifyRec()
        result = engine.process("I don't want a tragic ending")
        self.assertEqual(result["status"], "updated")
        self.assertEqual(result["profile"]["constraints"]["ending"], "not tragic")

    def test_ambiguous_correction_prompts_then_resolves(self):
        engine = ClarifyRec()
        first = engine.process("I want something lighter")
        self.assertEqual(first["status"], "clarification_pending")
        second = engine.process("I mean more humorous")
        self.assertEqual(second["status"], "resolved")
        self.assertIn("comedy", second["profile"]["likes"])

    def test_explicit_revision_reverses_feature_polarity(self):
        profile = PreferenceProfile()
        profile.apply({"raw":"I dislike comedy", "likes":[], "dislikes":["comedy"], "constraints":[]})
        profile.apply({"raw":"Actually I like comedy", "likes":["comedy"], "dislikes":[], "constraints":[]})
        self.assertIn("comedy", profile.likes)
        self.assertNotIn("comedy", profile.dislikes)

    def test_all_strategies_return_recommendations(self):
        for cls in [ImmediateUpdater, WeightedUpdater, ClarifyRec]:
            result = cls().process("I like romance")
            self.assertTrue(result["recommendations"])

    def test_not_tragic_constraint_penalises_tragic_movies(self):
        engine = ImmediateUpdater()
        result = engine.process("I don't want a tragic ending")
        self.assertTrue(all(m["ending"] != "tragic" for m in result["recommendations"]))

if __name__ == "__main__": unittest.main()

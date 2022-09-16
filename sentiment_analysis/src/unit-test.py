from main import analyze_emotion
import unittest

class TestEmotions(unittest.TestCase):

    def test_analyze_emotion_correct(self):
        self.assertEqual(
            analyze_emotion(
                {"name": "unittest.jpg", "bucket": "tfstate-bucket-soa"}, 0),
                "Happy")

    def test_analyze_emotion_incorrect(self):
        self.assertNotEqual(
            analyze_emotion(
                {"name": "unittest.jpg", "bucket": "tfstate-bucket-soa"}, 0),
                "Angry")

if __name__ == '__main__':
    unittest.main()
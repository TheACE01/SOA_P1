import main

"""
Unit test
"""


def test_analyze_emotion():
    """
    Unit test
    """
    result = main.analyze_emotion(
        {"name": "unittest.jpg", "bucket": "tfstate-bucket-soa"}, 0)

    assert result == "Happy"
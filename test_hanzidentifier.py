import hanzidentifier as han


def test_handles_punctuation():
    "has_chinese() returns False for Chinese punctuation"
    assert han.has_chinese('。？《》；（）’') == False

def test_kana():
    "has_chinese() returns False for Japanese kana"
    assert han.has_chinese('こんにちは') == False

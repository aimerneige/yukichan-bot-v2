from yukichan_bot.plugins.match import MATCH_RULES, is_matched_message


class TextEvent:
    def __init__(self, text: str) -> None:
        self.text = text

    def get_plaintext(self) -> str:
        return self.text


def test_is_matched_message_matches_dict_rules() -> None:
    assert is_matched_message(TextEvent("老婆"))
    assert MATCH_RULES["老婆"] == "肥宅不要乱叫老婆啊！"
    assert is_matched_message(TextEvent("关于"))
    assert "https://github.com/aimerneige/yukichan-bot-v2" in MATCH_RULES["关于"]
    assert is_matched_message(TextEvent("about"))
    assert "https://github.com/aimerneige/yukichan-bot-v2" in MATCH_RULES["about"]
    assert not is_matched_message(TextEvent("老婆！"))
    assert not is_matched_message(TextEvent("我的老婆"))

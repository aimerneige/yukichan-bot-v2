from yukichan_bot.plugins.match import is_wife_message


class TextEvent:
    def __init__(self, text: str) -> None:
        self.text = text

    def get_plaintext(self) -> str:
        return self.text


def test_is_wife_message_matches_only_the_exact_text() -> None:
    assert is_wife_message(TextEvent("老婆"))
    assert not is_wife_message(TextEvent("老婆！"))
    assert not is_wife_message(TextEvent("我的老婆"))

from style_bert_vits2.nlp.japanese.g2p import g2p as jp_g2p
from style_bert_vits2.nlp.japanese.mora_list import (
    CONSONANTS,
    MORA_KATA_TO_MORA_PHONEMES,
    MORA_PHONEMES_TO_MORA_KATA,
)
from style_bert_vits2.nlp.symbols import PUNCTUATIONS
from style_bert_vits2.nlp.english.g2p import g2p as en_g2p
from style_bert_vits2.constants import Languages

def is_japanese(text: str) -> bool:
    """
    テキストが日本語かどうかを判定する。
    """
    for ch in text:
        if '\u4e00' <= ch <= '\u9faf' or '\u3040' <= ch <= '\u309f' or '\u30a0' <= ch <= '\u30ff':
            return True
    return False

def g2kata_tone(norm_text: str, language: Languages) -> list[tuple[str, int]]:
    """
    テキストからカタカナとアクセントのペアのリストを返す。
    推論時のみに使われる関数のため、常に `raise_yomi_error=False` を指定して g2p() を呼ぶ仕様になっている。

    Args:
        norm_text: 正規化されたテキスト。
        language: テキストの言語 ('JP' or 'EN')。

    Returns:
        カタカナと音高のリスト。
    """

    if language == Languages.JP:
        phones, tones, _ = jp_g2p(norm_text, use_jp_extra=True, raise_yomi_error=False)
    else:
        phones, tones, _ = en_g2p(norm_text)
    return phone_tone2kata_tone(list(zip(phones, tones)), language)


def phone_tone2kata_tone(phone_tone: list[tuple[str, int]], language: Languages) -> list[tuple[str, int]]:
    """
    phone_tone の phone 部分をカタカナに変換する。ただし最初と最後の ("_", 0) は無視する。

    Args:
        phone_tone: 音素と音高のリスト。
        language: テキストの言語 ('JP' or 'EN')。

    Returns:
        カタカナと音高のリスト。
    """

    # 最初と最後の("_", 0)を無視する処理
    if phone_tone[0][0] == "_" and phone_tone[-1][0] == "_":
        phone_tone = phone_tone[1:-1]
    
    phones = [phone for phone, _ in phone_tone]
    tones = [tone for _, tone in phone_tone]
    result: list[tuple[str, int]] = []

    if language == Languages.JP:
        current_mora = ""
        for phone, next_phone, tone, next_tone in zip(phones, phones[1:] + ["_"], tones, tones[1:] + [0]):
            if phone in PUNCTUATIONS:
                result.append((phone, tone))
                continue
            if phone in CONSONANTS:  # n以外の子音の場合
                assert current_mora == "", f"Unexpected {phone} after {current_mora}"
                assert tone == next_tone, f"Unexpected {phone} tone {tone} != {next_tone}"
                current_mora = phone
            else:
                # phoneが母音もしくは「N」
                current_mora += phone
                result.append((MORA_PHONEMES_TO_MORA_KATA[current_mora], tone))
                current_mora = ""
    else:
        result = [(phone, tone) for phone, tone in zip(phones, tones)]

    return result


def kata_tone2phone_tone(kata_tone: list[tuple[str, int]], language: Languages) -> list[tuple[str, int]]:
    """
    `phone_tone2kata_tone()` の逆の変換を行う。

    Args:
        kata_tone: カタカナと音高のリスト。
        language: テキストの言語 ('JP' or 'EN')。

    Returns:
        音素と音高のリスト。
    """

    result: list[tuple[str, int]] = [("_", 0)]
    for mora, tone in kata_tone:
        if mora in PUNCTUATIONS:
            result.append((mora, tone))
        else:
            if language == Languages.JP:
                consonant, vowel = MORA_KATA_TO_MORA_PHONEMES[mora]
                if consonant is None:
                    result.append((vowel, tone))
                else:
                    result.append((consonant, tone))
                    result.append((vowel, tone))
            else:
                result.append((mora, tone))
    result.append(("_", 0))

    return result

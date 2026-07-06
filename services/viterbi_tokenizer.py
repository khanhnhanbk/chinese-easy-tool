import math
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHINESE_UNICODE_RANGE = [
    (0x25CB, 0x25CB),  # White Circle
    (0x2E80, 0x2EF3),  # CJK Radicals Supplement
    (0x2F00, 0x2FD5),  # Kangxi Radicals
    (0x3005, 0x3005),  # Ideographic Iteration Mark
    (0x3007, 0x3007),  # Ideographic Number Zero
    (0x3021, 0x3029),  # Hangzhou Numerals
    (0x3038, 0x3038),  # Hangzhou Numeral
    (0x303B, 0x303B),  # Ideographic Iteration Mark
    (0x337B, 0x337E),  # Square Era Names
    (0x3400, 0x4DBF),  # CJK Unified Ideographs Extension A
    (0x4E00, 0x9FFF),  # CJK Unified Ideographs
    (0xF900, 0xFAFF),  # CJK Compatibility Ideographs
    (0x20000, 0x2A6DF),  # CJK Unified Ideographs Extension B
    (0x2A700, 0x2B73F),  # CJK Unified Ideographs Extension C
    (0x2B740, 0x2B81F),  # CJK Unified Ideographs Extension D
    (0x2B820, 0x2CEAF),  # CJK Unified Ideographs Extension E
    (0x2CEB0, 0x2EBEF),  # CJK Unified Ideographs Extension F
    (0x2F800, 0x2FA1F),  # CJK Compatibility Ideographs Supplement
    (0x30000, 0x3134F),  # CJK Unified Ideographs Extension G
    (0x31350, 0x323AF),  # CJK Unified Ideographs Extension H
]


def is_chinese_char(char: str) -> bool:
    if not char:
        return False

    code = ord(char)
    for start, end in CHINESE_UNICODE_RANGE:
        if start <= code <= end:
            return True
    return False


class ViterbiChineseTokenizer:
    vocab_file_path = BASE_DIR / "dicts" / "word_list.txt"

    def __init__(self):
        self.word_cost: dict[str, float] = {}

        with open(self.vocab_file_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                word = line.strip()
                if word:
                    self.word_cost[word] = math.log(idx + 1)

        self.total_words = len(self.word_cost)

        self.oov_cost = math.log(self.total_words + 1)

    def _get_dag(self, text: str) -> dict[int, list[int]]:
        DAG: dict[int, list[int]] = {}
        N = len(text)
        for k in range(N):
            tmplist: list[int] = []
            i = k
            frag = text[k]
            while i < N:
                if frag in self.word_cost or len(frag) == 1:
                    tmplist.append(i)
                i += 1
                if i < N:
                    frag = text[k : i + 1]
            DAG[k] = tmplist
        return DAG

    def _split_segments(self, text: str) -> list[tuple[bool, str]]:
        """
        Chia text thành các đoạn:
        - (True, "...")  : chuỗi tiếng Trung
        - (False, "...") : chuỗi không phải tiếng Trung
        """

        if not text:
            return []

        result: list[tuple[bool, str]] = []

        current = text[0]
        current_is_chinese = is_chinese_char(text[0])

        for ch in text[1:]:
            flag = is_chinese_char(ch)

            if flag == current_is_chinese:
                current += ch
            else:
                result.append((current_is_chinese, current))
                current = ch
                current_is_chinese = flag

        result.append((current_is_chinese, current))
        return result

    def _tokenize_chinese(self, text: str) -> list[str]:
        if not text:
            return []

        N = len(text)
        DAG = self._get_dag(text)

        route: dict[int, tuple[float, int]] = {N: (0, 0)}

        for idx in range(N - 1, -1, -1):
            candidates: list[tuple[float, int]] = []
            for x in DAG[idx]:
                word = text[idx : x + 1]

                if word in self.word_cost:
                    cost = self.word_cost[word]
                else:
                    cost = self.oov_cost

                total_cost = cost + route[x + 1][0]
                candidates.append((total_cost, x))

            route[idx] = min(candidates, key=lambda c: c[0])

        result: list[str] = []
        x = 0
        while x < N:
            y = route[x][1] + 1
            result.append(text[x:y])
            x = y

        return result

    def _is_numeric_segment(self, segment: str) -> bool:
        return bool(re.fullmatch(r"[0-9]+", segment))

    def tokenize(self, text: str) -> list[str]:
        result: list[str] = []

        for is_chinese, segment in self._split_segments(text):
            if is_chinese:
                result.extend(self._tokenize_chinese(segment))
            else:
                if (
                    result
                    and self._is_numeric_segment(segment)
                    and self._is_numeric_segment(result[-1])
                ):
                    result[-1] = result[-1] + segment
                else:
                    result.append(segment)

        return result

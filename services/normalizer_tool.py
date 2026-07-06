# src/services/text_normalizer.py

import re
from dataclasses import dataclass

from datas.usersetting import SeparatorEnum, UserSettings


@dataclass
class TextNormalizer:
    user_settings: UserSettings

    # --- class constants ---
    PUNCTUATIONS = [
        ",", ".", "...", "!", "?", ";", ":", '"', "'", "(", ")", "[", "]",
        "，", "。", "、", "！", "？", "；", "：", "“", "”", "‘", "’", "（", "）", "…",
    ]

    FULLWIDTH_TO_ASCII = str.maketrans(
        {
            "，": ",",
            "。": ".",
            "；": ";",
            "：": ":",
            "！": "!",
            "？": "?",
            "（": "(",
            "）": ")",
            "、": ",",
        }
    )

    ALLOWED_RE = re.compile(
        r"[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFFA-Za-z0-9·]"
    )

    # ---------------- CORE API ----------------

    def normalize(self, text: str) -> str:
        if not text:
            return ""

        text = self._normalize_punctuation(text)
        text = self._remove_punctuation(text)

        if self.user_settings.multi_char_line:
            return self._normalize_multi_char(text)

        return self._normalize_single_char(text)

    # ---------------- INTERNAL METHODS ----------------

    def _normalize_punctuation(self, text: str) -> str:
        return text.translate(self.FULLWIDTH_TO_ASCII)

    def _remove_punctuation(self, text: str) -> str:
        punctuations = self.PUNCTUATIONS.copy()

        separator_equivalents = {
            SeparatorEnum.COMMA: [",", "，"],
            SeparatorEnum.SEMICOLON: [";", "；"],
            SeparatorEnum.ENTER: ["\n"],
            SeparatorEnum.ANY: [",", "，", ";", "；", "\n"],
        }

        equivalents = separator_equivalents.get(self.user_settings.separator)
        if equivalents:
            for ch in equivalents:
                if ch in punctuations:
                    punctuations.remove(ch)

        for p in punctuations:
            text = text.replace(p, "")

        return text

    def _clean_token(self, token: str) -> str:
        token = "".join(token.split())
        return "".join(ch for ch in token if self.ALLOWED_RE.match(ch))

    def _split_tokens(self, text: str) -> list[str]:
        sep = self.user_settings.separator

        if sep == SeparatorEnum.ENTER:
            return text.splitlines()

        if sep == SeparatorEnum.COMMA:
            return re.split(r"[,，]+", text)

        if sep == SeparatorEnum.SEMICOLON:
            return re.split(r"[;；]+", text)

        return re.split(r"[\s,;，；]+", text)

    def _unique_preserve_order(self, items: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []

        for item in items:
            if item and item not in seen:
                seen.add(item)
                result.append(item)

        return result

    # ---------------- MODES ----------------

    def _normalize_multi_char(self, text: str) -> str:
        tokens = self._split_tokens(text)
        tokens = [self._clean_token(t) for t in tokens]
        tokens = [t for t in tokens if t]

        if not self.user_settings.allow_duplicate:
            tokens = self._unique_preserve_order(tokens)

        separator_map = {
            SeparatorEnum.ENTER: "\n",
            SeparatorEnum.COMMA: ",",
            SeparatorEnum.SEMICOLON: ";",
            SeparatorEnum.ANY: ",",
        }

        return separator_map.get(
            self.user_settings.separator, " "
        ).join(tokens)

    def _normalize_single_char(self, text: str) -> str:
        text = self._clean_token(text)

        if self.user_settings.allow_duplicate:
            return text

        seen: set[str] = set()
        result: list[str] = []

        for ch in text:
            if ch not in seen:
                seen.add(ch)
                result.append(ch)

        return "".join(result)
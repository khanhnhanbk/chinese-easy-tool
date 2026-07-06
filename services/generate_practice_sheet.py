import math
from pathlib import Path
import re
import io
from reportlab.pdfgen import canvas

from pypinyin import pinyin
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from datas.usersetting import SeparatorEnum, UserSettings
from services.normalizer_tool import TextNormalizer

BASE_DIR = Path(__file__).resolve().parent.parent


FONT_PATH = BASE_DIR / "fonts" / "Kaiti.ttf"
PINYIN_FONT = BASE_DIR / "fonts" / "SpaceGrotesk.ttf"


def parse_lines(content: str) -> list[str]:
    return [line.strip() for line in content.splitlines() if line.strip()]


def get_pinyin(char: str) -> str:
    return " ".join([item[0] for item in pinyin(char)])


def build_output_file(
    output_directory: str,
    output_filename: str,
) -> str:
    """
    Build a safe PDF output path.

    If the directory or filename is invalid,
    fall back to ./output.pdf
    """

    try:
        filename = (output_filename or "").strip()

        if not filename:
            filename = "output.pdf"

        path = Path(output_directory or ".") / filename

        if path.suffix.lower() != ".pdf":
            path = path.with_suffix(".pdf")

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return str(path)

    except Exception:
        return str(Path.cwd() / "output.pdf")


class ChinesePracticeSheetGenerator:

    pdfmetrics.registerFont(TTFont("KaiTi", FONT_PATH))  # type: ignore
    pdfmetrics.registerFont(TTFont("PinyinFont", PINYIN_FONT))  # type: ignore
    CHAR_FONT = "KaiTi"
    PINYIN_FONT = "PinyinFont"
    BLACK : tuple[float, float, float] = (0, 0, 0)
    GRAY : tuple[float, float, float] = (0.6, 0.6, 0.6)
    RED : tuple[float, float, float] = (0.8, 0.4, 0.4)

    def __init__(
        self, characters: str, user_settings: UserSettings, output: str | None = None
    ):
        normalizer = TextNormalizer(user_settings)
        self.characters = normalizer.normalize(characters)
        self.settings = user_settings

        self.buffer = None
        self.pdf_canvas = None

        if output is None:
            self.output_mode = "memory"
        else:
            self.buffer = None
            self.filename = build_output_file(
                user_settings.output_directory,
                user_settings.output_filename
            )
            self.output_mode = "file"

        width, height = A4
        usable_width = width - user_settings.margin_left * 2
        usable_height = height - user_settings.margin_top * 2

        self.cols_per_page = int(usable_width // user_settings.grid_size)
        self.rows_per_page = int(usable_height // user_settings.grid_size)

    def draw_mizige_box(self, x: float, y: float):
        c = self.pdf_canvas
        size = self.settings.grid_size

        c.setStrokeColorRGB(*self.RED) # type: ignore

        c.setLineWidth(1.2) # type: ignore
        c.rect(x, y, size, size, stroke=1, fill=0) # type: ignore

        c.setLineWidth(0.5) # type: ignore
        c.setDash(2, 2) # type: ignore
 
        c.line(x, y + size / 2, x + size, y + size / 2) # type: ignore
        c.line(x + size / 2, y, x + size / 2, y + size) # type: ignore
        c.line(x, y, x + size, y + size) # type: ignore
        c.line(x, y + size, x + size, y) # type: ignore

        c.setDash() # type: ignore

    def draw_character(self, char: str, x: float, y: float, phrase_index: int):
        c = self.pdf_canvas
        size = self.settings.grid_size
        font_size = size * 0.75

        c.setFont(self.CHAR_FONT, font_size) # type: ignore
        text_width = pdfmetrics.stringWidth(char, self.CHAR_FONT, font_size)

        text_x = x + (size - text_width) / 2
        text_y = y + (size - font_size) / 2 + font_size * 0.2

        if phrase_index == 0:
            c.setFillColorRGB(*self.BLACK) # type: ignore
            c.drawString(text_x, text_y, char) # type: ignore
        elif phrase_index < self.settings.trace_columns:
            c.setFillColorRGB(*self.GRAY) # type: ignore
            c.drawString(text_x, text_y, char) # type: ignore

    def get_lines(self) -> list[str]:

        if self.settings.multi_char_line:
            sep = self.settings.separator

            if sep == SeparatorEnum.ENTER:
                tokens = parse_lines(self.characters)
            elif sep == SeparatorEnum.COMMA:
                tokens = [
                    t.strip()
                    for t in re.split(r"[\n,，]+", self.characters)
                    if t.strip()
                ]
            elif sep == SeparatorEnum.SEMICOLON:
                tokens = [
                    t.strip()
                    for t in re.split(r"[\n;；]+", self.characters)
                    if t.strip()
                ]
            else:  # sep == SeparatorEnum.ANY
                tokens = [
                    t.strip()
                    for t in re.split(r"[\n,;，；、]+", self.characters)
                    if t.strip()
                ]

            lines = tokens
        else:
            lines = [c for c in self.characters if not c.isspace()]

        if not lines:
            raise ValueError("No characters were provided for the practice sheet.")
        return lines

    def build_render_rows(self, lines: list[str]) -> list[tuple[str, int]]:
        """
        Returns:
            [
                ("你好", 0),
                ("你好", 11),
                ("中国", 0),
                ...
            ]

        tuple:
            (phrase, start_index)
        """

        rows : list[tuple[str, int]] = []

        usable_cells = self.cols_per_page - 1

        for phrase in lines:
            phrase_length = len(phrase)

            if phrase_length == 0:
                continue

            rows_needed = math.ceil(
                self.settings.trace_columns * phrase_length / usable_cells
            )

            for row in range(rows_needed):
                rows.append((phrase, row * usable_cells))

        return rows

    def draw_empty_row(self, current_y: float):
        for col in range(1, self.cols_per_page):
            self.draw_mizige_box(
                self.settings.margin_left + self.settings.grid_size * col,
                current_y,
            )

    def draw_pinyin(self, current_y: float, char: str):
        c = self.pdf_canvas
        char_pinyin = get_pinyin(char)

        font_size = max(8, int(self.settings.grid_size / 4))
        c.setFont(self.PINYIN_FONT, font_size) # type: ignore
        c.setFillColorRGB(*self.BLACK) # type: ignore

        available_width = self.settings.grid_size - 4
        tokens = char_pinyin.split()
        lines : list[str] = []
        current = ""
        for tok in tokens:
            test = (current + " " + tok).strip() if current else tok
            if (
                pdfmetrics.stringWidth(test, self.PINYIN_FONT, font_size)
                <= available_width
            ):
                current = test
            else:
                if current:
                    lines.append(current)
                current = tok
        if current:
            lines.append(current)

        line_height = font_size * 0.95
        start_y = (
            current_y + self.settings.grid_size * 0.6 + (len(lines) - 1) * line_height
        )
        pinyin_x = self.settings.margin_left - 5
        for i, line in enumerate(lines):
            pinyin_y = start_y - i * line_height
            c.drawString(pinyin_x, pinyin_y, line) # type: ignore

    def draw_row(self, current_y: float, line_text: str, start_index: int):

        if self.settings.show_pinyin and start_index == 0:
            self.draw_pinyin(current_y, line_text)

        for col in range(1, self.cols_per_page):
            current_x = self.settings.margin_left + (col * self.settings.grid_size)
            self.draw_mizige_box(current_x, current_y)
            phrase_length = len(line_text)

            if phrase_length == 0:
                continue
            phrase_index = (start_index + col - 1) // phrase_length

            char = line_text[(start_index + col - 1) % phrase_length]

            self.draw_character(char, current_x, current_y, phrase_index)

    def generate(self) -> io.BytesIO | str:
        lines = self.get_lines()
        if self.output_mode == "memory":
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            self.buffer = buffer
        else:
            c = canvas.Canvas(self.filename, pagesize=A4)

        self.pdf_canvas = c
        rpp = self.rows_per_page
        size = self.settings.grid_size
        render_rows = self.build_render_rows(lines)

        page_count = math.ceil(len(render_rows) / rpp)
        _, height = A4
        start_y = height - self.settings.margin_top
        for page in range(page_count):
            index_offset = page * rpp

            for row in range(rpp):
                current_y = start_y - (row * size) - size
                line_index = index_offset + row

                if line_index < len(render_rows):
                    line_text, start_index = render_rows[line_index]
                else:
                    self.draw_empty_row(current_y)
                    continue
                self.draw_row(current_y, line_text, start_index)
            if page < page_count - 1:
                c.showPage()

        # Save the canvas once (either writing to buffer or file)
        c.save()

        if self.output_mode == "memory":
            assert self.buffer is not None
            self.buffer.seek(0)
            return self.buffer
        return self.filename
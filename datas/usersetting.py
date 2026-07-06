from dataclasses import dataclass
from enum import Enum



# enum for separator
class SeparatorEnum(Enum):
    ENTER = "\n"
    COMMA = ","
    SEMICOLON = ";"
    ANY = "ANY"


@dataclass
class UserSettings:
    grid_size: int = 45
    trace_columns: int = 10
    multi_char_line: bool = False
    separator: SeparatorEnum = SeparatorEnum.ENTER

    show_pinyin: bool = True
    show_wubi: bool = True
    allow_duplicate: bool = False

    margin_left: int = 25
    margin_top: int = 35
    output_filename: str = "output.pdf"

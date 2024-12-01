import re
from collections.abc import Callable

from df_translation_toolkit.parse.parse_raws import is_translatable

MINIMAL_TRANSLATABLE_WORD_LENGTH = 3
MINMAL_TAG_LENGTH = 3


class IgnoringRuleRegistry:
    all_rules: dict[str, Callable[[str], bool]]

    def __init__(self) -> str:
        self.all_rules = {}

    def register(self, function: Callable[[str], bool]) -> Callable[[str], bool]:
        self.all_rules[function.__name__] = function
        return function

    def check_ignore(self, string: str) -> str | None:
        """
        Check if string should be ignored
        :param string: string to check
        :return: name of the rule if string should be ignored or None if string should be translated
        """
        for name, rule in self.all_rules.items():
            if rule(string):
                return name

        return None


rules = IgnoringRuleRegistry()


@rules.register
def ignore_xml(string: str) -> bool:
    result = re.search(r"""<(\?xml .*|[\w/]+)>""", string)
    return result is not None


square_brackets_exceptions = {
    "DONE",
    "MORE",
    "CAN'T WORK",
    "WITH YOU",
    "LIP",
    "REQUIRE",
    "DEMAND",
    "MANDATE",
    "TRADING",
    "PENDING",
}


@rules.register
def ignore_square_brackets(string: str) -> bool:
    if not any(char in string for char in "[]:"):
        return False
    string = string.replace(r"\t", "\t")
    parts = re.split(r"[\[:\]]", string)
    return not any(is_translatable(part) or part in square_brackets_exceptions for part in parts)


@rules.register
def ignore_paths(string: str) -> bool:
    if re.search(r"\.[a-z]{3}", string):
        return True

    if "/" not in string or " " in string:
        return False

    parts = re.split(r"[/.]", string)
    return all(not part or part.islower() or part == "*" for part in parts)


ignore_tags_exceptions = {"CLT"}


@rules.register
def ignore_tags(string: str) -> bool:
    return len(string) >= MINMAL_TAG_LENGTH and string not in ignore_tags_exceptions and re.fullmatch("[A-Z_]+", string)


@rules.register
def ignore_filenames(string: str) -> bool:
    return re.fullmatch(r".+\.\w{3}", string) is not None


@rules.register
def ignore_gl(string: str) -> bool:
    return re.fullmatch(r"(w?gl[A-Z]|W?GL_)\w+", string) is not None


@rules.register
def ignore_underline_separated_words(string: str) -> bool:
    return re.fullmatch(r"_*[A-Za-z\d]+_.*", string) is not None


@rules.register
def ignore_dash_prepended_strings(string: str) -> bool:
    return re.fullmatch(r"-[a-z0-9_]+-?", string) is not None


@rules.register
def ignore_dash_separated_words(string: str) -> bool:
    if " " in string:
        return False

    dash_index = string.index("-")
    if dash_index < 1:
        return False

    parts = string.split("-")
    for part in parts:
        if not part or not part.islower():
            return False

    if len(parts) >= 3:  # noqa: PLR2004
        return True

    ending = parts[-1]
    return ending.isnumeric() or ending in ("on", "off", "log", "gtr", "rtm")


@rules.register
def ignore_mixed_case(string: str) -> bool:
    return re.search(r"[a-z]+[A-Z]", string) is not None


@rules.register
def ignore_word_with_number(string: str) -> bool:
    return re.fullmatch(r"[A-Za-z]+\d+", string) is not None


forbidden_starts = {
    ": DEMAND_",
    ": MANDATE_",
    ": REQUIRED_",
    "?_",
    "Adventure:",
    "Arena Creature:",
    "Arena Tree:",
    "Arena Weather:",
    "Assign Trade:",
    "Building Items:",
    "Building List:",
    "Building,",
    "Buildjob:",
    "Cage: ",
    "Choose name:",
    "Command Line:",
    "Crash",
    "Custom:",
    "DOUBLE TAGGED ITEM:",
    "Designate,",
    "Dwf Look:",
    "Hot Keys:",
    "Hotkey:",
    "Image Creator:",
    "Item creation failed:",
    "Item submission failed:",
    "Legends:",
    "Load Game:",
    "Location:",
    "Main:",
    "Manager,",
    "Missing ",
    "Move view/cursor ",
    "Movie:",
    "NULL ",
    "Noble List:",
    "Nuked ",
    "Numpad ",
    "Option ",
    "Order:",
    "Orders:",
    "Patched save:",
    "Secondary Option",
    "Setup game:",
    "Setup,",
    "Squad Schedule:",
    "Stockpile Settings:",
    "Stockpile,",
    "String:",
    "Trainer:",
    "Unitjob,",
    "Unitview,",
    "Unrecognized ",
    "View item:",
    "Work Order,",
    "World Gen:",
    "World Generation:",
    "World Param:",
    "World:",
    "ill-sized",
    "incorrect ",
    "invalid ",
    "old save:",
    "unknown",
    "vector",
}


@rules.register
def ignore_starts(string: str) -> bool:
    return any(string.startswith(start) for start in forbidden_starts)


blacklist_full_string = {
    "!ARG",
    "2DASYNC",
    "2DHW",
    "2DSW",
    "Alt+",
    "Ampersand",
    "Asterisk",
    "At",
    "B!+",
    "B!~",
    "Backquote",
    "Backslash",
    "Backspace",
    "Bl+",
    "Bl~",
    "Capslock",
    "Caret",
    "Colon",
    "Comma",
    "Ctrl+",
    "Delete",
    "Dollar",
    "Down",
    "Empty biased index vector",
    "End",
    "End of macro",
    "Enter",
    "Equals",
    "Euro",
    "Exclaim",
    "Exh",
    "Fatal Error",
    "Fnt",
    "Greater",
    "Hash",
    "Insert",
    "Lalt",
    "Lctrl",
    "Left",
    "Leftbracket",
    "Leftparen",
    "Less",
    "Lmeta",
    "Lshift",
    "Lsuper",
    "Menu",
    "Minus",
    "Mode",
    "Nm+",
    "Nm-",
    "Nm~",
    "Numlock",
    "Out of memory - aborting",
    "Ovx",
    "Page Down",
    "Page Up",
    "Pal",
    "Pb!",
    "Pb+",
    "Pb~",
    "Period",
    "Plus",
    "Pn!",
    "Pn+",
    "Pn~",
    "Print",
    "Pz+",
    "Pz~",
    "Question",
    "Quote",
    "Quotedbl",
    "Ralt",
    "Rctrl",
    "Right",
    "Rightbracket",
    "Rightparen",
    "Rmeta",
    "Rshift",
    "Rsuper",
    "Scrollock",
    "Semicolon",
    "Shift+",
    "Slash",
    "Slg",
    "Space",
    "Sw!",
    "Sw+",
    "Sw~",
    "Sysreq",
    "Tab",
    "Tir",
    "Underscore",
    "Undo",
    "Unknown exception",
    "Up",
    "_DIV ",
    "addingtask",
    "assignbuildingjobs",
    "assigndesjobs",
    "bad allocation",
    "bad array new length",
    "bad cast",
    "buildreq",
    "current",
    "cursor",
    "data",
    "dunginv",
    "enabler",
    "feature-",
    "game",
    "gamemode",
    "gametype",
    "gps",
    "gview",
    "handleannounce",
    "init",
    "insufficient memory",
    "interactinvslot",
    "interactitem",
    "invalid string position",
    "itemmade",
    "jobvalue",
    "line",
    "linechar",
    "linelim",
    "looklist",
    "mainview",
    "manucomp",
    "menuposition",
    "modeitem",
    "modejob",
    "modepage",
    "modeseason",
    "modestation",
    "modeunit",
    "modeview",
    "nameless",
    "olookx",
    "olooky",
    "olookz",
    "oscrollx",
    "oscrolly",
    "oscrollz",
    "page",
    "paused",
    "plotinfo",
    "point",
    "preserveannounce",
    "raw",
    "region",
    "scrollx",
    "scrolly",
    "scrollz",
    "season",
    "selectingtaskobject",
    "site-",
    "squadcount",
    "string too long",
    "text",
    "texture",
    "throwitem",
    "title",
    "unitprintstack",
    "updatelightstate",
    "version",
    "weathertimer",
    "world",
    "year",
}


@rules.register
def ignore_by_blacklist_full_string(string: str) -> bool:
    return string in blacklist_full_string


blacklisted_words = {
    "error",
    "overflow",
    "token",
    "null",
    "sdl",
    "REJECTION",
    "font",
    "Font",
    "crc",
}


@rules.register
def ignore_by_blacklisted_words(string: str) -> bool:
    words = re.findall(r"\w+", string.lower())
    return any(blacklisted in words for blacklisted in blacklisted_words)


allowed_short_words = {
    "'s",
    "/E",
    "/N",
    "/S",
    "/W",
    "A",
    "At",
    "He",
    "I",
    "It",
    "No",
    "On",
    "Up",
    "We",
    "an",
    "as",
    "at",
    "b.",
    "by",
    "d.",
    "er",
    "es",
    "he",
    "in",
    "is",
    "it",
    "me",
    "my",
    "nd",
    "no",
    "of",
    "on",
    "rd",
    "s",
    "s]",
    "st",
    "th",
    "to",
    "us",
}


@rules.register
def ignore_short_words(string: str) -> bool:
    return len(string) < MINIMAL_TRANSLATABLE_WORD_LENGTH and string.strip() not in allowed_short_words


blacklisted_substrings = {"placed out of bounds", "set to default", "Patched save"}


@rules.register
def ignore_by_blacklisted_substrings(string: str) -> bool:
    return any(substring in string for substring in blacklisted_substrings)


def all_ignore_rules(string: str) -> str:
    return rules.check_ignore(string)


def dont_ignore(_string: str) -> bool:
    return False

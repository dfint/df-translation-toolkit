import re
from typing import Callable, List

from df_gettext_toolkit.parse_raws import is_translatable


class IgnoringRuleRegistry:
    all_rules: List[Callable[[str], bool]]

    def __init__(self):
        self.all_rules = []

    def register(self, function: Callable[[str], bool]) -> Callable[[str], bool]:
        self.all_rules.append(function)
        return function

    def check_ignore(self, string: str) -> bool:
        return any(rule(string) for rule in self.all_rules)


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
    return len(string) > 2 and string not in ignore_tags_exceptions and re.fullmatch("[A-Z_]+", string)


@rules.register
def ignore_filenames(string: str) -> bool:
    return re.fullmatch(r".+\.\w{3}", string) is not None


@rules.register
def ignore_gl(string: str) -> bool:
    return re.fullmatch(r"(w?gl[A-Z]|W?GL_)\w+", string) is not None


@rules.register
def ignore_underline_separated_words(string: str) -> bool:
    return re.fullmatch(r"[A-Za-z\d]+_.*", string) is not None


@rules.register
def ignore_dash_prepended_strings(string: str) -> bool:
    return re.fullmatch(r"-[a-z_]+-?", string) is not None


@rules.register
def ignore_mixed_case(string: str) -> bool:
    return re.search(r"[a-z]+[A-Z]", string) is not None


@rules.register
def ignore_word_with_number(string: str) -> bool:
    return re.fullmatch(r"[A-Za-z]+\d+", string) is not None


forbidden_starts = {
    "String:",
    "Adventure:",
    "Hotkey:",
    "Main:",
    "Location:",
    "Buildjob:",
    "Movie:",
    "Custom:",
    "Orders:",
    "Dwf Look:",
    "Arena Creature:",
    "Squad Schedule:",
    "Building List:",
    "Hot Keys:",
    "Load Game:",
    "old save:",
    "Stockpile Settings:",
    "Assign Trade:",
    "World:",
    "World Param:",
    "Command Line:",
    "Noble List:",
    "Arena Weather:",
    "Building Items:",
    "Arena Tree:",
    "Image Creator:",
    "Legends:",
    "World Gen:",
    "Setup game:",
    "World Generation:",
    "Choose name:",
    "View item:",
    "Trainer:",
    "Order:",
    "Unitview,",
    "Building,",
    "Designate,",
    "Stockpile,",
    "Setup,",
    "Manager,",
    "Work Order,",
    "Unitjob,",
    "Secondary Option",
    "Unrecognized ",
    "Missing ",
    "unknown",
    "Option ",
    "Numpad ",
    "Move view/cursor ",
    "invalid ",
    "incorrect ",
    "NULL ",
    "Nuked ",
    "Cage: ",
    ": REQUIRED_",
    ": MANDATE_",
    ": DEMAND_",
    "DOUBLE TAGGED ITEM:",
    "Patched save:",
}


@rules.register
def ignore_starts(string: str) -> bool:
    return any(string.startswith(start) for start in forbidden_starts)


blacklist_full_string = {
    "bad allocation",
    "bad array new length",
    "Out of memory - aborting",
    "Fatal Error",
    "nameless",
    "string too long",
    "invalid string position",
    "!ARG",
    "current",
    "Exh",
    "Ovx",
    "Pb!",
    "Pb+",
    "Pb~",
    "Pn!",
    "Pn+",
    "Pn~",
    "Sw!",
    "Sw+",
    "Sw~",
    "Tir",
    "Nm-",
    "Bl+",
    "B!~",
    "B!+",
    "Pz+",
    "Fnt",
    "Pal",
    "Bl~",
    "Nm~",
    "Nm+",
    "Slg",
    "Pz~",
    "scrollx",
    "scrolly",
    "buildreq",
    "jobvalue",
    "version",
    "gview",
    "assignbuildingjobs",
    "year",
    "assigndesjobs",
    "weathertimer",
    "season",
    "line",
    "linechar",
    "scrollz",
    "linelim",
    "gametype",
    "point",
    "gamemode",
    "cursor",
    "modejob",
    "modeitem",
    "addingtask",
    "modeseason",
    "selectingtaskobject",
    "paused",
    "modepage",
    "modestation",
    "squadcount",
    "modeview",
    "modeunit",
    "game",
    "gps",
    "plotinfo",
    "world",
    "itemmade",
    "olookz",
    "oscrollx",
    "olookx",
    "olooky",
    "menuposition",
    "looklist",
    "unitprintstack",
    "title",
    "init",
    "mainview",
    "texture",
    "interactitem",
    "interactinvslot",
    "throwitem",
    "dunginv",
    "page",
    "oscrolly",
    "oscrollz",
    "updatelightstate",
    "handleannounce",
    "preserveannounce",
    "manucomp",
    "enabler",
    "Empty biased index vector",
    "Unknown exception",
    "bad cast",
    "data",
    "region",
    "text",
    "raw",
    "site-",
    "feature-",
    "Backspace",
    "Enter",
    "Up",
    "Delete",
    "Leftbracket",
    "Backslash",
    "Rightbracket",
    "Caret",
    "Underscore",
    "Backquote",
    "Rshift",
    "Lshift",
    "Rctrl",
    "Lctrl",
    "Ralt",
    "Lalt",
    "Rmeta",
    "Lmeta",
    "Numlock",
    "Capslock",
    "Scrollock",
    "Down",
    "Right",
    "Insert",
    "End",
    "Page Up",
    "Page Down",
    "Euro",
    "Undo",
    "Lsuper",
    "Rsuper",
    "Print",
    "Sysreq",
    "Menu",
    "Space",
    "Tab",
    "Shift+",
    "Ctrl+",
    "Alt+",
    "Question",
    "Quotedbl",
    "Hash",
    "Ampersand",
    "Quote",
    "Leftparen",
    "Rightparen",
    "Left",
    "Colon",
    "Semicolon",
    "Less",
    "Equals",
    "Greater",
    "At",
    "Asterisk",
    "Plus",
    "Comma",
    "Minus",
    "Period",
    "Slash",
    "Exclaim",
    "Dollar",
    "Mode",
    "_DIV ",
    "End of macro",
    "2DASYNC",
    "2DHW",
    "2DSW",
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
}


@rules.register
def ignore_by_blacklisted_words(string: str) -> bool:
    words = re.findall(r"\w+", string.lower())
    return any(blacklisted in words for blacklisted in blacklisted_words)


allowed_short_words = {
    "A",
    "an",
    "er",
    "us",  # sarcofag-us
    "as",
    "in",
    "st",
    "is",
    "'s",
    "s",
    "es",
    "nd",
    "rd",
    "th",
    "me",
    "my",
    "no",
    "to",
    "b.",
    "d.",
    "At",
    "Up",
    "On",
    "of",
    "at",
    "by",
    "on",
    "I",
    "He",
    "he",
    "We",
    "it",
    "It",
    "No",
    "s]",
}


@rules.register
def ignore_short_words(string: str) -> bool:
    return len(string) <= 2 and string.strip() not in allowed_short_words


blacklisted_substrings = {"placed out of bounds", "set to default", "Patched save"}


@rules.register
def ignore_by_blacklisted_substrings(string: str) -> bool:
    return any(substring in string for substring in blacklisted_substrings)


def all_ignore_rules(string: str) -> bool:
    return rules.check_ignore(string)


def dont_ignore(_string) -> bool:
    return False

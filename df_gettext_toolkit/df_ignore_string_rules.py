import re
from .parse_raws import is_translatable


def ignore_xml(string):
    result = re.search(r"""<(\?xml .*|[\w/]+)>""", string)
    return result is not None


square_brackets_exceptions = {"DONE", "MORE", "CAN'T WORK", "WITH YOU", "LIP", "REQUIRE", "DEMAND", "MANDATE",
                              "TRADING", "PENDING"}


def ignore_square_brackets(string):
    if not any(char in string for char in '[]:'):
        return False
    string = string.replace(r'\t', '\t')
    parts = re.split(r'[\[:\]]', string)
    return not any(is_translatable(part) or part in square_brackets_exceptions for part in parts)


def ignore_paths(string):
    if re.search(r'\.[a-z]{3}', string):
        return True

    if '/' not in string or ' ' in string:
        return False

    parts = re.split(r'[/.]', string)
    return all(not part or part.islower() or part == '*' for part in parts)


ignore_tags_exceptions = {'CLT'}


def ignore_tags(string):
    return len(string) > 2 and string not in ignore_tags_exceptions and re.fullmatch('[A-Z_]+', string)


def ignore_filenames(string):
    return re.fullmatch(r".+\.[\w]{3}", string) is not None


def ignore_gl(string):
    return re.fullmatch(r"(w?gl[A-Z]|W?GL_)[\w]+", string) is not None


def ignore_underline_separated_words(string):
    return re.fullmatch(r"[A-Za-z0-9]+_.*", string) is not None


def ignore_dash_prepended_strings(string):
    return re.fullmatch(r"-[a-z_]+-?", string) is not None


def ignore_camel_case(string):
    return re.search(r"[a-z]+[A-Z]", string) is not None


def ignore_word_with_number(string):
    return re.fullmatch(r"[A-Za-z]+\d+", string) is not None


forbidden_starts = {
    "String:", "Adventure:", "Hotkey:", "Main:", "Location:", "Buildjob:", "Movie:", "Custom:", "Orders:", "Dwf Look:",
    "Arena Creature:", "Squad Schedule:", "Building List:", "Hot Keys:", "Load Game:", "old save:",
    "Stockpile Settings:", "Assign Trade:", "World:", "World Param:", "Command Line:", "Noble List:", "Arena Weather:",
    "Building Items:", "Arena Tree:", "Image Creator:", "Legends:", "World Gen:", "Setup game:", "World Generation:",
    "Choose name:", "View item:", "Trainer:", "Order:", "Unitview,", "Building,", "Designate,", "Stockpile,", "Setup,",
    "Manager,", "Work Order,", "Unitjob,", "Secondary Option", "Unrecognized ", "Missing ", "unknown", "Option ",
    "Numpad ", "Move view/cursor ", "invalid ", "incorrect ", "NULL ", "Nuked ", "Cage: ", ": REQUIRED_", ": MANDATE_",
    ": DEMAND_", "DOUBLE TAGGED ITEM:", "Patched save:"
}


def ignore_starts(string: str):
    return any(string.startswith(start) for start in forbidden_starts)


blacklist_full_string = {
    "bad allocation", "bad array new length", "Out of memory - aborting", "Fatal Error", "nameless",
    "string too long", "invalid string position", "!ARG", "current",

    'Exh', 'Ovx', 'Pb!', 'Pb+', 'Pb~', 'Pn!', 'Pn+', 'Pn~', 'Sw!', 'Sw+', 'Sw~', 'Tir', 'Nm-',
    'Bl+', 'B!~', 'B!+', 'Pz+', 'Fnt', 'Pal', 'Bl~', 'Nm~', 'Nm+', 'Slg', 'Pz~',

    "scrollx", "scrolly", "buildreq", "jobvalue", "version", "gview", "assignbuildingjobs", "year", "assigndesjobs",
    "weathertimer", "season", "line", "linechar", "scrollz", "linelim", "gametype", "point", "gamemode", "cursor",
    "modejob", "modeitem", "addingtask", "modeseason", "selectingtaskobject", "paused", "modepage", "modestation",
    "squadcount", "modeview", "modeunit", "game", "gps", "plotinfo", "world", "itemmade", "olookz", "oscrollx",
    "olookx", "olooky", "menuposition", "looklist", "unitprintstack", "title", "init", "mainview", "texture",
    "interactitem", "interactinvslot", "throwitem", "dunginv", "page", "oscrolly", "oscrollz", "updatelightstate",
    "handleannounce", "preserveannounce", "manucomp", "enabler",

    "Empty biased index vector", "Unknown exception", "bad cast",
    
    "data", "region", "text", "raw", 'site-', 'feature-',
    
    'Backspace', 'Enter', 'Up', 'Delete', 'Leftbracket', 'Backslash', 'Rightbracket', 'Caret', 'Underscore',
    'Backquote', 'Rshift', 'Lshift', 'Rctrl', 'Lctrl', 'Ralt', 'Lalt', 'Rmeta', 'Lmeta', 'Numlock', 'Capslock',
    'Scrollock', 'Down', 'Right', 'Insert', 'End', 'Page Up', 'Page Down', 'Euro', 'Undo', 'Lsuper', 'Rsuper',
    'Print', 'Sysreq', 'Menu', 'Space', 'Tab', 'Shift+', 'Ctrl+', 'Alt+', 'Question', 'Quotedbl', 'Hash', 'Ampersand',
    'Quote', 'Leftparen', 'Rightparen', 'Left'
}


def ignore_by_blacklist_full_string(string):
    return string in blacklist_full_string


blacklisted_words = {'error', 'overflow', 'token', 'null', 'sdl', 'REJECTION', 'font', 'Font'}


def ignore_by_blacklisted_words(string):
    words = re.findall(r'\w+', string.lower())
    return any(blacklisted in words for blacklisted in blacklisted_words)


allowed_short_words = {
    'A', 'a', 'an', 'er', 'us', 'i',  # sarcofag-us, sacrofag-i
    'as', 'in', 'st', 'is', "'s", 's', 'es',
    'nd', 'rd', 'th', 'me', 'my', 'no', 'to', 'b.', 'd.',
    'At', 'Up', 'On', 'of', 'at', 'by', 'on',
    'I', 'He', 'he', 'We', 'it', 'It',
    'No',
    's]',
}


def ignore_short_words(string):
    return len(string) <= 2 and string.strip() not in allowed_short_words


blacklisted_substrings = {
    'placed out of bounds', 'set to default', 'Patched save'
}

def ignore_by_blacklisted_substrings(string):
    return any(substring in string for substring in blacklisted_substrings)


all_rules_list = [ignore_xml, ignore_square_brackets, ignore_paths, ignore_tags, ignore_filenames, ignore_gl,
                  ignore_underline_separated_words, ignore_camel_case, ignore_word_with_number, ignore_starts,
                  ignore_by_blacklist_full_string, ignore_by_blacklisted_words, ignore_short_words, ignore_dash_prepended_strings,
                  ignore_by_blacklisted_substrings]


def all_ignore_rules(string):
    return any(rule(string) for rule in all_rules_list)

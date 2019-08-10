import re
from .parse_raws import is_translatable


def ignore_xml(string):
    result = re.search(r"""<(\?xml .*|[\w/]+)>""", string)
    return result is not None


def test_ignore_xml():
    assert ignore_xml("""<?xml version="1.0" encoding='CP437'?>""") is True
    assert ignore_xml("No love   <->    Loves easily") is False
    assert ignore_xml("<local_id>") is True
    assert ignore_xml("</local_id>") is True
    assert ignore_xml("<type>mead hall</type>") is True
    assert ignore_xml("<no uniforms>") is False


square_brackets_exceptions = {"DONE", "MORE", "CAN'T WORK", "WITH YOU", "LIP", "REQUIRE", "DEMAND", "MANDATE",
                              "TRADING", "PENDING"}


def ignore_square_brackets(string):
    if not any(char in string for char in '[]:'):
        return False
    string = string.replace(r'\t', '\t')
    parts = re.split(r'[\[:\]]', string)
    return not any(is_translatable(part) or part in square_brackets_exceptions for part in parts)


def test_ignore_square_brackets():
    assert ignore_square_brackets('We have many drinks to choose from.  [You receive a list.]') is False
    assert ignore_square_brackets('[B]') is True
    assert ignore_square_brackets('[PRO_SUB]') is True
    assert ignore_square_brackets('  [You receive a detailed description.]') is False
    assert ignore_square_brackets('[CREATURE:') is True
    assert ignore_square_brackets('[C:4:0:1]') is True
    assert ignore_square_brackets(' [C:7:0:1]and is [C:3:0:0]oblivious to reality') is False
    assert ignore_square_brackets(' [DONE]') is False
    assert ignore_square_brackets(' [MORE]') is False
    assert ignore_square_brackets(" [CAN'T WORK]") is False
    assert ignore_square_brackets(" [WITH YOU]") is False
    assert ignore_square_brackets("([LIP])") is False
    assert ignore_square_brackets(r"\t\t[SYN_AFFECTED_CLASS:GENERAL_POISON]") is True
    assert ignore_square_brackets(r"\t\t[SYN_INJECTED][SYN_CONTACT][SYN_INHALED][SYN_INGESTED]") is True
    assert ignore_square_brackets("[STATE_ADJ:ALL_SOLID:frozen ") is False
    assert ignore_square_brackets("[STATE_ADJ:ALL_SOLID:") is True
    assert ignore_square_brackets(":BP:BY_CATEGORY:ALL:EYE") is True


def ignore_paths(string):
    if re.search(r'\.[a-z]{3}', string):
        return True

    if '/' not in string or ' ' in string:
        return False

    parts = re.split(r'[/.]', string)
    return all(not part or part.islower() or part == '*' for part in parts)


def test_ignore_paths():
    assert ignore_paths('/stdout.txt') is True
    assert ignore_paths('data/save/current') is True
    assert ignore_paths('data/init/interface.txt') is True
    assert ignore_paths('objects/b_detail_plan_*.txt') is True
    assert ignore_paths('/Resting') is False
    assert ignore_paths('Upright Spear/Spike') is False
    assert ignore_paths('Track/Ramp (NW)') is False
    assert ignore_paths('Unknown Body Group/Relation Token(s): ') is False
    assert ignore_paths('data/save/*.*') is True
    assert ignore_paths('.bmp') is True
    assert ignore_paths('grinding.') is False


ignore_tags_exceptions = {'CLT'}


def ignore_tags(string):
    return len(string) > 2 and string not in ignore_tags_exceptions and re.fullmatch('[A-Z_]+', string)


def ignore_filenames(string):
    return re.fullmatch(r".+\.[\w]{3}", string) is not None


def test_ignore_filenames():
    assert ignore_filenames("-detailed.bmp") is True


def ignore_gl(string):
    return re.fullmatch(r"(w?gl[A-Z]|W?GL_)[\w]+", string) is not None


def ignore_underline_separated_words(string):
    return re.fullmatch(r"[A-Za-z0-9]+_.*", string) is not None


def test_ignore_underline_separated_words():
    assert ignore_underline_separated_words("index1_11") is True


def ignore_dash_prepended_strings(string):
    return re.fullmatch(r"-[a-z_]+-?", string) is not None


def test_ignore_dash_prepended_strings():
    assert ignore_dash_prepended_strings('-world_sites_and_pops') is True
    assert ignore_dash_prepended_strings('-site_map-') is True


def ignore_camel_case(string):
    return re.fullmatch(r"[A-Z][a-z]+[A-Z].*", string) is not None


def test_ignore_camel_case():
    assert ignore_camel_case("InitializeConditionVariable") is True
    assert ignore_camel_case("Initialize") is False
    assert ignore_camel_case("SleepConditionVariableCS") is True
    assert ignore_camel_case("CAPS") is False
    assert ignore_camel_case("RefusedID/") is True


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
    ": DEMAND_",
}


def ignore_starts(string: str):
    return any(string.startswith(start) for start in forbidden_starts)


blacklist = {
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

    "Empty biased index vector", "Unknown exception", "bad cast", "data",
}


def ignore_by_blacklist(string):
    return string in blacklist


blacklisted_words = {'error', 'overflow', 'token', 'null', 'sdl'}


def ignore_by_blacklisted_words(string):
    words = re.findall(r'\w+', string.lower())
    return any(blacklisted in words for blacklisted in blacklisted_words)


def test_ignore_by_blacklisted_words():
    assert ignore_by_blacklisted_words("*** Error(s) finalizing the creature ") is True


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


all_rules_list = [ignore_xml, ignore_square_brackets, ignore_paths, ignore_tags, ignore_filenames, ignore_gl,
                  ignore_underline_separated_words, ignore_camel_case, ignore_word_with_number, ignore_starts,
                  ignore_by_blacklist, ignore_by_blacklisted_words, ignore_short_words, ignore_dash_prepended_strings]


def all_ignore_rules(string):
    return any(rule(string) for rule in all_rules_list)


def test_all_ignore_rules():
    assert all_ignore_rules('any text') is False
    assert all_ignore_rules('Any text') is False
    assert all_ignore_rules('Any text.') is False
    assert all_ignore_rules('Another string: just a test') is False

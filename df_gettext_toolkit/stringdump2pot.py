import sys

from .po import save_pot
from .df_ignore_string_rules import ignore_all

with open(sys.argv[1]) as stringdump:
    template = (line.rstrip('\n') for line in stringdump)
    ignore_rules = ignore_all if '--no-ignore' not in sys.argv else lambda s: False

    with open('DwarfFortress.pot', 'w', encoding='utf-8') as potfile:
        save_pot(potfile, (line for line in template if not ignore_rules(line)))

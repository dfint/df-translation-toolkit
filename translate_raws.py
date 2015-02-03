import sys

from dfgettext import *

if len(sys.argv)<2:
    sys.exit()

dictionary = {(item['msgid'],item['msgctxt']):item['msgstr'] for item in LoadMO(sys.argv[1])}

for line in translate_raw_file(sys.stdin, dictionary):
    print(line)

import sys
import os

from dfgettext import *

if len(sys.argv)<2:
    path = '.'
else:
    path = sys.argv[1]

raws = filter(lambda x: not x.startswith('language_'), os.listdir(path))

for file_name in raws:
    fullpath = os.path.join(path, file_name)
    if os.path.isfile(fullpath) and file_name.endswith('.txt'):
        with open(fullpath) as file:
            for context, item in ExtractTranslatablesFromRaws(file):
                print('#:', file_name)
                print(FormatPO(msgid=item, msgstr="", msgctxt=context))

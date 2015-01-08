import sys

from dfgettext import *

for context, item in ExtractTranslatablesFromRaws(sys.stdin):
    print(FormatPO(msgid=item,msgstr="",msgctxt=context))

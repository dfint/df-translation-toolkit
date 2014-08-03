import sys

from dfgettext import *

for context, item in ExtractTranslatablesFormRaws(sys.stdin):
    print(FormatPO(msgid=item,msgstr="",msgctxt=context))

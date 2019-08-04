import sys
import os
import shutil

from .parse_raws import translate_raw_file
from .po import load_po
from .fix_translated_strings import cleanup_string


def translate_raws(pofilename, path, encoding, silent=False):
    with open(pofilename, 'r', encoding='utf-8') as pofile:
        dictionary = {(item['msgid'],item['msgctxt']): item['msgstr'] for item in load_po(pofile)}
    
    raws = filter(lambda x: not x.startswith('language_'), os.listdir(path))
    for file_name in raws:
        basename, ext = os.path.splitext(file_name)
        if ext == '.txt':
            bak_name = os.path.join(path, basename+'.bak')
            raw_file = os.path.join(path, file_name)
            
            if not os.path.exists(bak_name):
                shutil.copy(raw_file, bak_name)
            
            with open(bak_name) as src:
                with open(raw_file, 'w', encoding=encoding) as dest:
                    yield file_name
                    for line in translate_raw_file(src, dictionary):
                        line = cleanup_string(line)
                        try:
                            print(line, file=dest)
                        except UnicodeEncodeError as e:
                            line = line.encode(encoding, errors='backslashreplace').decode(encoding)
                            print('Some characters of this line: %r '
                                  'cannot be represented in cp%d. Using backslashreplace mode.' %
                                  (line, encoding), file=sys.stderr)
                            
                            print(line, file=dest)

if __name__ == "__main__":
    if len(sys.argv)<4:
        sys.exit()
    
    pofilename = sys.argv[1]
    path = sys.argv[2]
    encoding = sys.argv[3]
    for filename in translate_raws(pofilename, path, encoding):
        print(filename, file=sys.stderr)
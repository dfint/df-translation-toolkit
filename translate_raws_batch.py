import os
import sys
from translate_raws import translate_raws
from translate_plain_text import translate_plain_text

base_path = sys.argv[1]
po_file_path = sys.argv[2]
encoding = 'cp1251' if len(sys.argv) < 4 else sys.argv[3]

lang_prefix = 'ru'

patterns = {
    r'raw\objects': dict(
        po_filename=lang_prefix+'-raw-objects.po',
        func=translate_raws,
    ),
    r'data_src': dict(
        po_filename=lang_prefix+'-uncompressed.po',
        func=lambda *args: translate_plain_text(*args, join_paragraphs=True),
    ),
    r'data\speech': dict(
        po_filename=lang_prefix+'-speech.po',
        func=lambda *args: translate_plain_text(*args, join_paragraphs=False),
    ),
    r'raw\objects\text': dict(
        po_filename=lang_prefix+'-text.po',
        func=lambda *args: translate_plain_text(*args, join_paragraphs=False),
    ),
}

for cur_dir, _, files in os.walk(base_path):
    for pattern in patterns:
        if cur_dir.endswith(pattern):
            print(cur_dir, file=sys.stderr)
            print(file=sys.stderr)
            po_filename =  os.path.join(po_file_path, patterns[pattern]['po_filename'])
            func = patterns[pattern]['func']
            func(po_filename), cur_dir, encoding)
            print(file=sys.stderr)

import os
import sys
from translate_raws import translate_raws

base_path = sys.argv[1]
po_file_name = sys.argv[2]

for cur_dir, _, files in os.walk(base_path):
    if cur_dir.endswith(r'raw\objects'):
        print(cur_dir, file=sys.stderr)
        print(file=sys.stderr)
        translate_raws(po_file_name, cur_dir, 'cp1251')
        print(file=sys.stderr)

import os
import sys
from translate_raws import translate_raws

po_file_name = r'..\python-transifex\ru-raw-objects.po'
base_path = r"d:\Games\PeridexisErrant's Starter Pack 0.42.05-r01"

for cur_dir, _, files in os.walk(base_path):
    if cur_dir.endswith(r'raw\objects'):
        print(cur_dir, file=sys.stderr)
        print(file=sys.stderr)
        translate_raws(po_file_name, cur_dir, 'cp1251')
        print(file=sys.stderr)

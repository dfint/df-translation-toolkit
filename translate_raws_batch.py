import os
import sys
from translate_raws import translate_raws

po_file_name = r'..\python-transifex\ru-raw-objects.po'
base_path = r"d:\Games\PeridexisErrant's Starter Pack 0.42.05-r01"

tilesets_path = os.path.join(base_path, 'LNP\graphics')
dirs = [os.path.join(tilesets_path, x, r'raw\objects') for x in list(os.listdir(tilesets_path))]
dirs += [os.path.join(base_path, 'Dwarf Fortress 0.42.05', r'raw\objects')]

for dir in dirs:
    print(dir+':', file=sys.stderr)
    print('', file=sys.stderr)
    translate_raws(po_file_name, dir, 'cp1251')
    print('', file=sys.stderr)

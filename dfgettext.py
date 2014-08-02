def LoadDSV(filename, delimiter='|'):
    with open(filename,'r', encoding='cp1251') as dsv:
        for line in dsv:
            if '|' in line:
                parts = line.split(delimiter)
                yield parts

def LoadFromTrans(filename):
    return {line[1]:line[2:] for line in LoadDSV(filename)}

def LoadStringDump(filename):
    return [line[:2] for line in LoadDSV(filename)]

# def LoadPO(filename):
    # st_msgid = 1
    # st_msgstr = 2
    # state = None
    # with open(filename, 'r', encoding='cp65001') as pofile:
        # for line in pofile:

def read_uint(file_object):
    return int.from_bytes(file_object.read(4), byteorder='little')

def LoadMO(filename):
    def load_string(file_object, offset):
        file_object.seek(offset)
        string_size = read_uint(file_object)
        string_offset = read_uint(file_object)
        file_object.seek(string_offset)
        return file_object.read(string_size).decode(encoding="utf-8")
    
    with open(filename,'rb') as mofile:
        magic_number = mofile.read(4)
        if magic_number != b'\xde\x12\x04\x95':
            return None
        mofile.seek(8)
        number_of_strings = read_uint(mofile)
        original_string_table_offset = read_uint(mofile)
        traslation_string_table_offset = read_uint(mofile)
        for i in range(number_of_strings):
            original_string = load_string(mofile, original_string_table_offset+i*8)
            translation_string = load_string(mofile, traslation_string_table_offset+i*8)
            yield (original_string, translation_string)

def EscapeQuotes(s):
    if '\\' in s:
        s=s.replace('\\','\\\\')
    if '"' in s:
        s=s.replace('"','\\"')
    return s

def SavePO(filename,template,dictionary,ignorelist):
    with open(filename,'w',encoding='cp65001') as pofile:
        print('msgid ""', file=pofile)
        print('msgstr ""', file=pofile)
        print('"Content-Type: text/plain; charset=UTF-8\\n"', file=pofile)
        print('"Language: ru_RU\\n"', file=pofile)
        for id, text in template:
            if text not in ignorelist:
                print('', file=pofile)
                if text in dictionary and len(dictionary[text])>1: 
                    for item in dictionary[text][1:]:
                        if len(item.strip())>0:
                            print('#',item.strip(), file=pofile) # translator comments
                print('msgid "%s"' % EscapeQuotes(text), file=pofile)
                if text in dictionary:
                    print('msgstr "%s"' % EscapeQuotes(dictionary[text][0]), file=pofile)
                else:
                    print('msgstr ""', file=pofile)

def SavePOT(filename,template,ignorelist):
    with open(filename,'w',encoding='cp65001') as pofile:
        print('msgid ""', file=pofile)
        print('msgstr ""', file=pofile)
        print('"Content-Type: text/plain; charset=UTF-8\\n"', file=pofile)
        for id, text in template:
            if text not in ignorelist:
                print('', file=pofile)
                print('msgid "%s"' % EscapeQuotes(text), file=pofile)
                print('msgstr ""', file=pofile)

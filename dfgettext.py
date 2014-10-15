import sys

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

def FormatPO(msgid, msgstr="", msgctxt=None):
    s = ""
    if msgctxt:
        s += 'msgctxt "%s"\n' % EscapeQuotes(msgctxt)
    s += 'msgid "%s"\n' % EscapeQuotes(msgid)
    s += 'msgstr "%s"\n' % EscapeQuotes(msgstr)
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

# Working with raws
def tags(s):
    tag_start = None
    for i, char in enumerate(s):
        if tag_start is None:
            if char=='[':
                tag_start = i
            else:
                pass
        elif char==']':
            yield s[tag_start+1:i].split(':')
            tag_start = None

def is_translatable(s):
    return any((char>='a' and char<='z') for char in s)

def bracket_tag(tag):
    return "[%s]" % ':'.join(tag)

def ExtractTranslatablesFormRaws(file):
    object = None
    context = None
    for line in file:
        for tag in tags(line):
            if tag[0] == 'OBJECT':
                object = tag[1]
            elif object and (tag[0] == object or (object in {'ITEM','BUILDING'} and tag[0].startswith(object))) or \
                    object.endswith('_'+tag[0]):
                context = ':'.join(tag) # don't enclose context string into brackets - transifex dislike this
            elif 'TILE' not in tag[0] and any(is_translatable(s) for s in tag[1:]):
                yield (context, bracket_tag(tag))

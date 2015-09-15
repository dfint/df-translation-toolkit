def load_dsv(file, delimiter='|'):
    for line in file:
        if '|' in line:
            parts = line.split(delimiter)
            yield parts


def load_trans(file):
    return {line[1]: line[2:] for line in load_dsv(file)}


def load_string_dump(file):
    return (line[:2] for line in load_dsv(file))


def read_uint(file_object):
    return int.from_bytes(file_object.read(4), byteorder='little')


def load_mo(mofile):
    def load_string(file_object, offset):
        file_object.seek(offset)
        string_size = read_uint(file_object)
        string_offset = read_uint(file_object)
        file_object.seek(string_offset)
        return file_object.read(string_size).decode(encoding="utf-8")
    
    mofile.seek(0)
    magic_number = mofile.read(4)
    if magic_number != b'\xde\x12\x04\x95':
        raise IOError("Wrong mo-file format")
    
    mofile.seek(8)
    number_of_strings = read_uint(mofile)
    original_string_table_offset = read_uint(mofile)
    traslation_string_table_offset = read_uint(mofile)
    for i in range(number_of_strings):
        original_string = load_string(mofile, original_string_table_offset + i * 8)
        translation_string = load_string(mofile, traslation_string_table_offset + i * 8)
        if '\x04' in original_string:
            context, original_string = original_string.split('\x04')
        else:
            context = None
        yield dict(msgctxt=context, msgid=original_string, msgstr=translation_string)


def escape_quotes(s):
    if '\\' in s:
        s = s.replace('\\', '\\\\')
    if '"' in s:
        s = s.replace('"', '\\"')
    return s


def format_po(msgid, msgstr="", msgctxt=None):
    s = ""
    if msgctxt:
        s += 'msgctxt "%s"\n' % escape_quotes(msgctxt)
    s += 'msgid "%s"\n' % escape_quotes(msgid)
    s += 'msgstr "%s"\n' % escape_quotes(msgstr)
    return s


def save_po(pofile, template, dictionary, ignorelist=None):
    if not ignorelist:
        ignorelist = {}
    
    print('msgid ""', file=pofile)
    print('msgstr ""', file=pofile)
    print('"Content-Type: text/plain; charset=UTF-8\\n"', file=pofile)
    print('"Language: ru_RU\\n"', file=pofile)
    for id, text in template:
        if text not in ignorelist:
            print('', file=pofile)
            if text in dictionary and len(dictionary[text]) > 1:
                for item in dictionary[text][1:]:
                    if len(item.strip()) > 0:
                        print('#', item.strip(), file=pofile)  # translator comments
            print('msgid "%s"' % escape_quotes(text), file=pofile)
            if text in dictionary:
                print('msgstr "%s"' % escape_quotes(dictionary[text][0]), file=pofile)
            else:
                print('msgstr ""', file=pofile)


def save_pot(pofile, template, ignorelist):
    print('msgid ""', file=pofile)
    print('msgstr ""', file=pofile)
    print('"Content-Type: text/plain; charset=UTF-8\\n"', file=pofile)
    for id, text in template:
        if text not in ignorelist:
            print('', file=pofile)
            print('msgid "%s"' % escape_quotes(text), file=pofile)
            print('msgstr ""', file=pofile)


def split_tag(s):
    return s.strip('[]').split(':')


# Working with raws
def tags(s):
    tag_start = None
    for i, char in enumerate(s):
        if tag_start is None:
            if char == '[':
                tag_start = i
            else:
                pass
        elif char == ']':
            yield split_tag(s[tag_start:i])
            tag_start = None


translatable_tags = {'SINGULAR', 'PLURAL', 'STP', 'NO_SUB', 'NP', 'NA'}


def is_translatable(s):
    return s in translatable_tags or any((char >= 'a' and char <= 'z') for char in s)


def bracket_tag(tag):
    return "[%s]" % ':'.join(tag)


def last_sutable(s, func):
    for i in range(len(s)-1,0,-1):
        if func(s[i]):
            return i+1  # if the last element is sutable, then return len(s), so that s[:i] gives full list
    else:
        return 0  # if there aren't sutable elements, then return 0, so that s[:i] gives empty list


def extract_translatables_from_raws(file):
    object = None
    context = None
    keys = set()
    for line in file:
        for tag in tags(line):
            if tag[0] == 'OBJECT':
                object = tag[1]
            elif object and (tag[0] == object or (object in {'ITEM', 'BUILDING'} and tag[0].startswith(object)) or
                                 object.endswith('_' + tag[0])):
                context = ':'.join(tag)  # don't enclose context string into brackets - transifex dislike this
                keys.clear()
            elif 'TILE' not in tag[0] and any(is_translatable(s) for s in tag[1:]) and tuple(tag) not in keys:
                if not is_translatable(tag[-1]):
                    last = last_sutable(tag, is_translatable)
                    tag = tag[:last]
                    tag.append('')  # Add an empty element to the tag to mark the tag as not completed
                keys.add(tuple(tag))
                yield (context, bracket_tag(tag))

import re

re_leading_spaces = re.compile("^([^\[]*)\[")

def translate_raw_file(file, dictionary):
    object = None
    context = None
    for line in file:
        if '[' in line:
            result = re_leading_spaces.search(line)
            s = result.group(1)
            for tag in tags(line):
                if tag[0] == 'OBJECT':
                    object = tag[1]
                elif object and (tag[0] == object or (object in {'ITEM', 'BUILDING'} and tag[0].startswith(object)) or
                                     object.endswith('_' + tag[0])):
                    context = ':'.join(tag)
                
                br_tag = bracket_tag(tag)
                if any(is_translatable(s) for s in tag[1:]):
                    key = (br_tag, context)
                    if key in dictionary:
                        br_tag = dictionary[key]
                    elif (br_tag, None) in dictionary:
                        br_tag = dictionary[(br_tag, None)]
                    elif not is_translatable(tag[-1]):
                        last = last_sutable(tag, is_translatable)
                        new_tag = tag[:last+1]
                        new_tag[-1] = ''
                        br_tag = bracket_tag(new_tag)
                        key = (br_tag, context)
                        new_tag = None
                        if key in dictionary:
                            new_tag = split_tag(dictionary[key])
                        elif (br_tag, None) in dictionary:
                            new_tag = split_tag(dictionary[(br_tag, None)])
                        
                        if new_tag:
                            tag[:len(new_tag)-1] = new_tag[:-1]
                            br_tag = bracket_tag(tag)
                
                s += br_tag
            yield s
        else:
            yield line.rstrip()


import re


def load_dsv(file, delimiter='|'):
    for line in file:
        if '|' in line:
            parts = line.split(delimiter)
            yield parts


def load_trans(file):
    return {line[1]: line[2:] for line in load_dsv(file)}


def load_string_dump(file):
    return (line[:2] for line in load_dsv(file))


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
    return s in translatable_tags or any('a' <= char <= 'z' for char in s)


def bracket_tag(tag):
    return "[%s]" % ':'.join(tag)


def last_suitable(s, func):
    for i in range(len(s)-1, 0, -1):
        if func(s[i]):
            return i+1  # if the last element is sutable, then return len(s), so that s[:i] gives full list
    else:
        return 0  # if there aren't sutable elements, then return 0, so that s[:i] gives empty list


def extract_translatables_from_raws(file):
    obj = None
    context = None
    keys = set()
    for i, line in enumerate(file, 1):
        for tag in tags(line):
            if tag[0] == 'OBJECT':
                obj = tag[1]
            elif obj and (tag[0] == obj or (obj in {'ITEM', 'BUILDING'} and tag[0].startswith(obj)) or
                          obj.endswith('_' + tag[0])):
                context = ':'.join(tag)  # don't enclose context string into brackets - transifex dislike this
                keys.clear()
            elif 'TILE' not in tag[0] and any(is_translatable(s) for s in tag[1:]) and tuple(tag) not in keys:
                if not is_translatable(tag[-1]):
                    last = last_suitable(tag, is_translatable)
                    tag = tag[:last]
                    tag.append('')  # Add an empty element to the tag to mark the tag as not completed
                keys.add(tuple(tag))
                yield (context, bracket_tag(tag), i)

re_leading_spaces = re.compile("^([^\[]*)\[")


def translate_raw_file(file, dictionary):
    obj = None
    context = None
    for line in file:
        if '[' in line:
            result = re_leading_spaces.search(line)
            s = result.group(1)
            for tag in tags(line):
                if tag[0] == 'OBJECT':
                    obj = tag[1]
                elif obj and (tag[0] == obj or (obj in {'ITEM', 'BUILDING'} and tag[0].startswith(obj)) or
                              obj.endswith('_' + tag[0])):
                    context = ':'.join(tag)
                
                br_tag = bracket_tag(tag)
                if any(is_translatable(s) for s in tag[1:]):
                    key = (br_tag, context)
                    if key in dictionary:
                        br_tag = dictionary[key]
                    elif (br_tag, None) in dictionary:
                        br_tag = dictionary[(br_tag, None)]
                    elif not is_translatable(tag[-1]):
                        last = last_suitable(tag, is_translatable)
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


def skip_tags(s):
    opened = 0
    for char in s:
        if char == '[':
            opened += 1
        elif char == ']':
            opened -= 1
        elif opened == 0:
            yield char


def parse_plain_text_file(file, join_paragraphs=True):
    is_translatable = lambda s: any(char.islower() for char in skip_tags(s))
    paragraph = ''
    if join_paragraphs:
        line = file.readline()  # The first line with the file name
        yield line, False
    
    for line in file:
        if join_paragraphs:
            if is_translatable(line):
                if '~' in line or line[0] == '[' and not (paragraph and paragraph.rstrip()[-1].isalpha()):
                    if paragraph:
                        yield paragraph, True
                        paragraph = ''
                    
                    if line.rstrip().endswith(']'):
                        yield line, True
                    else:
                        paragraph += line
                else:
                    paragraph += line
            else:
                if paragraph:
                    yield paragraph, True
                    paragraph = ''
                
                yield line, False  # Not translatable line
        else:
            yield line, is_translatable(line)
    
    if paragraph:
        yield paragraph, True

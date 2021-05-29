def load_dsv(file, delimiter='|'):
    for line in file:
        if '|' in line:
            parts = line.split(delimiter)
            yield parts


def load_trans(file):
    return {line[1]: line[2:] for line in load_dsv(file)}


def load_string_dump(file):
    return (line[:2] for line in load_dsv(file))

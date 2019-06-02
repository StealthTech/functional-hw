def load(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return [line for line in lines.split('\n') if line]


def dump(lst, filename):
    with open(filename, 'w') as f:
        f.writelines(wrap_lines(lst))


def wrap_lines(lst):
    return [
        f'{elem}\n' for elem in lst
    ]


def print_multiline(lst):
    print('\n'.join(map(str, lst)))


def construct_from_line(cls, line):
    args = line.split(', ')
    return cls(*args)


def extract_models(cls, lines):
    return [
        construct_from_line(cls, line) for line in lines
    ]


def parse_ids(s):
    spl = [elem for elem in s.split(':') if elem]
    return list(sorted(map(int, spl)))


def get_instance_by_id(pk, lst):
    return list(filter(lambda x: x.pk == pk, lst))[0]


def intersection_rank(a, b):
    return len(set(a) & set(b))

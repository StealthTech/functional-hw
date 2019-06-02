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


def estimate_relation_value(student, teacher):
    value = 0

    # Если любимые темы студента совпадают с нелюбимыми темами преподавателя
    value += -10 * intersection_rank(student.themes_positive, teacher.themes_negative)
    # Если любимые темы преподавателя совпадают с нелюбимыми темами студента
    value += -10 * intersection_rank(teacher.themes_positive, student.themes_negative)
    # Если любимые темы студента совпадают с любимыми темами преподавателя
    value += 10 * intersection_rank(student.themes_positive, teacher.themes_positive)

    # Если преподаватель и студент испытывают друг к другу неприятие
    value += -100 * (
            intersection_rank(student.teachers_negative, [teacher.pk]) +
            intersection_rank(teacher.students_negative, [student.pk])
    )

    # Если преподаватель и студент испытывают друг к другу симпатию
    value += 100 * (
            intersection_rank(student.teachers_positive, [teacher.pk]) +
            intersection_rank(teacher.students_positive, [student.pk])
    )
    return value


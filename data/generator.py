import random

pool_first_name = [
    'Иван',
    'Михаил',
    'Дмитрий',
    'Александр',
    'Никита',
    'Юрий',
    'Евгений'
]

pool_middle_name = [
    'Иванович',
    'Михайлович',
    'Дмитриевич',
    'Александрович',
    'Никитич',
    'Юрьевич',
    'Евгеньевич',
]

pool_last_name = [
    'Иванов',
    'Петров',
    'Сидоров',
]

pool_themes = [
    'Физика',
    'Математика',
    'Программирование',
    'Базы данных',
    'Аналитика',
    'Политология',
    'История',
]


def _generate_full_name():
    return ' '.join((
        random.choice(pool_first_name),
        random.choice(pool_middle_name),
        random.choice(pool_last_name),
    ))


def _generate_themes(count, themes_lst):
    return random.sample(themes_lst, count)


def prepare_themes():
    return [
        {'id': idx + 1, 'name': theme_name} for idx, theme_name in enumerate(pool_themes)
    ]


def generate_split_themes(max_count, themes_lst):
    theme_count = random.randint(0, max_count)
    themes = _generate_themes(theme_count, themes_lst)
    half_idx = int(len(themes) / 2)
    themes_positive = themes[:half_idx]
    themes_negative = themes[half_idx:]
    return themes_positive, themes_negative


def generate_relations(max_count, teachers_lst, students_lst):
    for student in students_lst:
        relations_count = random.randint(0, max_count)
        _teachers = random.sample(teachers_lst, relations_count)
        teachers_positive, teachers_negative = justify(_teachers)
        student['teachers_positive'] = extract_ids(teachers_positive)
        student['teachers_negative'] = extract_ids(teachers_negative)

    for teacher in teachers_lst:
        relations_count = random.randint(0, max_count)
        _students = random.sample(students_lst, relations_count)
        students_positive, students_negative = justify(_students)
        teacher['students_positive'] = extract_ids(students_positive)
        teacher['students_negative'] = extract_ids(students_negative)


def justify(lst):
    half_idx = int(len(lst) / 2)
    return lst[:half_idx], lst[half_idx:]


def extract_ids(lst):
    return [elem.get('id') for elem in lst]


def generate_teachers(count, themes_lst):
    result = []
    for i in range(count):
        max_themes_count = 4
        themes_positive, themes_negative = generate_split_themes(max_themes_count, themes_lst)

        result.append({
            'id': i + 1,
            'name': _generate_full_name(),
            'themes_positive': extract_ids(themes_positive),
            'themes_negative': extract_ids(themes_negative),
            'students_positive': [],
            'students_negative': [],
        })
    return result


def generate_students(count, themes_lst):
    result = []
    for i in range(count):
        max_themes_count = 4
        themes_positive, themes_negative = generate_split_themes(max_themes_count, themes_lst)

        result.append({
            'id': i + 1,
            'name': _generate_full_name(),
            'themes_positive': extract_ids(themes_positive),
            'themes_negative': extract_ids(themes_negative),
            'teachers_positive': [],
            'teachers_negative': [],
        })
    return result


def flatten(obj):
    if type(obj) == list:
        return ':'.join([
            flatten(elem) for elem in obj
        ])

    if type(obj) == dict:
        result = []
        for k, v in obj.items():
            result.append(flatten(v))
        return ', '.join(result)

    return str(obj)


def wrap_lines(lst):
    return [
        f'{elem}\n' for elem in lst
    ]


def dump(lst, filename):
    with open(filename, 'w') as f:
        f.writelines(wrap_lines(lst))


if __name__ == '__main__':
    themes = prepare_themes()

    teachers_count = 40  # по условию
    teachers = generate_teachers(teachers_count, themes)

    students_count = 140  # по условию
    students = generate_students(students_count, themes)

    max_relations = 4  # примерное значение
    generate_relations(max_relations, teachers, students)

    dump([
        flatten(elem) for elem in teachers
    ], 'teachers.csv')

    dump([
        flatten(elem) for elem in students
    ], 'students.csv')

    dump([
        flatten(elem) for elem in themes
    ], 'themes.csv')

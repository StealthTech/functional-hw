import os

import utils
from models import Theme, Teacher, Student


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)

    # Загрузка тем
    themes_data = utils.load('../data/themes.csv')
    themes = utils.extract_models(Theme, themes_data)
    utils.print_multiline(themes)

    # Загрузка преподавателей
    teachers_data = utils.load('../data/teachers.csv')
    teachers = utils.extract_models(Teacher, teachers_data)
    utils.print_multiline(teachers[:10])

    # Загрузка студентов
    students_data = utils.load('../data/students.csv')
    students = utils.extract_models(Student, students_data)
    utils.print_multiline(students[:10])

    # Расчет отношений
    _students = students
    lines = []
    for idx, _student in enumerate(_students):
        min_students_count = min(map(lambda x: len(x.current_students), teachers))
        _teachers = filter(lambda x: not x.is_cap_reached and len(x.current_students) == min_students_count, teachers)

        values = sorted([
            (_teacher, utils.estimate_relation_value(_student, _teacher))
            for _teacher in _teachers
        ], key=lambda x: x[1], reverse=True)

        _teacher, value = values[0]  # обратная деструктуризация
        _teacher.current_students.append(_student)
        _student.current_teacher = _teacher

        lines.append('\t'.join(map(str, [
            idx + 1, _student.pk, _teacher.pk, value
        ])))

        print(f'{idx + 1} :: pair found :: Оценка {value} :: {_student} // {_teacher}')
    utils.dump(lines, 'output/relations.csv')

    print('- ' * 30)

    for idx, _teacher in enumerate(teachers):
        print(f'{idx + 1} :: Количество {len(_teacher.current_students)} :: {_teacher}')
    print(f'Валидация: {sum(map(lambda x: len(x.current_students), teachers))} из 140 студентов распределены')

import os

import utils
from processing import calculate_relations
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

    students, teachers, lines = calculate_relations(students, teachers)

    utils.dump(lines, 'output/relations.csv')

    print('- ' * 30)

    for idx, _teacher in enumerate(teachers):
        print(f'{idx + 1} :: Количество {len(_teacher.current_students)} :: {_teacher}')
    print(f'Валидация: {sum(map(lambda x: len(x.current_students), teachers))} из 140 студентов распределены')

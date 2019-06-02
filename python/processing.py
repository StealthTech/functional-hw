import copy

from utils import intersection_rank


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


def calculate_relations(student_lst, teacher_lst):
    # Расчет отношений
    lines = []

    students = copy.deepcopy(student_lst)
    teachers = copy.deepcopy(teacher_lst)

    for idx, _student in enumerate(students):
        min_students_count = min(map(lambda x: len(x.current_students), teachers))
        _teachers = filter(lambda x: not x.is_cap_reached and len(x.current_students) == min_students_count, teachers)

        values = sorted([
            (_teacher, estimate_relation_value(_student, _teacher))
            for _teacher in _teachers
        ], key=lambda x: x[1], reverse=True)

        _teacher, value = values[0]  # обратная деструктуризация
        _teacher.current_students.append(_student)
        _student.current_teacher = _teacher

        lines.append('\t'.join(map(str, [
            idx + 1, _student.pk, _teacher.pk, value
        ])))

        print(f'{idx + 1} :: pair found :: Оценка {value} :: {_student} // {_teacher}')
    return students, teachers, lines

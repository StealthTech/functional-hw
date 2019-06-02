from utils import parse_ids


class Student:
    def __init__(self, pk, name, themes_positive, themes_negative, teachers_positive, teachers_negative):
        self.pk = int(pk)
        self.name = name
        self.themes_positive = parse_ids(themes_positive)
        self.themes_negative = parse_ids(themes_negative)
        self.teachers_positive = parse_ids(teachers_positive)
        self.teachers_negative = parse_ids(teachers_negative)

        self.current_teacher = None

    def __str__(self):
        return f'Студент ID{self.pk} :: {self.name}'


class Teacher:
    max_students_cap = 40

    def __init__(self, pk, name, themes_positive, themes_negative, students_positive, students_negative):
        self.pk = int(pk)
        self.name = name
        self.themes_positive = parse_ids(themes_positive)
        self.themes_negative = parse_ids(themes_negative)
        self.students_positive = parse_ids(students_positive)
        self.students_negative = parse_ids(students_negative)

        self.current_students = []

    def __str__(self):
        return f'Преподаватель ID{self.pk} :: {self.name}'

    @property
    def is_cap_reached(self):
        return len(self.current_students) >= self.max_students_cap


class Theme:
    def __init__(self, pk, name):
        self.pk = int(pk)
        self.name = name

    def __str__(self):
        return f'Тема ID{self.pk} :: {self.name}'


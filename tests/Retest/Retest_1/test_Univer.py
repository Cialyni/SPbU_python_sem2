import pytest

from src.Retest.Retest_1.Univer import *

UNIVER = University(
    [
        Student(
            "Ilia",
            [
                StudentCourses(
                    course_name="Math", teacher_name="Genadi Sergeevich", attendance=0.56, scores=[1, 5, 3, 4]
                ),
                StudentCourses(
                    course_name="Topology", teacher_name="Ivan Ivanovitch", attendance=0.2, scores=[5, 5, 5, 4]
                ),
                StudentCourses(
                    course_name="Algebra", teacher_name="Maksim Alexeevitch", attendance=0.1, scores=[1, 1, 3, 2]
                ),
                StudentCourses(
                    course_name="Informatica", teacher_name="Maksim Alexeevitch", attendance=0.44, scores=[1, 5, 1, 2]
                ),
            ],
        ),
        Student(
            "Masha",
            [
                StudentCourses(
                    course_name="Topology", teacher_name="Genadi Sergeevich", attendance=0.97, scores=[5, 5, 5, 4]
                ),
                StudentCourses(
                    course_name="Algebra", teacher_name="Maksim Alexeevitch", attendance=0.87, scores=[1, 4, 4, 4]
                ),
            ],
        ),
        Student(
            "Anton",
            [
                StudentCourses(
                    course_name="Algebra", teacher_name="Maksim Alexeevitch", attendance=0.65, scores=[1, 2, 3, 4]
                ),
                StudentCourses(
                    course_name="Topology", teacher_name="Genadi Sergeevich", attendance=0.45, scores=[5, 5, 1, 4]
                ),
                StudentCourses(
                    course_name="Informatica", teacher_name="Maksim Alexeevitch", attendance=0.76, scores=[1, 3, 3, 4]
                ),
            ],
        ),
    ],
    [
        Teacher(
            "Maksim Alexeevitch",
            [
                TeacherCourses(course_name="Algebra", students_names=["Masha, Anton, Ilia"]),
                TeacherCourses(course_name="Informatica", students_names=["Anton, Ilia"]),
            ],
        ),
        Teacher(
            "Genadi Sergeevich",
            [
                TeacherCourses(course_name="Math", students_names=["Ilia"]),
                TeacherCourses(course_name="Topology", students_names=["Anton, Masha"]),
            ],
        ),
        Teacher("Ivan Ivanovitch", [TeacherCourses(course_name="Topology", students_names=["Ilia"])]),
    ],
)


class TestStudent:
    @pytest.mark.parametrize(
        "student_name, course_name, expected",
        (
            ("Masha", "Math", None),
            ("Masha", "Topology", 4.75),
            ("Anton", "Topology", 3.75),
            ("Ilia", "Algebra", 1.75),
        ),
    )
    def test_find_middle_score(self, student_name, course_name, expected):
        assert UNIVER.find_student_middle_score(student_name, course_name) == expected

    @pytest.mark.parametrize(
        "student_name, course_name, expected",
        (
            ("Masha", "Math", None),
            ("Masha", "Topology", 0.97),
            ("Anton", "Topology", 0.45),
            ("Ilia", "Algebra", 0.1),
        ),
    )
    def test_find_attendance(self, student_name, course_name, expected):
        assert UNIVER.find_student_attendance(student_name, course_name) == expected

    @pytest.mark.parametrize(
        "student_name, expected",
        (
            ("aveaf", None),
            ("Masha", ["Topology", "Algebra"]),
            ("Anton", ["Algebra", "Topology", "Informatica"]),
            ("Ilia", ["Math", "Topology", "Algebra", "Informatica"]),
        ),
    )
    def test_find_student_courses(self, student_name, expected):
        assert UNIVER.find_student_courses(student_name) == expected


class TestTeacher:
    @pytest.mark.parametrize(
        "teacher_name,  expected",
        (
            ("Genadi Sergeevich", ["Math", "Topology"]),
            ("Maksim Alexeevitch", ["Algebra", "Informatica"]),
            ("Ivan Ivanovitch", ["Topology"]),
            ("adfasf", None),
        ),
    )
    def test_find_teacher_courses(self, teacher_name, expected):
        assert UNIVER.find_teacher_courses(teacher_name) == expected

    @pytest.mark.parametrize(
        "teacher_name, , expected",
        (("Genadi Sergeevich", 2), ("Maksim Alexeevitch", 2), ("Ivan Ivanovitch", 1), ("asadfsadf", None)),
    )
    def test_find_teacher_workload(self, teacher_name, expected):
        assert UNIVER.find_teacher_workload(teacher_name) == expected


class TestAdd:
    def test_add_student(self):
        UNIVER.add_student("Kriss")
        UNIVER.add_student_course("Kriss", "a", "b", 0, [1])
        assert UNIVER.find_student_attendance("Kriss", "a") == 0

    def test_add_teacher(self):
        UNIVER.add_teacher("Mihail")
        UNIVER.add_teacher_course("Mihail", "qq", ["aboba"])
        assert UNIVER.find_teacher_courses("Mihail") == ["qq"]

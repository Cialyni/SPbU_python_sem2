import pprint
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TeacherCourses:
    course_name: str
    students_names: List[str]


@dataclass
class StudentCourses:
    course_name: str
    teacher_name: str
    attendance: float
    scores: List[float]


class Teacher:
    def __init__(self, name: str, courses: List[TeacherCourses]) -> None:
        self.name = name
        self.courses = courses

    def find_courses(self) -> List[str]:
        return [course.course_name for course in self.courses]


class Student:
    def __init__(self, name: str, courses: List[StudentCourses]) -> None:
        self.name = name
        self.courses = courses

    def find_middle_score(self, course_name: str) -> float:
        for course in self.courses:
            if course.course_name == course_name:
                return sum(course.scores) / len(course.scores)
        raise ValueError("This student does not have such a subject")

    def find_attendance(self, course_name: str) -> float:
        for course in self.courses:
            if course.course_name == course_name:
                return course.attendance
        raise ValueError("This student does not have such a subject")


class University:
    def __init__(self, students: List[Student], teachers: List[Teacher]) -> None:
        self.students: List[Student] = students
        self.teachers: List[Teacher] = teachers

    def find_student_middle_score(self, student_name: str, course_name: str) -> Optional[float]:
        try:
            for student in self.students:
                if student.name == student_name:
                    return student.find_middle_score(course_name)
        except ValueError as error:
            print(error)
        else:
            print("This student does not exist")

    def find_student_attendance(self, student_name: str, course_name: str) -> Optional[float]:
        try:
            for student in self.students:
                if student.name == student_name:
                    return student.find_attendance(course_name)
        except ValueError as error:
            print(error)
        else:
            print("This student does not exist")

    def find_teacher_workload(self, teacher_name: str) -> Optional[int]:
        for teacher in self.teachers:
            if teacher.name == teacher_name:
                return len(teacher.courses)
        print("This teacher does not exist")

    def find_teacher_courses(self, teacher_name: str) -> Optional[List[str]]:
        for teacher in self.teachers:
            if teacher.name == teacher_name:
                return teacher.find_courses()

    def add_student(self, student_name: str) -> None:
        student = Student(student_name, [])
        self.students.append(student)

    def add_student_course(
        self, student_name: str, course_name: str, teacher_name: str, attendance: float, scores: List[float]
    ) -> None:
        course = StudentCourses(course_name, teacher_name, attendance, scores)
        for i, student in enumerate(self.students):
            if student.name == student_name:
                self.students[i].courses.append(course)
                break

    def add_teacher(self, teacher_name: str) -> None:
        teacher = Teacher(teacher_name, [])
        self.teachers.append(teacher)

    def add_teacher_course(self, teacher_name: str, course_name: str, students: List[str]) -> None:
        course = TeacherCourses(course_name, students)
        for i, teacher in enumerate(self.teachers):
            if teacher.name == teacher_name:
                self.teachers[i].courses.append(course)
                break

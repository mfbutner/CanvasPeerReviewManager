import canvasapi
from StudentClass import *


class AssignmentPeerReview:

    def __init__(self, course: canvasapi.course.Course, assignment):
        self.name = assignment.name
        self.assignment_id = assignment.id
        self.students = self.make_students(course, assignment)
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0

    def make_students(self, course: canvasapi.course.Course, assignment):
        students = []
        for submission in assignment.get_submissions():
            student = Student(course, assignment, submission)
            students.append(student)
        return students

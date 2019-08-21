from StudentClass import *


class AssignmentPeerReview(object):

    def __init__(self, course: canvasapi.course.Course, assignment):
        self.name = assignment.name
        self.assignment_id = assignment.id
        self.students = self.make_students(course, assignment)
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0
        self.get_peer_review_stats()

    def make_students(self, course: canvasapi.course.Course, assignment):
        students = []
        for submission in assignment.get_submissions():
            student = Student(course, assignment, submission)
            students.append(student)
        return students

    def get_peer_review_stats(self):
        # make iterable here
        data = []
        for student in self.students:
            for review in student.this_students_reviews:
                data.append(review.total_score)

        if len(data) >= 1:
            self.mean = statistics.mean(data)
            self.median = statistics.median(data)
            self.mode = statistics.mode(data)
        else:
            self.mean = "N/A"
            self.median = "N/A"
            self.mode = "N/A"
        if len(data) >= 2:
            self.std_dev = statistics.stdev(data)
        else:
            self.std_dev = "N/A"


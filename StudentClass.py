from StudentReviewClass import *
import canvasapi
import statistics


class Student(object):

    def __init__(self, course: canvasapi.course.Course, assignment, submission: canvasapi.submission):
        user_id = submission.user_id
        self.canvas_id = user_id
        self.sis_login_id = course.get_user(user_id).login_id
        self.name = course.get_user(user_id).name
        self.first, self.last = self.name.split()
        self.student_id = 0

        self.late = submission.late
        self.total = submission.score
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0
        self.get_stats()

        self.this_students_reviews = self.get_reviews(self, course, assignment, submission)
        self.rubric_stats = get_rubric_stats()

    @staticmethod
    def get_reviews(self, course: canvasapi.course.Course, assignment, submission):  # reviews have attribute "to_json"
        review_list = []

        for review in assignment.get_peer_reviews():
            student_id = review.user_id                     # get name of student for peer review
            student_name = course.get_user(student_id).name

            if self.name == student_name:           # matches name of this student to name on reviewed assignment
                reviewer = StudentReview(course, assignment, review, submission)
                review_list.append(reviewer)

        return review_list

    def get_stats(self):
        # make iterable here
        data = []
        self.mean = statistics.mean(data)
        self.median = statistics.median(data)
        self.mode = statistics.mode(data)
        self.std_dev = statistics.stdev(data)

from StudentReviewClass import *
import canvasapi
import statistics


class Student(object):

    def __init__(self, course: canvasapi.course.Course, assignment, submission: canvasapi.submission):
        user_id = submission.user_id
        self.canvas_id = user_id
        self.sis_login_id = course.get_user(user_id).login_id
        # self.name = course.get_user(user_id).name
        self.first, self.last = course.get_user(user_id).name.split()
        self.student_id = 0

        self.late = submission.late
        self.total = submission.score
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0

        # this student's reviews
        self.reviews = self.get_reviews(self, course, assignment)
        self.get_student_peer_review_stats()

    @staticmethod
    def get_reviews(self, course: canvasapi.course.Course, assignment):  # reviews have attribute "to_json"
        review_list = []

        for review in assignment.get_peer_reviews():
            student_id = review.user_id                     # get name of student for peer review
            student_name = course.get_user(student_id).name
            name = self.first + " " + self.last
            if name == student_name:           # matches name of this student to name on reviewed assignment
                reviewer = StudentReview(course, assignment, review)
                review_list.append(reviewer)

        return review_list

    def get_student_peer_review_stats(self):
        data = []
        for review in self.reviews:
            data.append(review.total_score)
        print(self.first, " ", self.last)
        print(data)

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

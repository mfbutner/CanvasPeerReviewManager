import sys
import canvasapi
import csv
import json


class Student:

    def __init__(self, course, assignment, submission):
        user_id = submission.user_id
        self.sis_login_id = course.get_user(user_id).login_id
        self.first, self.last = course.get_user(user_id).name.split()
        self.canvas_id = 0
        self.student_id = 0
        self.total = submission.score
        self.mean = self.mean_of_reviews(submission)
        self.median = self.median_of_reviews(submission)
        self.mode = self.mode_of_reviews(submission)
        self.std_dev = self.std_dev_of_reviews(submission)
        self.reviews = self.get_reviews(assignment)
        self.total_score = submission.score
        self.late = submission.late

    @staticmethod
    def get_reviews(assignment):
        review_list = []
        for review in assignment.get_peer_reviews():
            print(review.asset_type)
            print(review.assessor_id, " ", review.id)
            # if review.workflow_state == "completed":
            #     review_list.append(review.user_id)
        return review_list

    @staticmethod
    def mean_of_reviews(submission):
        mean = 0

        return mean

    @staticmethod
    def median_of_reviews(submission):
        median = 0

        return median

    @staticmethod
    def mode_of_reviews(submission):
        mode = 0

        return mode

    @staticmethod
    def std_dev_of_reviews(submission):
        std_dev = 0

        return std_dev


class AssignmentPeerReviews:

    def __init__(self, assignment):
        self.name = assignment.name
        self.assignment_id = assignment.id
        self.reviewers = []
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0


canvas = canvasapi.Canvas("https://canvas.ucdavis.edu", sys.argv[1]  )         # Make a new Canvas object
course = canvas.get_course(1599)  # Make a new Course object with course number
assignments = course.get_assignments()
assignment = assignments[0]

for submission in assignment.get_submissions():
    student = Student(course, assignment, submission)

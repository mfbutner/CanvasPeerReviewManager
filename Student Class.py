import sys
import canvasapi
import csv
import json


class Student:

    def __init__(self, course, assignment, submission):

        user_id = submission.user_id
        self.canvas_id = user_id
        self.sis_login_id = course.get_user(user_id).login_id
        self.name = course.get_user(user_id).name
        self.first, self.last = self.name.split()
        self.student_id = 0

        self.late = submission.late
        self.total = submission.score
        self.mean = self.mean_of_reviews(submission)
        self.median = self.median_of_reviews(submission)
        self.mode = self.mode_of_reviews(submission)
        self.std_dev = self.std_dev_of_reviews(submission)

        self.this_students_reviews = self.get_reviews(self, course, assignment, submission)
        self.rubric_stats = self.get_rubric_stats()

    @staticmethod
    def get_rubric_stats():
        stats = []
        return stats

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

    @staticmethod
    def get_reviews(self, course, assignment, submission):  # reviews have attribute "to_json"
        review_list = []

        for review in assignment.get_peer_reviews():
            student_id = review.user_id                     # get name of student for peer review
            student_name = course.get_user(student_id).name

            if self.name == student_name:           # matches name of this student to name on reviewed assignment
                reviewer = StudentReview(course, assignment, review)
                review_list.append(reviewer)

        return review_list


class StudentReview:

    def __init__(self, course, assignment, review):
        self.reviewer_id = review.assessor_id
        self.reviewer_name = course.get_user(self.reviewer_id).name


class AssignmentPeerReviews:

    def __init__(self, assignment):
        self.name = assignment.name
        self.assignment_id = assignment.id
        self.reviewers = []
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0


def main():
    canvas = canvasapi.Canvas("https://canvas.ucdavis.edu", sys.argv[1])
    course = canvas.get_course(1599)
    assignments = course.get_assignments()
    assignment = assignments[0]

    for submission in assignment.get_submissions():
        student = Student(course, assignment, submission)


main()

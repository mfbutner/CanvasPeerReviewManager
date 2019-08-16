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
        self.mean = mean_of_reviews(submission)
        self.median = median_of_reviews(submission)
        self.mode = mode_of_reviews(submission)
        self.std_dev = std_dev_of_reviews(submission)
        self.reviews = get_reviews(course, assignment, submission)
        self.total_score = submission.score
        self.late = submission.late
        # (assignment.rubric)[0]['points']


class AssignmentPeerReviews:

    def __init__(self, assignment):
        self.name = assignment.name
        self.assignment_id = assignment.id
        self.reviewers = []
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0


def get_reviews(course, assignment, submission):            # reviews have attribute "to_json"
    review_list = []

    for review in assignment.get_peer_reviews():
        # print(review)
        student_id = review.user_id
        student_name = course.get_user(review.user_id).name

        reviewer_id = review.assessor_id
        reviewer_name = course.get_user(review.assessor_id).name


        print(submission.get_submission_peer_reviews)
        # for submissionReview in submission.get_submission_peer_reviews():
        #     print(submissionReview)


        print()
    return review_list


def mean_of_reviews(submission):
    mean = 0

    return mean


def median_of_reviews(submission):
    median = 0

    return median


def mode_of_reviews(submission):
    mode = 0

    return mode


def std_dev_of_reviews(submission):
    std_dev = 0

    return std_dev


def main():
    canvas = canvasapi.Canvas("https://canvas.ucdavis.edu", sys.argv[1]  )         # Make a new Canvas object
    course = canvas.get_course(1599)  # Make a new Course object with course number
    assignments = course.get_assignments()
    assignment = assignments[0]

    # submissions = assignment.get_submissions()
    # student = Student(course, assignment, submissions[0])
    for submission in assignment.get_submissions():
        student = Student(course, assignment, submission)
        print("NEXT:")


main()

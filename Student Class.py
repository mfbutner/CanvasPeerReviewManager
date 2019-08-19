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

    def get_rubric_stats(self):
        stats = []
        return stats

    def mean_of_reviews(self, submission):
        mean = 0

        return mean

    def median_of_reviews(self, submission):
        median = 0

        return median

    def mode_of_reviews(self, submission):
        mode = 0

        return mode

    def std_dev_of_reviews(self, submission):
        std_dev = 0

        return std_dev

    @staticmethod
    def get_reviews(self, course, assignment, submission):  # reviews have attribute "to_json"
        review_list = []

        for review in assignment.get_peer_reviews():
            student_id = review.user_id                     # get name of student for peer review
            student_name = course.get_user(student_id).name

            if self.name == student_name:           # matches name of this student to name on reviewed assignment
                reviewer = StudentReview(course, assignment, review, submission)
                review_list.append(reviewer)

        return review_list


class StudentReview:

    def __init__(self, course, assignment, review, submission):
        self.canvas_id = review.assessor_id
        self.sis_login_id = course.get_user(self.canvas_id).login_id
        self.student_id = 0

        self.reviewer_name = course.get_user(self.canvas_id).name
        self.first, self.second = self.reviewer_name.split()

        self.rubric = self.get_reviewer_assessment(self, course, assignment, review, submission)
        self.total_score = 0

    @staticmethod
    def get_reviewer_assessment(self, course, assignment, review, submission):
        assessment = {}

        rubric_id = assignment.rubric
        r = course.get_rubric(rubric_id, include=["peer_assessments"], style="full")
        print(r.assessments["score"])

        return assessment


class AssignmentPeerReviews:

    def __init__(self, assignment):
        self.name = assignment.name
        self.assignment_id = assignment.id
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0


def main():
    canvas = canvasapi.Canvas("https://canvas.ucdavis.edu", sys.argv[1])
    course = canvas.get_course(1599)
    
    get_assignment_peer_reviews()



    # for rubric in course.get_rubrics():
    #     print(rubric)
    #
    # r = course.get_rubric(14843, include=["peer_assessments"], style="full")
    #
    # for elem in r.assessments:
    #     print(elem)
    #     print("data:", elem["data"])
    #     print()


def get_assignment_peer_reviews(course: canvasapi.course.Course, assignment_id: int):
    assignment = course.get_assignment(assignment_id)
    for submission in assignment.get_submissions():
        student = Student(course, assignment, submission)
    return 0


main()

from Main import *
import canvasapi


# makes new StudentReview object for each reviewer of a particular assignment
class StudentReview:

    def __init__(self, course: canvasapi.course.Course, assignment, review, submission):
        self.canvas_id = review.assessor_id
        self.sis_login_id = course.get_user(self.canvas_id).login_id
        self.student_id = 0

        self.reviewer_name = course.get_user(self.canvas_id).name
        self.first, self.second = self.reviewer_name.split()

        self.rubric = self.get_reviewer_assessment(self, course, assignment, review, submission)
        self.total_score = 0

    @staticmethod
    def get_reviewer_assessment(self, course: canvasapi.course.Course, assignment, review, submission):
        assessment = {}

        rubric_id = assignment.rubric
        r = course.get_rubric(rubric_id, include=["peer_assessments"], style="full")
        print(r.assessments["score"])
        return assessment

from StudentReviewClass import *
import canvasapi


class Student:

    def __init__(self, course: canvasapi.course.Course, assignment, submission: canvasapi.submission):
        user_id = submission.user_id
        self.canvas_id = user_id
        self.sis_login_id = course.get_user(user_id).login_id
        self.name = course.get_user(user_id).name
        self.first, self.last = self.name.split()
        self.student_id = 0

        self.late = submission.late
        self.total = submission.score
        self.mean = mean_of_reviews(submission)
        self.median = median_of_reviews(submission)
        self.mode = mode_of_reviews(submission)
        self.std_dev = std_dev_of_reviews(submission)

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

# for rubric in course.get_rubrics():
#     print(rubric)
#
# r = course.get_rubric(14843, include=["peer_assessments"], style="full")
#
# for elem in r.assessments:
#     print(elem)
#     print("data:", elem["data"])
#     print()

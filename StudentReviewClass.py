import canvasapi


# makes new StudentReview object for each reviewer of a particular assignment
class StudentReview(object):

    def __init__(self, course: canvasapi.course.Course, assignment, review):
        self.canvas_id = review.assessor_id
        self.sis_login_id = course.get_user(self.canvas_id).login_id
        self.student_id = 0

        # self.reviewer_name = course.get_user(self.canvas_id).name
        self.first, self.second = course.get_user(self.canvas_id).name.split()
        self.total_score = 0
        self.rubric = self.get_reviewer_assessment(self, course, assignment)

    @staticmethod
    def get_reviewer_assessment(self, course: canvasapi.course.Course, assignment):
        reviewer_assessment = {'categories': []}
        rubric = course.get_rubrics(rubric_association_id=assignment.id)[0]
        rubric_id = rubric.id
        r = course.get_rubric(rubric_id, include=["peer_assessments"], style="full")
        for assessment in r.assessments:
            if assessment["assessor_id"] == self.canvas_id:     # makes sure review rubric belongs to reviewer
                self.total_score = assessment["score"]
                for each_category in assessment["data"]:
                    category = Category(each_category["points"], each_category["description"], each_category["comments"])
                    reviewer_assessment["categories"].append(category)

        return reviewer_assessment


class Category:

    def __init__(self, points, field, comment):
        self.score = points
        self.category_name = field
        self.comment = comment

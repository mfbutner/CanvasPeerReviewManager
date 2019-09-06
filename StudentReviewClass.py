import canvasapi


# makes new StudentReview object for each reviewer of a particular assignment
class StudentReview(object):

    def __init__(self, course: canvasapi.course.Course, assignment, review: canvasapi.peer_review.PeerReview):
        self.canvas_id = review.assessor_id
        self.sis_login_id = course.get_user(self.canvas_id).login_id
        self.student_id = 0

        # self.reviewer_name = course.get_user(self.canvas_id).name
        self.first, self.last = course.get_user(self.canvas_id).name.split()
        self.completed_the_review = False          # default to false, changed to true if assessment can be found
        self.total_score = 0
        self.rubric = self.get_reviewer_assessment(self, course, assignment)
        self.dict_reviews = self.reviews_to_dictionary()

    @staticmethod
    def get_reviewer_assessment(self, course: canvasapi.course.Course, assignment):
        reviewer_assessment = {'categories': []}
        rubric = course.get_rubrics(rubric_association_id=assignment.id)[0]
        rubric_id = rubric.id
        r = course.get_rubric(rubric_id, include=["peer_assessments"], style="full")    # gets rubrics containing p.r.'s
        for assessment in r.assessments:
            if assessment["assessor_id"] == self.canvas_id:     # makes sure review rubric belongs to reviewer
                self.completed_the_review = True
                self.total_score = assessment["score"]
                for each_category in assessment["data"]:        # gets points from each category
                    category = Category(each_category["points"], each_category["description"], each_category["comments"])
                    reviewer_assessment["categories"].append(category)

        return reviewer_assessment

    def reviews_to_dictionary(self):
        review = {"canvas_id": self.canvas_id,
                  "sis_login_id": self.sis_login_id,
                  "student_id": self.student_id,
                  "first": self.first,
                  "last": self.last,
                  "completed the review": self.completed_the_review,
                  "total score": self.total_score,
                  "rubric": {}
                  }
        categories = []
        for category in self.rubric:
            dict = category.categories_to_dictionary()
            categories.append(dict)

        review["rubric"] = categories
        return review


# makes new Category object for each category of the assessment found in rubric
class Category:

    def __init__(self, points: int, field: str, comment: str):
        self.score = points
        self.category_name = field
        self.comment = comment

    def categories_to_dictionary(self):
        category = {"score": self.score,
                    "category name": self.category_name,
                    "comment": self.category}
        return category

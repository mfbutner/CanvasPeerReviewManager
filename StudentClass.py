from StudentReviewClass import StudentReview
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
            student_id = review.user_id                 # get name of student for peer review
            student_name = course.get_user(student_id).name
            name = self.first + " " + self.last
            if name == student_name:                    # matches name of this student to name on reviewed assignment
                reviewer = StudentReview(course, assignment, review)
                review_list.append(reviewer)

        return review_list

    def get_student_peer_review_stats(self):
        data = []
        for review in self.reviews:
            data.append(review.total_score)

        if len(data) >= 1:
            self.mode = statistics.mode(data)
            self.mean = statistics.mean(data)
            self.median = statistics.median(data)
        else:
            self.mode = "none"
            self.mean = "none"
            self.median = "none"

        if len(data) >= 2:
            self.std_dev = round(statistics.stdev(data), 2)
        else:
            self.std_dev = 0

    def student_to_dictionary(self):
        student = {"canvas_id": self.canvas_id,
                   "sis_login_id": self.sis_login_id,
                   "first": self.first,
                   "last": self.last,
                   "student_id": self.student_id,
                   "late": self.late,
                   "total": self.total,
                   "mean": self.mean,
                   "median": self.median,
                   "mode": self.mode,
                   "std_dev": self.std_dev,
                   "reviews": []
                    }
        reviews = []
        for review in self.reviews:
            dict = review_to_dictionary(review)
            reviews.append(dict)
        student["reviews"] = reviews

        return student

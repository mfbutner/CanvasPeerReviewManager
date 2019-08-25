from StudentClass import Student, canvasapi, statistics


class AssignmentPeerReview(object):

    def __init__(self, course: canvasapi.course.Course, assignment):
        self.name = assignment.name
        self.assignment_id = assignment.id
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0
        self.students = self.make_students(course, assignment)
        self.get_peer_review_stats()

    @staticmethod
    def make_students(course: canvasapi.course.Course, assignment):
        students = []
        for submission in assignment.get_submissions():
            student = Student(course, assignment, submission)
            students.append(student)
        return students

    def get_peer_review_stats(self):
        data = []
        for student in self.students:           # make iterable out of peer review scores
            for review in student.reviews:
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


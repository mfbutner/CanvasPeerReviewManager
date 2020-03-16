from canvasapi import Canvas
import canvasapi

class peer_review:
    def __init__(self,canvas : Canvas, course_id, submission: canvasapi.submission, assessor_id):
        self.submission = submission
        self.submission_id = submission.id
        self.assessor_id = assessor_id
        self.user_id = submission.user_id
        self.assignment_id = submission.assignment_id
        self.course = canvas.get_course(course_id)
        self.work_flow = 0
        self.rubric = self.get_rubric()
        self.given_score = self.get_score()
        pass



    def get_score(self):
        assessments = self.rubric.assessments
        for assessment in assessments:
            if assessment['assessor_id'] == self.assessor_id:
                if assessment['artifact_id']== self.submission_id:
                    return assessment['score']




    def get_rubric(self):
        rubric = self.course.get_rubrics(rubric_association_id=self.assignment_id, include=["peer_assessments"], style="full")[0]
        rubric_id = rubric.id
        rubric = self.course.get_rubric(rubric_id, include=["peer_assessments"], style="full")
        return rubric

from canvasapi import Canvas
import canvasapi
from methodtools import lru_cache


class peer_review:

    def __init__(self,canvas : Canvas, course, submission: canvasapi.submission, assessor_id, rubric):

        self.submission = submission
        self.submission_id = submission.id
        self.assessor_id = assessor_id
        self.user_id = submission.user_id
        self.assignment_id = submission.assignment_id
        self.course = course
        self.work_flow = 0
        self.rubric = rubric
        self.given_score = self.get_score()
        pass

    def get_score(self):
        assessments = self.rubric.assessments
        for assessment in assessments:
            if assessment['assessor_id'] == self.assessor_id:
                if assessment['artifact_id']== self.submission_id:
                    return assessment['score']





class PeerReview:

    def __init__(self, course, submission, assessor_id, rubric, assessor_name,):
        self.assessor_name = assessor_name
        self.submission = submission
        self.submission_id = submission.id
        self.assessor_id = assessor_id
        self.user_id = submission.user_id
        self.assignment_id = submission.assignment_id
        self.course = course
        self.work_flow = None
        self.rubric = rubric
        self.assessment = None
        self.criteria_scores = dict()
        self.given_score = None
        self.get_scores()
        pass

    def get_scores(self):
        """
        If there is a rubric associated with the assignment in review, this method matches the existing assessments to
        the peer review object.
        This method finds and adds the criteria scores and the given score by the assessor to the peer review object.
        Upon creation of a peer review object this method runs automatically.
        """
        if self.rubric:
            assessments = self.rubric.assessments
            for assessment in assessments:
                if assessment['assessor_id'] == self.assessor_id:
                    if assessment['artifact_id'] == self.submission_id:
                        self.assessment = assessment
                        self.given_score = assessment['score']

            for i in range(len(self.rubric.criteria)):
                if self.assessment:
                    self.criteria_scores[self.rubric.criteria[i]['description']]= self.assessment['data'][i]['points']
                else:
                    self.criteria_scores[self.rubric.criteria[i]['description']] = None



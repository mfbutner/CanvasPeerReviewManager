import canvasapi
from canvasapi import Canvas
from peer_review_class import peer_review




class student:
    def __init__(self,canvas : Canvas, user_id, course, assignment, reviews,name,login_id,rubric):

        self.canvas = canvas
        self.id = user_id
        self.rubric = rubric
        self.name = name
        self.reviews = reviews
        self.login_id = login_id
        self.course = course
        self.assignment = assignment
        self.peer_reviews_completed = 0
        self.number_of_reviews_assigned = 0
        self.peer_reviews = self.get_peer_reviews_assigned()

        # self.name = canvas.get_user(user_id).name


    def get_peer_reviews_assigned(self):
        peer_reviews_assigned = []
        for review in self.reviews :
            if review.assessor_id == self.id:
                submission = self.assignment.get_submission(review.user_id)
                peer_reviews_assigned.append(peer_review(self.canvas,self.course,submission,self.id,self.rubric))
                if review.workflow_state == 'completed' :
                    self.peer_reviews_completed = self.peer_reviews_completed +1
                peer_reviews_assigned[-1].work_flow = review.workflow_state

        self.number_of_reviews_assigned = len(peer_reviews_assigned)
        return peer_reviews_assigned





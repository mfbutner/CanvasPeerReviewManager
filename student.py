import canvasapi
from canvasapi import Canvas
from peer_review_class import peer_review




class student:
    def __init__(self,canvas : Canvas, user_id, course_id, assignment_id):
        self.canvas = canvas
        self.id = user_id
        self.course_id = course_id
        self.course = canvas.get_course(course_id)
        self.assignment_id = assignment_id
        self.peer_reviews_completed = 0
        self.number_of_reviews_assigned = 0
        self.peer_reviews = self.get_peer_reviews_assigned()

        # self.name = canvas.get_user(user_id).name


    def get_peer_reviews_assigned(self):
        peer_reviews_assigned = []
        reviews = self.course.get_assignment(self.assignment_id).get_peer_reviews()
        for review in reviews :
            if review.assessor_id == self.id:
                submission = self.course.get_assignment(self.assignment_id).get_submission(review.user_id)
                peer_reviews_assigned.append(peer_review(self.canvas,self.course_id,submission,self.id))
                if review.workflow_state == 'completed' :
                    self.peer_reviews_completed = self.peer_reviews_completed +1
                peer_reviews_assigned[-1].work_flow = review.workflow_state

        self.number_of_reviews_assigned = len(peer_reviews_assigned)
        return peer_reviews_assigned





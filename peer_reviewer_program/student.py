

class Student:
    def __init__(self, user_id, course, assignment,name):

        self.id = user_id
        self.name = name
        self.course = course
        self.assignment = assignment
        self.peer_reviews_completed = 0
        self.peer_reviews = []
        self.peer_reviews_received =[]
        self.number_of_complete_reviews_received = 0
        self.number_of_reviews_assigned = 0






class student:
    def __init__(self, user_id, course, assignment,name,login_id):

        self.id = user_id
        self.name = name
        self.login_id = login_id
        self.course = course
        self.assignment = assignment
        self.peer_reviews_completed = 0
        self.peer_reviews = []
        self.peer_reviews_received =[]
        self.number_of_reviews_assigned = 0




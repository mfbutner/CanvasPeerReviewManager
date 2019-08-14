import sys
import canvasapi
import csv
import json

class StudentReview:


    def __init__(self, course, user_id):
        self.sis_login_id = course.get_user(user_id).login_id
        self.first, self.last = course.get_user(user_id).name.split()
        self.canvas_id = 0
        self.student_id = 0
        self.total = 0
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.std_dev = 0



class AssignmentPeerReviews:

  def __init__(self, assignment):
      self.name = assignment.name
      self.assignment_id = assignment.id
      self.reviewers = []
      self.mean = 0
      self.median = 0
      self.mode = 0
      self.std_dev = 0


canvas = canvasapi.Canvas("https://canvas.ucdavis.edu", sys.argv[1]  )         # Make a new Canvas object
course = canvas.get_course(1599)  # Make a new Course object with course number
assignments = course.get_assignments()
assignment = assignments[0]

for submission in assignment.get_submissions():

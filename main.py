from canvasapi import Canvas

from PeerReviewerClass import peerReviewer

# Canvas API URL
API_URL = "https://canvas.ucdavis.edu"
# Canvas API key
API_KEY = "3438~1dZ0nJfFzMLFk4dJxn6RU4KMgSiQ7tmZTpqqMEwrelzHqx9XiD5tDJDFlIABeFbg"
canvas = Canvas(API_URL, API_KEY)

a = peerReviewer(canvas, canvas.get_current_user())
# a = view_Courses(canvas,canvas.get_current_user())
# b = view_assignments(canvas,canvas.get_current_user(),a.course_id)
# c = view_peer_reviews(canvas,canvas.get_current_user(),a.course_id,b.current_assignment_id)

# student_A = student(canvas,241892,1599,348537)
# thelist = student_A.get_peer_reviews_assigned()
pass




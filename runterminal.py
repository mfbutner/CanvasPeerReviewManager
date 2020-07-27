from canvasapi import Canvas, exceptions
from peer_reviewer_program.PeerReviewerClass import PeerReviewer

# Canvas API URL
API_URL = "https://canvas.ucdavis.edu"
# Canvas API key
API_KEY = input("please enter your API key: ").strip()

while True:
    try:
        canvas = Canvas(API_URL, API_KEY)
        PeerReviewer(canvas, canvas.get_current_user())
        break
    except exceptions.InvalidAccessToken :
        print("Access token Invalid")
        API_KEY = input("please enter your API key: ").strip()



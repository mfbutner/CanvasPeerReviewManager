from canvasapi import Canvas, exceptions
from peer_reviewer_program.PeerReviewerClass import PeerReviewer

def run():


    while True:
        try:
            API_URL = input("please enter your API URL or press enter for UCD: ").strip()
            API_KEY = input("please enter your API key: ").strip()
            if not API_URL:
                API_URL = "https://canvas.ucdavis.edu"
            canvas = Canvas(API_URL, API_KEY)
            PeerReviewer(canvas, canvas.get_current_user())
            break
        except :
            print("Access token or API URL Invalid! Please try again.\n")


if __name__ == '__main__':
    run()

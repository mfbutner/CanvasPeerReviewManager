import cProfile
import pstats
from pstats import SortKey
from canvasapi import Canvas
from GuiPeerReviewer import GuipeerReviewer
from PeerReviewerClass import peerReviewer

# Canvas API URL
API_URL = "https://canvas.ucdavis.edu"
# Canvas API key
API_KEY = "3438~1dZ0nJfFzMLFk4dJxn6RU4KMgSiQ7tmZTpqqMEwrelzHqx9XiD5tDJDFlIABeFbg"
canvas = Canvas(API_URL, API_KEY)
GuipeerReviewer()

a = cProfile.run('peerReviewer(canvas, canvas.get_current_user())', 'peerreviewer_stats')
p = pstats.Stats('peerreviewer_stats')
p.sort_stats(SortKey.TIME).print_stats(10)

pass




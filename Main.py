import sys
import csv
import json
from AssignmentPeerReviewsClass import *
from StudentReviewClass import *


def main():
    canvas = canvasapi.Canvas("https://canvas.ucdavis.edu", sys.argv[1])
    course = canvas.get_course(1599)
    assignment_id = 348537
    peer_reviews = get_assignment_peer_reviews(course, assignment_id)
    # create_json(peer_reviews)


def get_assignment_peer_reviews(course: canvasapi.course.Course, assignment_id: int):
    assignment = course.get_assignment(assignment_id)
    peer_reviews = AssignmentPeerReview(course, assignment)
    return peer_reviews


def create_json(peer_reviews):
    with open('peer_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(peer_reviews, f, ensure_ascii=False, indent=4, default=lambda o: o.__dict__)


def from_json(json_file: json):
    peer_reviews = 0
    return peer_reviews


main()

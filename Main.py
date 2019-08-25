import sys
import csv
import canvasapi
import json
from AssignmentPeerReviewsClass import AssignmentPeerReview


def main():
    canvas = canvasapi.Canvas("https://canvas.ucdavis.edu", sys.argv[1])        # first command line arg: API key
    course = canvas.get_course(1599)
    assignment_id = sys.argv[2]                     # second command line arg: a single assignment ID

    peer_reviews = get_assignment_peer_reviews(course, assignment_id)
    # create_json(peer_reviews)
    # to_csv(peer_reviews)


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


def to_csv(peer_reviews):
    data = []           # make list of list ['Student Name', 'ID', 'Stats', 'Peer Reviews', ]
    write_to_csv(data)


def write_to_csv(data):
    with open("peer_reviews.csv") as csv_file:
        for line in data:
            csv_file.writerow(data)


main()

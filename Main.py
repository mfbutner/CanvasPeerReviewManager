import sys
import canvasapi
from typing import Iterable, List
import csv
import json
from AssignmentPeerReviewsClass import *
from StudentReviewClass import *


def main():
    canvas = canvasapi.Canvas("https://canvas.ucdavis.edu", sys.argv[1])
    course = canvas.get_course(1599)
    assignment_id = 348537
    peer_reviews = get_assignment_peer_reviews(course, assignment_id)


def get_assignment_peer_reviews(course: canvasapi.course.Course, assignment_id: int):
    assignment = course.get_assignment(assignment_id)
    peer_reviews = AssignmentPeerReview(course, assignment)
    return peer_reviews


def get_rubric_stats():
    stats = []
    return stats


def mean_of_reviews(data: Iterable[int]):
    mean = 0

    return mean


def median_of_reviews(data: Iterable[int]):
    median = 0

    return median


def mode_of_reviews(data: Iterable[int]):
    mode = 0

    return mode


def std_dev_of_reviews(data: Iterable[int]):
    std_dev = 0

    return std_dev


main()

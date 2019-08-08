import sys
import canvasapi
import csv
import json
from datetime import datetime


def main():
    # Canvas URL
    API_URL = "https://canvas.ucdavis.edu"
    # Canvas API key from configurations
    API_KEY = sys.argv[1]
    # Make a new Canvas object
    canvas = canvasapi.Canvas(API_URL, API_KEY)
    # Make a new Course object with course number
    course = canvas.get_course(1599)


# only prints completed peer reviews
def print_completed_reviews(course, x: int):
    review_list = []
    assignments = course.get_assignments()
    for review in assignments[x].get_peer_reviews():
        if review.workflow_state == "completed":
            print(review)
            print(review.user_id)
            print()
            review_list.append(review.user_id)      # FIGURE OUT WHAT INFO YOU WANT HERE
    return review_list
# tell if students haven't completed peer review
# student who doesnt submit/doesnt do peer review


# prints all reviews, takes course and assignment number as paramters
def print_reviews(course: canvasapi, x: int):
    print("REVIEWS:")
    assignments = course.get_assignments()
    for review in assignments[x].get_peer_reviews():
        print(review, "\n", review.user_id, "\n", review.workflow_state)
        print()

#rubric.include_peer_review()

# prints submissions, takes course and assignment number as parameters
def print_submissions(course, x: int):
    print("SUBMISSIONS")
    assignments = course.get_assignments()
    for submission in assignments[x].get_submissions():
        print(submission)
        print(submission.workflow_state)
        print("Late?:", submission.late)
        print(submission.score)
        print(submission.grade, "\n")


# prints all assignments and assignment number
def print_assignments(course):
    assignments = course.get_assignments()
    print("\nASSIGNMENTS:")
    for assignment in assignments:
        print(assignment)
    print()


# prints all people in course and ID
def print_people(course):
    print("\nPEOPLE:")
    users = course.get_users()
    for user in users:
        print(user)


# create new assignment
def create_new_assignment(course):
    new_assignment = course.create_assignment({
        'name': 'Assignment 1',
        'submission_types': ['online_upload'],
        'allowed_extensions': ['docx', 'doc', 'pdf'],
        'notify_of_update': True,
        'points_possible': 100 ,
        'due_at': datetime(2019, 7, 31, 11, 59),
        'description': 'Creating test assignment',
        'published': True
    })
    print(new_assignment)


def print_course_name(course):
    print("COURSE NAME:")
    print(course.name)


main()
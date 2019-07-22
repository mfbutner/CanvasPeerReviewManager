import sys
import canvasapi
import csv
from datetime import datetime

def main():
    # Canvas API URL
    API_URL = "https://canvas.ucdavis.edu"
    # Canvas API key
    API_KEY = sys.argv[1]

    # Make a new Canvas object
    canvas = canvasapi.Canvas(API_URL, API_KEY)
    course = canvas.get_course(1599)

    print("COURSE NAME:")
    print(course.name)

    assignments = course.get_assignments()

    # prints all reviews
    print("REVIEWS:")
    # print(assignments[0].get_peer_reviews())
    for review in assignments[0].get_peer_reviews():
        print(review, "\n", review.user_id, "\n", review.workflow_state)
        print()

    # only prints completed peer reviews
    for review in assignments[0].get_peer_reviews():
        if review.workflow_state == "completed":
            print(review)
            print(review.user_id)
            print()

    # tell if students haven't completed peer review
    # student who doesnt submit/doesnt do peer review

def writeToFile():
    with open(..., 'wb', newline ='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(mylist)

def printsubmissions(course, x):
    assignments = course.get_assignments()
    print("SUBMISSIONS")
    for submission in assignments[x].get_submissions():
        print(submission)
        print(submission.workflow_state)
        print("Late?:", submission.late)
        print(submission.score)
        print(submission.grade)
        print()


# prints all assignments and assignment number
def printassignments(course):
    assignments = course.get_assignments()
    print("\nASSIGNMENTS:")
    for assignment in assignments:
        print(assignment)
    print()


# prints all people in course and ID
def printpeople(course):
    print("\nPEOPLE:")
    users = course.get_users()
    for user in users:
        print(user)


def createassignment(course):
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

main()

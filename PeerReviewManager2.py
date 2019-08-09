import sys
import canvasapi
import csv
import json


def main():
    # Canvas URL
    API_URL = "https://canvas.ucdavis.edu"
    # Canvas API key from configurations
    API_KEY = sys.argv[1]
    # Make a new Canvas object
    canvas = canvasapi.Canvas(API_URL, API_KEY)
    # Make a new Course object with course number
    course = canvas.get_course(1599)

    assignments = course.get_assignments()
    assignment = assignments[0]
    name = assignment.name
    assignment_id = assignment.id
    max_points = assignment.points_possible

    rubric = make_rubric(assignment)        # gets dictionary with categories of assignment and points

    students = make_student_list(course, assignment)


# accepts assignment and returns a dictionary of all categories in rubric with name and max_points
def make_rubric(assignment):
    rubric = dict()  # make empty dictionary for rubric
    rubric["max_points"] = (assignment.rubric)[0]['points']  # gets points of assignment from rubric

    allcategories = []
    for element in assignment.rubric:                       # iterates over all categories of the assignment rubric
        category = dict()                                   # makes new dictionary for each category
        category["category name"] = element['description']  # adds name and points to each category
        category["max_points"] = element['points']
        allcategories.append(category)                      # adds each category to list of categories
    rubric["categories"] = allcategories

    return rubric


# takes in assignment & course, will return list of students that have their info, scores, and peer reviews
def make_student_list(course, assignment):
    students = []                                       # list of student dictionaries
    if not assignment.has_submitted_submissions:        # makes sure there is at least 1 submission
        return students

    i = 0
    for submission in assignment.get_submissions():     # goes through all of the submissions for assignment
        thisStudent = {}                                # creates new dictionary for each student
        thisStudent = get_student_info(course, submission, thisStudent)     # calls function to get student info
        score = submission.score

        # FOR EACH STUDENT:
        # calls get rubric stats
        # calls get peer reviews

        thisStudent["rubric_stats"] = get_student_rubric_stats()
        thisStudent["reviews"] = get_student_peer_reviews()

        students[i] = thisStudent                       # adds current student to list of students
        i += 1
    return students


# takes course, a single submission, and dictionary for student, returns filled dictionary with student info
def get_student_info(course, submission, thisStudent):
    user_id = submission.user_id
    # course.get_user(user_id).student_id      FIND OUT HOW TO GET STUDENT/CANVAS ID
    # course.get_user(user_id).canvas_id
    thisStudent["sis_login_id"] = course.get_user(user_id).login_id

    name = course.get_user(user_id).name
    thisStudent["first_name"], thisStudent["last_name"] = name.split()  # gets first and last name of each student

    thisStudent["canvas_id"] = 0                # sets attributes to 0, not sure how to get them yet
    thisStudent["student_id"] = 0
    thisStudent["total"] = 0
    thisStudent["mean"] = 0
    thisStudent["median"] = 0
    thisStudent["mode"] = 0
    thisStudent["std_dev"] = 0

    return thisStudent


def get_student_rubric_stats():     # might need to pass assignment and student name/ID
    rubric_stats = []

    return rubric_stats


def get_student_peer_reviews():     # might need to pass assignment and student name/ID
    # check if assignment even has peer reviews
    peer_reviews = []


    return peer_reviews


# prints all people in course and ID
def print_people(course):
    print("\nPEOPLE:")
    users = course.get_users()
    for user in users:
        print(user)


main()

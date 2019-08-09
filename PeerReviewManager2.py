import sys
import canvasapi
import csv
import json


def main():
    API_URL = "https://canvas.ucdavis.edu"              # Canvas URL
    API_KEY = sys.argv[1]                               # Canvas API key from configurations
    canvas = canvasapi.Canvas(API_URL, API_KEY)         # Make a new Canvas object
    course = canvas.get_course(1599)                    # Make a new Course object with course number

    assignments = course.get_assignments()
    assignment = assignments[0]

    # maybe iterate over all assignments
    this_assignment = {}        # creates empty dictionary for assignment
    this_assignment = make_assignment_dic(assignment, this_assignment)


def make_assignment_dic(course, assignment, this_assignent):
    this_assignent["name"] = assignment.name
    this_assignent["assignment_id"] = assignment.id
    max_points = assignment.points_possible

    this_assignent["mean"] = 0                # sets attributes to 0, not sure how to get them yet
    this_assignent["median"] = 0
    this_assignent["mode"] = 0
    this_assignent["std_dev"] = 0

    this_assignent["rubric"] = make_rubric(assignment)        # gets dict with categories of assignment and points
    this_assignent["students"] = make_student_list(course, assignment)      # gets list of student dictionaries

    return this_assignent

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


main()

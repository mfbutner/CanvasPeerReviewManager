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
    ID = assignment.id

    rubric = make_rubric(assignment)        # gets dictionary with categories of assignment and points

    max_points = 0          # gets max points of assignment by adding up max_points for each category
    for category in rubric["categories"]:
        max_points += category["max_points"]

    points = assignment.points_possible
    print(points)
    print(max_points)


# accepts assignment and returns a dictionary of all categories in rubric with name and max_points
def make_rubric(assignment):
    rubric = {}  # make empty dictionary for rubric
    rubric["max_points"] = (assignment.rubric)[0]['points']  # gets points of assignment from rubric

    allcategories = []
    for element in assignment.rubric:  # iterates over all individual categories (elements) of the assignment rubric
        category = {}  # makes new dictionary for each category
        category["category name"] = element['description']  # adds name and points to each category
        category["max_points"] = element['points']
        allcategories.append(category)  # adds each category to list of categories
    rubric["categories"] = allcategories
    return rubric


def make_student_list(assignment):
    students = []
    # for student :
        # calls get student info
        # calls get rubric stats
        # calls get peer reviews
    return students


def get_student_info(): # dont know what to pass yet
    # maybe just pass the students [] list and append info straight to it and then return it?
    # could also make new list with that info and return that list, which can be iterated over in make_student_list and added to students[]

    return


def get_student_rubric_stats(): #might need to pass assignment and student name/ID

    return


def get_student_peer_reviews(): # might need to pass assignment and student name/ID
    # check if assignment even has peer reviews

    return
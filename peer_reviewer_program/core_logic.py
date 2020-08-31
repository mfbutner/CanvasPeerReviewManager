import os
import typing
from canvasapi import Canvas
from canvasapi import assignment
from canvasapi import rubric
from canvasapi import peer_review
import canvasapi
from peer_reviewer_program.student import Student
from peer_reviewer_program.peer_review_class import PeerReview
import json
from peer_reviewer_program.peer_review_statistics_class import Statistics
import tkinter

# -------------------------NEW STUFF-------------------------
import enum
from typing import Callable, TypeVar, Iterable, List



def get_courses(user: canvasapi) -> [canvasapi.canvas.Course]:
    """
    :param user: canvas user object
    :return: a list of canvas course objects
    """
    return user.get_courses()


def get_favorite_courses(user: canvasapi.canvas.User) -> [canvasapi.canvas.Course]:
    """
    :param user: canvas user object
    :return: a list of canvas course objects
    """
    return user.get_favorite_courses()


def get_course(canvas: Canvas, course_id: int) -> canvasapi.canvas.Course:
    """
    :param canvas: canvas object
    :return: canvas course object
    """
    return canvas.get_course(course_id)

T = TypeVar('T')


class CanvasRole(enum.Enum):
    TEACHER = 'teacher'
    STUDENT = 'student'
    TA = 'ta'
    DESIGNER = 'designer'
    OBSERVER = 'observer'


def get_courses_enrolled_in_by_role(lookup_method: Callable[..., Iterable[canvasapi.course.Course]],
                                    roles: Iterable[CanvasRole] = (CanvasRole.TEACHER,),
                                    **kwargs) -> List[canvasapi.course.Course]:
    """

    :param lookup_method: a method that returns a iterable of canvas course. Likely an Instance of either
    canvasapi.Canvas.get_courses or canvasapi.current_user.CurrentUser.get_favorite_courses
    :param roles: The roles for the classes you are interested in
    :param kwargs: any other keyword parms to the canvas lookup method
    :return:
    """
    roles = {role.value for role in roles}
    courses = list()
    for course in lookup_method(**kwargs):
        try:
            for enrollment in course.enrollments:
                if enrollment['type'] in roles:
                    courses.append(course)
                    break
        except:
            pass
    return courses



def get_assignments(course: canvasapi.canvas.Course) -> [canvasapi.assignment]:
    """
    :param course: canvas course object
    :return: a list of canvas assignment objects
    """
    return course.get_assignments()


def get_assignments_with_peer_reviews(course):
    """
       :param course: canvas course object
       :return: a list of canvas assignment objects that have peer reviews assigned to them
       """
    return [assignment for assignment in course.get_assignments() if assignment.peer_reviews]


def get_assignment(course: canvasapi.canvas.Course, assignment_id: int):
    """
    :param course: canvas course object
    :return: a canvas assignment is returned given its id
    """
    return course.get_assignment(assignment_id)


def print_assignments(assignments: [canvasapi.assignment]):
    """
    prints the name of assignments for a canvas course
    :param assignments: canvas course object
    """
    print('\nAssignments:')
    i = 1
    for assignment in assignments:
        print(i, ')', assignment.name, assignment.id)
        i = i + 1


def print_courses(courses: [canvasapi.canvas.Course]):
    """
       prints the name of the course objects
       :param courses: a list of canvas course objects
       """
    i = 1
    print("Courses:")
    for course in courses:
        try:
            print(i, ')', course.name, "course id :", course.id)
            i = i + 1
        except AttributeError:
            print(i, ') Invalid Course')
            i = i + 1


def print_favorite_courses(courses: [canvasapi.canvas.Course]):
    """
    prints the name of the course objects
    :param courses: a list of canvas course objects
    """
    print("Favorite Courses:")
    i = 1
    for course in courses:
        try:
            print(i, ')', course.name, "course id :", course.id)
            i = i + 1
        except AttributeError:
            print(i, ') Invalid Course')
            i = i + 1


def get_students(course: canvasapi.canvas.Course) -> [canvasapi.canvas.User]:
    """
    :param course: canvas course object
    :return: returns a list of students in a canvas course
    """
    return course.get_users(enrollment_type='student')


def get_peer_reviews(assignment: canvasapi.assignment) -> [canvasapi.peer_review]:
    """
    :return: returns a list of canvas peer review objects for an assignment
    """
    return assignment.get_peer_reviews()


def get_rubric(course: canvasapi.canvas.Course, assignment_id: int) -> canvasapi.rubric:
    """
    :param course: canvas course object
    :return: the rubric associated with the assignment is returned
    """
    # r = get_assignment(course,assignment_id).rubric
    # rubric = course.get_rubrics(rubric_association_id=assignment_id, include=["peer_assessments"], style="full")[0]
    # rubric_id = rubric.id
    # rubric = course.get_rubric(rubric_id, include=["peer_assessments"], style="full")
    # return rubric
    assignment = get_assignment(course, assignment_id)
    try:
        rubric_id = assignment.rubric_settings['id']
        rubric = course.get_rubric(rubric_id, include=["peer_assessments"], style="full")
        return rubric
    except AttributeError:
        return None


def make_students_dict(students: [canvasapi.canvas.User], course: canvasapi.canvas.Course,
                       assignment: canvasapi.assignment, reviews: [canvasapi.peer_review],
                       rubric: canvasapi.rubric) -> typing.Dict[int, Student]:
    """
    :return: a dictionary with student id as keys and student objects as values
    """
    students_dict = {}
    for s in students:
        students_dict[s.id] = (Student(s.id, course, assignment, s.name))
    submissions_dict = make_submissions_dict(assignment)
    update_peer_reviews(reviews, students_dict, course, submissions_dict, rubric)
    return students_dict


def make_submissions_dict(assignment: canvasapi.assignment):
    submissions = assignment.get_submissions()
    submissions_dict = {}
    for s in submissions:
        submissions_dict[s.user_id] = s
    return submissions_dict


def generate_csv(students_dict: typing.Dict[int, Student], assignment_id: int, path: str = None, rubric=None):
    """
    -- a csv is exported containing student,id,SIS login ID,peer_reviews_assigned,peer_reviews_completed
    :param path: optional argument- this is the absolute path of where to save the csv file;
     if not given it will be saved in cwd
    :side_effect: overrides any csv file with the same name
    """
    if path is None:
        path = os.getcwd() + str(assignment_id) + "_peer_review.csv"
    f = open(path, "w+")
    f.write("student,id,peer_reviews_assigned,peer_reviews_completed\n")
    for s in students_dict.values():
        f.write(str(s.name) + ",")
        f.write(str(s.id) + ",")
        f.write(str(s.number_of_reviews_assigned) + ",")
        f.write(str(s.peer_reviews_completed) + "\n")

    f.close()
    if not rubric:
        return
    ff = open(os.getcwd() + str(assignment_id) + "_peer_review_second_file.csv", "w+")

    max_num_reviews = 0
    for s in students_dict.values():
        if s.number_of_complete_reviews_received > max_num_reviews:
            max_num_reviews = s.number_of_complete_reviews_received

    for s in students_dict.values():

        stats = Statistics(s, rubric)
        ff.write("Person Reviewed:,")
        ff.write(s.name + ",")
        ff.write("\n")
        ff.write("Reviewer:,")
        for r in s.peer_reviews_received:
            if r.work_flow == "completed":
                ff.write(str(r.assessor_name) + ",")

        for i in range(max_num_reviews - s.number_of_complete_reviews_received):
            ff.write(",")

        ff.write("Average,")
        ff.write("STD,")
        for r in s.peer_reviews_received:
            if r.work_flow == "completed":
                ff.write(str(r.assessor_name) + " Disagreement " + ",")

        for i in range(max_num_reviews - s.number_of_complete_reviews_received):
            ff.write(",")
        ff.write("Average Disagreement,")
        ff.write("STD Disagreement\n")

        for i in range(len(stats.criteria)):
            ff.write(stats.criteria[i] + ",")
            for score in stats.received_criteria_scores_percentage[i]:
                ff.write(str(score) + ",")
            for j in range(max_num_reviews - s.number_of_complete_reviews_received):
                ff.write(",")
            ff.write(str(stats.received_criteria_scores_average_percentage[i]) + ",")
            ff.write(str(stats.received_criteria_scores_std_percentage[i]) + ",")
            for disagreement in stats.criteria_disagreements_percentage[i]:
                ff.write(str(disagreement) + ",")
            for j in range(max_num_reviews - s.number_of_complete_reviews_received):
                ff.write(",")
            ff.write(str(stats.criteria_disagreement_average_percentage[i]) + ",")
            ff.write(str(stats.criteria_disagreement_std_percentage[i]))
            ff.write("\n")

        ff.write("Total,")

        for score in stats.received_total_scores_percentage:
            ff.write(str(score) + ",")
        for j in range(max_num_reviews - s.number_of_complete_reviews_received):
            ff.write(",")
        ff.write(str(stats.received_total_scores_average_percentage) + ",")
        ff.write(str(stats.received_total_scores_std_percentage) + ",")
        for dg in stats.total_disagreements_percentage:
            ff.write(str(dg) + ",")
        for j in range(max_num_reviews - s.number_of_complete_reviews_received):
            ff.write(",")
        ff.write(str(stats.total_disagreement_average_percentage) + ",")
        ff.write(str(stats.total_disagreement_std_percentage))
        ff.write("\n,\n")

    ff.close()


def update_peer_reviews(reviews: [canvasapi.peer_review], students_dict,
                        course: canvasapi.canvas.Course, submissions_dict,
                        rubric: canvasapi.rubric):
    """
    function generates peer review objects and inserts them in the students dictionary
    :param reviews: list of peer reviews received from canvas
    :param submissions_dict: list of assignment submissions received from canvas
    :side_effect: students dictionary is updated
    """
    for review in reviews:
        grader = students_dict[review.assessor_id]
        students_dict[review.assessor_id].peer_reviews.append(
            PeerReview(course, submissions_dict[review.user_id], grader.id, rubric, grader.name))
        students_dict[review.user_id].peer_reviews_received.append(
            PeerReview(course, submissions_dict[review.user_id], grader.id, rubric, grader.name))
        if review.workflow_state == 'completed':
            students_dict[review.assessor_id].peer_reviews_completed += 1
            students_dict[review.user_id].number_of_complete_reviews_received += 1
        students_dict[review.assessor_id].number_of_reviews_assigned = students_dict[
                                                                           review.assessor_id].number_of_reviews_assigned + 1
        students_dict[review.assessor_id].peer_reviews[-1].work_flow = review.workflow_state
        students_dict[review.user_id].peer_reviews_received[-1].work_flow = review.workflow_state


def export_statistics(students_dict: typing.Dict[int, Student], rubric: canvasapi.rubric, path: str = None):
    """
    --Exports a json file containing statistics for each student as a reviewer and as a reviewee
    :param path: optional argument- this is the absolute path of where to save the json file;
     if not given it will be saved in cwd
    :param students_dict: a dictionary generated by core_logic.make_students_dict()
    :param rubric: the rubric used by the peer reviews
    :side_effect overrides any previous statistics json files
    """
    statistics = []
    i = 0
    for s in students_dict.values():
        statistics.append({})
        stats = Statistics(s, rubric)
        statistics[i]["name"] = s.name
        statistics[i]["id"] = s.id
        statistics[i]["statistics as student "] = stats.received_statistics
        statistics[i]["statistics as reviewer"] = stats.reviewer_statistics
        i = i + 1

    json_object = json.dumps(statistics)
    assignment = list(students_dict.values())[0].assignment
    if path is None:
        path = os.getcwd() + "_" + str(assignment.id) + "_statistics.json"
    with open(path, "w") as outfile:
        outfile.write(json_object)


def creat_new_assignment(reference_assignment: canvasapi.assignment, course: canvasapi.canvas.Course,
                         students_dict: typing.Dict[int, Student], assignment_group_id):
    """
    --creates a new assignment inside the course
    :param reference_assignment: the new assignment inherits its name from the refrence assignment
    :param course: the course in which the assignment is created
    :param students_dict: student's dictionary is used to generate grades and upload the the new assignment
    :param assignment_group_id
    :side effects: the new assignment will not show up in the assignments view until the view is updated

    """
    assignment = {}
    name = ("Peer Review For " + reference_assignment.name)
    number_of_times_name_used = 0
    assignments = course.get_assignments()

    for a in assignments:
        if name in a.name:
            number_of_times_name_used = number_of_times_name_used + 1

    if number_of_times_name_used > 0:
        name = ("Peer Review For " + reference_assignment.name) + "(" + str(number_of_times_name_used) + ")"

    assignment['name'] = name
    assignment['published'] = True
    assignment['points_possible'] = 100
    assignment['grading_type'] = "percent"
    assignment['assignment_group_id'] = assignment_group_id
    new_assignment = course.create_assignment(assignment)
    new_assignment.submissions_bulk_update(grade_data=make_grade_dictionary(students_dict))


def make_grade_dictionary(students_dict: typing.Dict[int, Student]) -> typing.Dict[int, typing.Dict]:
    """
    :param students_dict: the number of peer reviews completed and assigned in the students dictionary is used to calculate students' grades
    :return: grade dictionary for further use to grade an assignment
    """
    grades_dict = {}
    for s in students_dict.values():
        completed = 0
        for review in s.peer_reviews:
            if review.work_flow == "completed" or review.submission.workflow_state == "unsubmitted":
                completed += 1
        if s.number_of_reviews_assigned:
            grades_dict[s.id] = {'posted_grade': completed / s.number_of_reviews_assigned * 100}
    return grades_dict


def assignment_already_graded(assignment: canvasapi.assignment) -> bool:
    """
    --checks if an assignment is already graded or not
    :return: a bool
    """
    submissions = assignment.get_submissions()
    for s in submissions:
        if s.score:
            return True
    else:
        return False


def get_assignment_groups(course: canvasapi.canvas.Course):
    """
    returns assignment groups for a given course
    """
    return course.get_assignment_groups()


def upload_grades(assignment: canvasapi.assignment, grade_dict: typing.Dict[int, typing.Dict]):
    """
    -- uploads a grade dictionary to a certain assignment
    """
    assignment.submissions_bulk_update(grade_data=grade_dict)
    print("assignment graded.\n")


def clear_frame(frame: tkinter.Frame):
    """
    clears the contents of a given frame
    """
    for widget in frame.winfo_children():
        widget.destroy()

from canvasapi import Canvas
from student import student
from peer_review_class import peer_review
import json
from peer_review_statistics_class import Statistics


def get_courses(user):
    return user.get_courses()


def get_favorite_courses(user):
    return user.get_favorite_courses()


def get_course(canvas: Canvas, course_id):
    return canvas.get_course(course_id)


def get_assignments(course):
    return course.get_assignments()


def get_assignment(course,assignment_id):
    return course.get_assignment(assignment_id)


def print_assignments(assignments):
    print('\nAssignments:')
    i = 1
    for assignment in assignments:
        print(i, ')', assignment.name, assignment.id)
        i = i + 1


def print_courses(courses):
    i = 1
    print("Courses:")
    for course in courses:
        try:
            print(i, ')', course.name, "course id :", course.id)
            i = i + 1
        except AttributeError:
            pass


def print_favorite_courses(courses):
    print("Favorite Courses:")
    i = 1
    for course in courses:
        try:
            print(i, ')', course.name, "course id :", course.id)
            i = i + 1
        except AttributeError:
            pass


def get_students(course):
    return course.get_users(enrollment_type='student')


def get_peer_reviews(assignment):
    return assignment.get_peer_reviews()


def get_rubric(course,assignment_id):
    rubric = course.get_rubrics(rubric_association_id= assignment_id, include=["peer_assessments"], style="full")[0]
    rubric_id = rubric.id
    rubric = course.get_rubric(rubric_id, include=["peer_assessments"], style="full")
    return rubric


def make_students_dict(students,course, assignment, reviews, rubric):
    students_dict = {}
    for s in students :
        students_dict[s.id] = (student(s.id,course,assignment, s.name,s.login_id))
    submissions_dict = make_submissions_dict(assignment)
    update_peer_reviews(reviews, students_dict, course, submissions_dict, rubric)
    return students_dict


def make_submissions_dict(assignment):
    submissions = assignment.get_submissions()
    submissions_dict = {}
    for s in submissions :
        submissions_dict[s.user_id]= s
    return submissions_dict


def generate_csv(students_dict,assignment_id):
    f = open(str(assignment_id) + "_peer_review.csv", "w+")
    f.write("student,id,SIS login ID,peer_reviews_assigned,peer_reviews_completed\n")
    for s in students_dict.values():
        f.write(str(s.name)+",")
        f.write(str(s.id)+",")
        f.write(str(s.login_id) + ",")
        f.write(str(s.number_of_reviews_assigned)+",")
        f.write(str(s.peer_reviews_completed)+"\n")


def update_peer_reviews(reviews, students_dict, course,submissions_dict,rubric):
    for review in reviews:
        grader = students_dict[review.assessor_id]
        students_dict[review.assessor_id].peer_reviews.append(peer_review(course, submissions_dict[review.user_id], grader.id, rubric))
        students_dict[review.user_id].peer_reviews_received.append(peer_review(course, submissions_dict[review.user_id], grader.id, rubric))
        if review.workflow_state == 'completed':
            students_dict[review.assessor_id].peer_reviews_completed = students_dict[review.assessor_id].peer_reviews_completed + 1
        students_dict[review.assessor_id].number_of_reviews_assigned= students_dict[review.assessor_id].number_of_reviews_assigned + 1

        students_dict[review.assessor_id].peer_reviews[-1].work_flow = review.workflow_state
        students_dict[review.user_id].peer_reviews_received[-1].work_flow = review.workflow_state


def export_statistics(students_dict,rubric):
    statistics = []
    i = 0
    for s in students_dict.values():
        statistics.append({})
        stats = Statistics(s,rubric)
        statistics[i]["name"] = s.name
        statistics[i]["id"] = s.id
        statistics[i]["statistics as student "] = stats.received_statistics
        statistics[i]["statistics as reviewer"] = stats.reviewer_statistics
        i = i + 1

    json_object = json.dumps(statistics)
    print(json_object)
    with open("stats.json", "w") as outfile:
        outfile.write(json_object)


def creat_new_assignment(reference_assignment,course,students_dict):
    """
    :param reference_assignment:
    :param course:
    :param students_dict:
    :side effects:
    """
    assignment = {}
    name = ("Peer Review For "+ reference_assignment.name)
    number_of_times_name_used = 0
    assignments = course.get_assignments()

    for a in assignments:
        if name in a.name:
            number_of_times_name_used = number_of_times_name_used + 1

    if number_of_times_name_used > 0:
        name = ("Peer Review For " + reference_assignment.name) + "(" + str(number_of_times_name_used) + ")"

    assignment['name'] = name
    assignment['published'] = True
    new_assignment = course.create_assignment(assignment)
    new_assignment.submissions_bulk_update(grade_data= make_grade_dictionary(students_dict))


def make_grade_dictionary(students_dict):
    """

    :param students_dict:
    :return:
    """
    grades_dict = {}
    for s in students_dict.values():
        grades_dict[s.id] = {'posted_grade' : s.peer_reviews_completed/s.number_of_reviews_assigned}
    return grades_dict


def assignment_already_graded(assignment):
    submissions = assignment.get_submissions()
    for s in submissions:
        if s.score:
            return True
    else:
        return False


def upload_grades(assignment, grade_dict):
#if they do it on an unpublished assignment then publish it and put in the grades otherwise check the two conditions : attempts and existing grades
    assignment.submissions_bulk_update(grade_data=grade_dict)
    print("assignment graded.\n")



def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


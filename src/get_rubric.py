import sys
import canvasapi
from student import Student
from peer_review import PeerReview


def get_rubric_for_assignment(assignment: canvasapi.assignment.Assignment, course: canvasapi.course.Course):
    rubric_id = assignment.rubric_settings['id']
    rubric = course.get_rubric(rubric_id)
    return rubric


def get_peer_reviews_for_assignment(assignment: canvasapi.assignment.Assignment, course: canvasapi.course.Course):
    reviews = assignment.get_peer_reviews(include=['submission_comments', 'user'])

    result = dict()
    for review in reviews:
        reviewer = Student(review.assessor)
        reviewed = Student(review.user)
        given_review = PeerReview(reviewer, reviewed, [comment['comment'] for comment in review.submission_comments if
                                                       comment['author_id'] == reviewer.id])
        if reviewer not in result:
            result[reviewer] = {reviewed: given_review}
        else:
            result[reviewer][reviewed] = given_review

    if hasattr(assignment, 'rubric_settings'):
        rubric_id = assignment.rubric_settings['id']
        rubric = course.get_rubric(rubric_id, include=['peer_assessments'], style='full')
        submissions = assignment.get_submissions(include=['user'])
        submission_map = {submission.id: submission.user for submission in submissions}

        for assessment in rubric.assessments:
            # if this assessment is for the assignment of interest
            if assessment['rubric_association']['association_id'] == assignment.id:
                rubric_review = {criteria['description']:
                                     {'max_points': criteria['points'],
                                      'points': scoring['points'],
                                      'comments': scoring['comments']}
                                 for criteria, scoring in zip(rubric.criteria, assessment['data'])}
                reviewer = course.get_user(assessment['assessor_id'])
                reviewer = Student(reviewer.attributes)
                reviewed = Student(submission_map[assessment['artifact_id']])
                result[reviewer][reviewed].rubric_review = rubric_review
    return result


def print_peer_reviews(assignment: canvasapi.assignment.Assignment, course: canvasapi.course.Course):
    student_reviews = get_peer_reviews_for_assignment(assignment, course)
    for reviewer,reviewed in student_reviews.items():
        for review in reviewed.values():
            print(review)


def main():
    canvas_key = sys.argv[1]
    canvas_url = 'https://canvas.ucdavis.edu'
    course_id = 1599
    assignment_id = 348537  # 502620
    canvas_connection = canvasapi.Canvas(canvas_url, canvas_key)
    course = canvas_connection.get_course(course_id)
    me = course.get_user(240755)
    assignment = course.get_assignment(assignment_id)
    print_peer_reviews(assignment, course)


if __name__ == '__main__':
    main()

import canvasapi
from canvasapi import Canvas
import taskClass
from student import student
from methodtools import lru_cache

class view:


    def __init__(self, canvas : Canvas, user: canvasapi.user):
        self.user = user
        self.canvas = canvas
        self.user_in = 0
    def run(self):
        pass
        
class view_peer_reviews(view):

    @lru_cache()
    @staticmethod
    def create(canvas: Canvas, user: canvasapi.user, course_id, assignment_id):
        return view_peer_reviews(canvas, user, course_id, assignment_id)

    def __init__(self, canvas: Canvas, user: canvasapi.user, course, assignment_id):
        super().__init__(canvas, user)
        self.course = course
        self.students = self.course.get_users(enrollment_type='student')
        self.assignment_id = assignment_id
        self.assignments = self.course.get_assignment(assignment_id)
        self.reviews = self.assignments.get_peer_reviews()
        self.user_in = 0
        self.rubric = self.get_rubric()
        self.students_list = self.make_students_list()

        pass

    def generate_csv(self):
        f = open(str(self.assignment_id) + "_peer_review.csv", "w+")
        f.write("student,id,SIS login ID,peer_reviews_assigned,peer_reviews_completed\n")
        for s in self.students_list:
            f.write(str(s.name)+",")
            f.write(str(s.id)+",")
            f.write(str(s.login_id) + ",")
            f.write(str(s.number_of_reviews_assigned)+",")
            f.write(str(s.peer_reviews_completed)+"\n")
        pass

    def get_rubric(self):
        rubric = self.course.get_rubrics(rubric_association_id=self.assignment_id, include=["peer_assessments"], style="full")[0]
        rubric_id = rubric.id
        rubric = self.course.get_rubric(rubric_id, include=["peer_assessments"], style="full")
        return rubric


    def run(self):

        self.user_in = input("Options: \n1 ) Get the CSV for the peer reviews\nb ) back\nq ) quit\nEnter what you want to do "
                             "next: " )
        if self.user_in == 'b':
            return taskClass.backTask()
        elif self.user_in == 'q':
            return taskClass.quitTask()
        elif self.user_in == '1':
            self.generate_csv()
            print("CSV generated. \n")
            return self.run()


    def make_students_list(self):
        students_list = []
        for s in self.students :
            students_list.append(student(self.canvas,s.id,self.course,self.assignments,self.reviews, s.name,s.login_id,self.rubric))

        return students_list


class view_assignments(view):
    def __init__(self,canvas : Canvas, user: canvasapi.user, course_id):
        super().__init__(canvas, user)
        self.course_id = course_id
        self.course = canvas.get_course(course_id)
        self.assignments = self.course.get_assignments()
        self.user_in = 0
        self.current_assignment_id = 0


    def run(self):
        print('\nAssignments:')
        i = 1
        for assignment in self.assignments:
            print(i,')',assignment.name, assignment.id)
            i = i + 1
        print('b ) back\nq ) quit')
        self.user_in = input("Enter the number of the assignment you want to grade or enter : ")
        print('\n')
        try:
            self.current_assignment_id = self.assignments[int(self.user_in)-1].id
        except:
            pass
        if self.user_in == 'b':
            return taskClass.backTask()
        elif self.user_in == 'q':
            return taskClass.quitTask()
        else:
            return taskClass.AddTask(view_peer_reviews.create(self.canvas,self.user,self.course,self.current_assignment_id))






class view_Courses(view):
    def __init__(self,canvas : Canvas, user: canvasapi.user):
        super().__init__(canvas,user)
        self.courses = user.get_courses()
        self.favorite_courses = user.get_favorite_courses()
        self.user_in = 0
        self.course_id = 0


    def display_courses(self):
        i = 1
        print("Your courses are:")
        for course in self.courses:
            try:
                print(i, ')', course.name, "course id :", course.id)
                i = i + 1
            except AttributeError:
                pass


    def display_favorite_courses(self):
        print("Your favorite courses are:")
        i = 1
        for course in self.favorite_courses:
            try:
                print(i, ')', course.name, "course id :", course.id)
                i = i + 1
            except AttributeError:
                pass


    def run(self):
        if self.user_in == 'a':
            self.display_courses()
            print('b ) back\nq ) quit')
            self.user_in = input('Enter the course you want to grade: ')
            try:
                self.course_id = self.courses[int(self.user_in)-1].id
            except:
                pass
        else:
            self.display_favorite_courses()
            print('b ) back\nq ) quit')
            self.user_in = input('Enter the course you want to grade or enter "a" to see all courses: ')
            try:
                self.course_id = self.favorite_courses[int(self.user_in)-1]
            except:
                pass
            if self.user_in == 'a':
                self.run()

            elif self.user_in == 'b':
                return taskClass.backTask()
            elif self.user_in == 'q':
                return taskClass.quitTask()
            else :
                #view_assignments(recent_view.canvas, recent_view.user, recent_view.course_id)
                return taskClass.AddTask(view_assignments(self.canvas, self.user,self.course_id))






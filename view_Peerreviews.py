from viewClass import view
from view_upload_grades import grade_peer_review_assignment
import canvasapi
from canvasapi import Canvas
import tkinter
import taskClass
from methodtools import lru_cache
import core_logic


class view_peer_reviews(view):
    @lru_cache()
    @staticmethod
    def create(canvas: Canvas, user: canvasapi.user, course, assignment_id,  root :  tkinter.Tk):
        return view_peer_reviews(canvas, user, course, assignment_id, root)

    def __init__(self, canvas: Canvas, user: canvasapi.user, course, assignment_id,root :  tkinter.Tk):
        super().__init__(canvas, user)
        self.root = root
        self.course = course
        self.students = core_logic.get_students(self.course)
        self.assignment_id = assignment_id
        self.assignments = core_logic.get_assignment(self.course,self.assignment_id)
        self.reviews = core_logic.get_peer_reviews(self.assignments)
        self.user_in = 0
        self.rubric = core_logic.get_rubric(course,assignment_id)
        self.students_dict = core_logic.make_students_dict(self.students,self.course,self.assignments,self.reviews,self.rubric)

    def run(self):
        self.user_in = input("Options: \n"
                             "1 ) Get the CSV for the peer reviews\n"
                             "2 ) Creat a new assignment for the peer reviews\n"
                             "3 ) Upload Grades to an existing Assignment\n"
                             "4 ) Export Statistics JSON\n"
                             "b ) back\n"
                             "q ) quit\n"
                             "Enter what you want to do next: ").strip()

        if self.user_in == 'b':
            return taskClass.backTask()

        elif self.user_in == 'q':
            return taskClass.quitTask()

        elif self.user_in == '1':
            core_logic.generate_csv(self.students_dict,self.assignment_id)
            print("CSV generated. \n")
            return self.run()

        elif self.user_in == '2':
            core_logic.creat_new_assignment(self.assignments,self.course,self.students_dict)
            print("Assignment Created.\n")
            return self.run()

        elif self.user_in == '3':
            return taskClass.AddTask(grade_peer_review_assignment(self.canvas,self.user,self.course,
                                                                  core_logic.make_grade_dictionary(self.students_dict), self.root))
        elif self.user_in == '4':
            core_logic.export_statistics(self.students_dict,self.rubric)
            print("JSON exported. \n")
            return self.run()



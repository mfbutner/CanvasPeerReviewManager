from viewClass import view
import core_logic
import canvasapi
from canvasapi import Canvas
import taskClass
import tkinter

class grade_peer_review_assignment(view):
    def __init__(self, canvas: Canvas, user: canvasapi.user, course, grade_dict : dict, root : tkinter.Tk) :
        super().__init__(canvas, user)
        self.root = root
        self.course = course
        self.canvas = canvas
        self.grade_dict = grade_dict
        self.assignments = self.course.get_assignments()
        self.assignment = 0
        self.user_in = 0

    def run(self):
        core_logic.print_assignments(self.assignments)
        print('b ) back\nq ) quit')
        self.user_in = input('Please Choose an assignment to upload the grades to: ').strip()
        if self.user_in == 'b':
            print("\n")
            return taskClass.backTask()
        elif self.user_in == 'q':
            return taskClass.quitTask()
        else:
            self.assignment = self.assignments[int(self.user_in) - 1]
            if core_logic.assignment_already_graded(self.assignment):
                inp = input(
                    "This assignment has existing grades; Are you sure you want to overwrite the grades? ").strip()
                if inp == 'n' or inp == 'no':
                    print("\n")
                    return taskClass.backTask()
                elif inp == 'y' or inp == 'yes':
                    core_logic.upload_grades(self.assignment,self.grade_dict)
            else:
                core_logic.upload_grades(self.assignment,self.grade_dict)

            print("\n")
            return taskClass.backTask()

from  viewClass import view
from view_Peerreviews import view_peer_reviews
import canvasapi
from canvasapi import Canvas
import tkinter
import taskClass
import core_logic


class view_assignments(view):
    def __init__(self,canvas : Canvas, user: canvasapi.user, course_id, root :  tkinter.Tk):
        super().__init__(canvas, user)
        self.course_id = course_id
        self.canvas = canvas
        self.root = root
        self.course = core_logic.get_course(self.canvas, self.course_id)
        self.assignments = core_logic.get_assignments(self.course)
        self.user_in = 0
        self.current_assignment_id = 0

    def run(self):
        core_logic.print_assignments(self.assignments)
        print('b ) back\nq ) quit')
        self.user_in = input("Enter the number of the assignment you want to grade or enter : ").strip()
        print('\n')
        try:
            self.current_assignment_id = self.assignments[int(self.user_in)-1].id
        except :
            pass
        if self.user_in == 'b':
            return taskClass.backTask()
        elif self.user_in == 'q':
            return taskClass.quitTask()
        else:
            return taskClass.AddTask(view_peer_reviews.create(self.canvas,self.user,self.course,self.current_assignment_id,self.root))

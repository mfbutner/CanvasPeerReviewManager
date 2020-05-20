from  viewClass import view
from assignmentView import view_assignments
import canvasapi
from canvasapi import Canvas
import tkinter
import taskClass
import core_logic

class view_Courses(view):
    def __init__(self,canvas: Canvas, user: canvasapi.user, root :  tkinter.Tk ):
        self.root = root
        super().__init__(canvas,user)
        self.courses = core_logic.get_courses(user)
        self.favorite_courses = core_logic.get_favorite_courses(user)
        self.user_in = 0
        self.course_id = 0


    def run(self):

        if self.user_in == 'a':
            core_logic.print_courses(self.courses)
            print('b ) back\nq ) quit')
            self.user_in = input('Enter the course you want to grade: ')
            try:
                self.course_id = self.courses[int(self.user_in)-1].id
            except :
                pass
        else:
            core_logic.print_favorite_courses(self.favorite_courses)
            print('b ) back\nq ) quit')
            self.user_in = input('Enter the course you want to grade or enter "a" to see all courses: ').strip()

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
            else:
                return taskClass.AddTask(view_assignments(self.canvas, self.user,self.course_id, self.root))







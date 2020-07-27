from peer_reviewer_program.viewClass import view
from peer_reviewer_program.view_assignments import ViewAssignments
import canvasapi
from canvasapi import Canvas
from peer_reviewer_program import taskClass
from peer_reviewer_program import core_logic


class ViewCourses(view):
    def __init__(self, canvas: Canvas, user: canvasapi.canvas.User):
        super().__init__(canvas, user)
        self.courses = core_logic.get_courses(user)
        self.favorite_courses = core_logic.get_favorite_courses(user)
        self.print_all_courses = False
        self.user_in = None
        self.course_id = 0

    def run(self):
        """
        Runs view courses for the terminal version of the program.
        Upon running this method the user is asked to select a course/action.
        After selecting a course this method adds a ViewAssignments instance to the program task stack.

        """
        if self.print_all_courses:
            core_logic.print_courses(self.courses)
        else:
            core_logic.print_favorite_courses(self.favorite_courses)

        print('a ) all courses\nq ) quit')
        self.user_in = input('Enter the course you want to grade : ').strip()

        if self.user_in.isnumeric():
            try:
                if self.print_all_courses:
                    self.course_id = self.courses[int(self.user_in) - 1]
                else:
                    self.course_id = self.favorite_courses[int(self.user_in) - 1]
                test = self.course_id.name
                return taskClass.AddTask(ViewAssignments(self.canvas, self.user, self.course_id))
            except (ValueError, IndexError, AttributeError):
                print("\ninvalid input please try again.\n")
                return self.run()

        elif self.user_in == 'a':
            self.print_all_courses = True
            return self.run()

        elif self.user_in == 'q':
            return taskClass.QuitTask()
        else:
            print("\ninvalid input please try again.\n")
            return self.run()

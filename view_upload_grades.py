from peer_reviewer_program.viewClass import view
from peer_reviewer_program import core_logic
import canvasapi
from canvasapi import Canvas
from peer_reviewer_program import taskClass



class ViewUploadGrades(view):
    def __init__(self, canvas: Canvas, user: canvasapi.canvas.User, course, grade_dict: dict):
        super().__init__(canvas, user)
        self.course = course
        self.canvas = canvas
        self.grade_dict = grade_dict
        self.assignments = self.course.get_assignments()
        self.assignment = 0
        self.user_in = 0

    def run(self):
        """
        Runs view upload grades for the terminal version of the program.
        Upon running, the user is asked to choose an assignment to upload the generated grades for peer reviews to.
        After Completion, the user is taken back to the peer reviews view.

        """
        core_logic.print_assignments(self.assignments)
        print('b ) back\nq ) quit')
        self.user_in = input('Please Choose an assignment to upload the grades to: ').strip()
        if self.user_in == 'b':
            print("\n")
            return taskClass.BackTask()
        elif self.user_in == 'q':
            return taskClass.QuitTask()
        else:
            try:
                self.assignment = self.assignments[int(self.user_in) - 1]
                if core_logic.assignment_already_graded(self.assignment):
                    inp = input(
                        "This assignment has existing grades; Are you sure you want to overwrite the grades? ").strip()
                    if inp == 'n' or inp == 'no':
                        print("\n")
                        return taskClass.BackTask()
                    elif inp == 'y' or inp == 'yes':
                        core_logic.upload_grades(self.assignment, self.grade_dict)
                else:
                    core_logic.upload_grades(self.assignment, self.grade_dict)

                print("\n")
                return taskClass.BackTask()
            except (ValueError, IndexError, AttributeError):
                print("\ninvalid input please try again.\n")
                return self.run()

from peer_reviewer_program.viewClass import view
from peer_reviewer_program.view_peerreviews import ViewPeerReviews
import canvasapi
from canvasapi import Canvas
from peer_reviewer_program import taskClass
from peer_reviewer_program import core_logic


class ViewAssignments(view):
    def __init__(self, canvas: Canvas, user: canvasapi.canvas.User, course_id):
        super().__init__(canvas, user)
        self.course_id = course_id
        self.canvas = canvas
        self.course = core_logic.get_course(self.canvas, self.course_id)
        self.assignments = core_logic.get_assignments_with_peer_reviews(self.course)
        self.user_in = None
        self.current_assignment_id = None

    def run(self):
        """
        Runs view assignments for the terminal version of the program.
        Upon running this method the user is asked to select an assignment/action.
        After selecting an assignment this method adds a ViewPeerReviews instance to the program task stack.

        """
        core_logic.print_assignments(self.assignments)
        print('b ) back\nq ) quit')
        self.user_in = input("Enter the number of the assignment you want to grade or enter : ").strip()


        if self.user_in == 'b':
            return taskClass.BackTask()
        elif self.user_in == 'q':
            return taskClass.QuitTask()
        else:
            try:
                self.current_assignment_id = self.assignments[int(self.user_in) - 1].id
                return taskClass.AddTask(
                    ViewPeerReviews.create(self.canvas, self.user, self.course, self.current_assignment_id))
            except (ValueError, IndexError, AttributeError):
                print("\ninvalid input please try again.")
                return self.run()


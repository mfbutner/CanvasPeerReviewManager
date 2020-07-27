from peer_reviewer_program.viewClass import view
from peer_reviewer_program.view_upload_grades import ViewUploadGrades
import canvasapi
from canvasapi import Canvas
from peer_reviewer_program import taskClass
from methodtools import lru_cache
from peer_reviewer_program import core_logic


class ViewPeerReviews(view):
    @lru_cache()
    def create(canvas: Canvas, user: canvasapi.canvas.User, course, assignment_id):
        return ViewPeerReviews(canvas, user, course, assignment_id)

    def __init__(self, canvas: Canvas, user: canvasapi.canvas.User, course, assignment_id):
        super().__init__(canvas, user)
        self.course = course
        self.students = core_logic.get_students(self.course)
        self.assignment_id = assignment_id
        self.assignments = core_logic.get_assignment(self.course,self.assignment_id)
        self.reviews = core_logic.get_peer_reviews(self.assignments)
        self.user_in = None
        self.rubric = core_logic.get_rubric(course,assignment_id)
        self.students_dict = core_logic.make_students_dict(self.students,self.course,self.assignments,self.reviews,self.rubric)

    def run(self):
        """
        Runs view peer reviews for the terminal version of the program.
        Upon running this method the user is asked to select one of the options listed below.

        """
        self.user_in = input("\nOptions: \n"
                             "1 ) Get the CSV for the peer reviews\n"
                             "2 ) Creat a new assignment for the peer reviews\n"
                             "3 ) Upload Grades to an existing Assignment\n"
                             "4 ) Export Statistics JSON\n"
                             "b ) back\n"
                             "q ) quit\n"
                             "Enter what you want to do next: ").strip()

        if self.user_in == 'b':
            return taskClass.BackTask()

        elif self.user_in == 'q':
            return taskClass.QuitTask()

        elif self.user_in == '1':
            core_logic.generate_csv(self.students_dict,self.assignment_id,None, self.rubric)
            print("CSV generated.")
            return self.run()

        elif self.user_in == '2':
            core_logic.creat_new_assignment(self.assignments,self.course,self.students_dict)
            print("Assignment Created.")
            return self.run()

        elif self.user_in == '3':
            return taskClass.AddTask(ViewUploadGrades(self.canvas,self.user,self.course,
                                                                  core_logic.make_grade_dictionary(self.students_dict)))
        elif self.user_in == '4':
            core_logic.export_statistics(self.students_dict, self.rubric)
            print("JSON exported. ")
            return self.run()
        else:
            print("\ninvalid input please try again.\n")
            return self.run()




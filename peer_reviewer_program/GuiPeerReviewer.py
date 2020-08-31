import os
import tkinter
from tkinter import filedialog
import peer_reviewer_program
from peer_reviewer_program import core_logic
from canvasapi import Canvas
from canvasapi import exceptions
import Image
import ImageTk



class GuipeerReviewer:
    def __init__(self):
        self.canvas = None
        self.user=None
        self.courses= None
        self.assignments=None
        self.header=None
        self.img=None
        self.message_frame=None
        self.action_frame= None
        self.message_label =None
        self.selected_course = None
        self.favorite_courses=None
        self.root = tkinter.Tk()
        self.courses_frame = None
        self.assignments_frame=None
        self.options_frame=None
        self.secondary_options_frame=None
        self.students_dict = None
        self.selected_assignment= None
        self.reviews = None
        self.rubric=None
        self.upload_grades_to=None
        self.command=None
        self.pop_up=None
        self.assignment_groups= None
        self.selected_assignment_group= None
        self.functions_list=[]
        self.build_header()
        self.root.mainloop()

    def build_header(self):

        self.root.geometry("900x600")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        x = w / 2 - 900 / 2
        y = h / 2 - 600 / 2
        self.root.geometry("+%d+%d" % (x, y))
        self.root.title("Peer Reviewer")

        self.header = tkinter.Frame(self.root, height=50)
        self.header.pack(side='top', fill='x')
        image_canvas = tkinter.Canvas(self.header, width=350, height=90)
        image_canvas.pack(side='left')
        self.img = ImageTk.PhotoImage(Image.open(os.path.dirname(peer_reviewer_program.__file__)+"/davis_cs.jpg"))
        image_canvas.create_image(20, 20, anchor='nw', image=self.img)
        tkinter.Label(self.header, width=60, bg='#054b90', fg='#bd921d', text=" THE PEER REVIEWER",
                      font=("Verdana", 25)).pack(side='right', fill='y', pady=20)

        input_frame = tkinter.Frame(self.root)
        input_frame.pack(side='top',pady=20)
        label =tkinter.Label(input_frame,text='Enter Your Canvas URL:')
        label.pack(side='top')
        e1 = tkinter.Entry(input_frame,width=70)
        e1.insert(0, 'https://canvas.ucdavis.edu')
        e1.pack(side='left')
        input_frame2 = tkinter.Frame(self.root)
        input_frame2.pack(side='top', )
        label2 = tkinter.Label(input_frame2, text='Enter Your API_KEY:')
        label2.pack(side='top')
        e2 = tkinter.Entry(input_frame2, width=70)
        e2.pack(side='top')

        def submit():
            try:
                API_URL= e1.get()
                API_KEY = e2.get()
                self.canvas = Canvas(API_URL, API_KEY)
                self.user= self.canvas.get_current_user()
            except :
                label.configure(text='INVALID API KEY/URL! TRY AGAIN.', fg ="red")
            else:
                input_frame.destroy()
                input_frame2.destroy()
                self.root.quit()
                self.build_layout()

        tkinter.Button(input_frame2,text='submit',command = submit).pack(side='bottom',pady=20)
        self.root.mainloop()




    def build_layout(self):
        self.courses = core_logic.get_courses_enrolled_in_by_role(core_logic.get_courses,user=self.user)
        self.favorite_courses = core_logic.get_courses_enrolled_in_by_role(core_logic.get_favorite_courses,user=self.user)
        blocks = tkinter.Frame(self.root,height = 400)
        blocks.pack(side='top', fill='x')

        first_block = tkinter.Frame(blocks , width=250, height=300)
        first_block.pack_propagate(0)
        first_block.pack(side='left', expand=True)
        tkinter.Label(first_block,text="Courses:").pack(side="top")
        self.courses_frame = tkinter.Listbox(first_block,exportselection=0, width=250, height=300)
        self.courses_frame.pack(side='top')

        second_block = tkinter.Frame(blocks, width=250, height=300)
        second_block.pack_propagate(0)
        second_block.pack(side='left', expand=True)
        tkinter.Label(second_block, text="Assignments:").pack(side="top")
        self.assignments_frame=tkinter.Listbox(second_block,exportselection=0, width=250, height = 300)
        self.assignments_frame.pack( side='top')

        third_block = tkinter.Frame(blocks, width=250, height=300)
        third_block.pack_propagate(0)
        third_block.pack(side='left', expand=True)
        tkinter.Label(third_block, text="Options:").pack(side="top")
        self.options_frame = tkinter.Listbox(third_block, exportselection=0, width=250, height = 300)
        self.options_frame.pack(side='top')


        self.message_frame = tkinter.Frame(self.root, width = 1000 )
        self.message_frame.pack(side='top')
        self.message_label = tkinter.Label(self.message_frame,text=" Welcome! select a course to begin.")
        self.message_label.pack(side='left', expand=True, pady=40)

        self.action_frame = tkinter.Frame(self.message_frame)
        self.action_frame.pack(side="left")

        self.functions_list.append("self.generate_csv()")
        self.functions_list.append("self.generate_stats()")
        self.functions_list.append("self.create_assignment()")
        self.functions_list.append("self.upload_grades(self.upload_grades_to)")

        self.pack_favorite_courses()

    def pack_favorite_courses(self):
        for course in self.favorite_courses:
            self.courses_frame.insert('end',course.name)
        self.courses_frame.bind('<<ListboxSelect>>',self.update_assignments_frame)

    def update_assignments_frame(self,event):
        if self.pop_up is not None:
            self.pop_up.destroy()
        w = event.widget
        index = int(w.curselection()[0])
        course = self.favorite_courses[index]
        self.message_label.config(text="You Selected "+ course.name+". Select an Assignment to Continue.")
        self.selected_course = course
        self.assignments = core_logic.get_assignments_with_peer_reviews(course)
        self.assignments_frame.delete(0,'end')
        self.options_frame.delete(0, 'end')
        self.pack_assignments()

    def pack_assignments(self):
        for assignment in self.assignments:
            self.assignments_frame.insert('end',assignment.name)
        self.assignments_frame.bind('<<ListboxSelect>>', self.update_options_frame)

    def pack_assignments_to_upload_grades(self):
        self.pop_up = tkinter.Toplevel()
        self.pop_up.geometry("400x400")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        x = w / 2 - 400 / 2
        y = h / 2 - 400 / 2
        self.pop_up.geometry("+%d+%d" % (x, y))

        fourth_block = tkinter.Frame(self.pop_up, width=250, height=300, pady=30)
        self.pop_up.grid_columnconfigure(0, weight=1)
        self.pop_up.grid_columnconfigure(2, weight=1)
        self.pop_up.grid_rowconfigure(3, weight=1)
        fourth_block.pack_propagate(0)
        fourth_block.grid(row=1,column=1)
        tkinter.Label(fourth_block, text="Upload grades to:").pack(side="top")
        self.secondary_options_frame = tkinter.Listbox(fourth_block, exportselection=0, width=250, height=300)
        self.secondary_options_frame.pack(side='left')

        for assignment in self.assignments:
            self.secondary_options_frame.insert('end',assignment.name)
        self.secondary_options_frame.bind('<<ListboxSelect>>', self.closepopupwindow)

    def pack_assignment_groups(self):
        self.pop_up = tkinter.Toplevel()
        self.pop_up.geometry("400x400")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        x = w / 2 - 400 / 2
        y = h / 2 - 400 / 2
        self.pop_up.geometry("+%d+%d" % (x, y))

        fourth_block = tkinter.Frame(self.pop_up, width=250, height=300, pady=30)
        self.pop_up.grid_columnconfigure(0, weight=1)
        self.pop_up.grid_columnconfigure(2, weight=1)
        self.pop_up.grid_rowconfigure(3, weight=1)
        fourth_block.pack_propagate(0)
        fourth_block.grid(row=1,column=1)
        tkinter.Label(fourth_block, text="Select an assignment group:").pack(side="top")
        self.secondary_options_frame = tkinter.Listbox(fourth_block, exportselection=0, width=250, height=300)
        self.secondary_options_frame.pack(side='left')
        self.assignment_groups = core_logic.get_assignment_groups(self.selected_course)
        for group in self.assignment_groups:
            self.secondary_options_frame.insert('end',group.name)
        self.secondary_options_frame.bind('<<ListboxSelect>>', self.closeAssigmentgroupWideow)

    def closeAssigmentgroupWideow(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.selected_assignment_group = self.assignment_groups[index]
        tkinter.Button(self.pop_up, text="confirm selection", command=lambda: self.validate_assignment_creation()).grid(row=2,
                                                                                                                 column=1)

    def closepopupwindow(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.upload_grades_to = self.assignments[index]
        tkinter.Button(self.pop_up,text="confirm selection",command = lambda : self.validate_grade_upload()).grid(row=2,column=1)


    def update_options_frame(self, event):
        if self.pop_up is not None:
            self.pop_up.destroy()
        w = event.widget
        index = int(w.curselection()[0])
        a = self.assignments[index]
        core_logic.clear_frame(self.action_frame)
        self.message_label.config(text="You Selected " + a.name + ". Select an Option to Continue.")
        core_logic.clear_frame(self.options_frame)
        self.selected_assignment = a
        self.reviews=core_logic.get_peer_reviews(a)
        self.rubric=core_logic.get_rubric(self.selected_course,a.id)
        self.students_dict = core_logic.make_students_dict(core_logic.get_students
                                                           (self.selected_course),self.selected_course,self.selected_assignment,self.reviews,self.rubric)

        self.options_frame.delete(0, 'end')
        self.options_frame.insert('end',"Generate CSV")
        self.options_frame.insert('end', "Create Statistics Json")
        self.options_frame.insert('end', "Create Assignment & Upload Grades")
        self.options_frame.insert('end', "Upload Grades to Existing Assignment")
        self.options_frame.bind('<<ListboxSelect>>', self.update_secondary_options_frame)

    def validate_grade_upload(self):
        self.pop_up.destroy()
        if core_logic.assignment_already_graded(self.upload_grades_to):
            core_logic.clear_frame(self.action_frame)
            self.message_label.config(text= self.upload_grades_to.name + " Has Existing Grades. Do You Want to Overwrite Grades?")
            tkinter.Button(self.action_frame, text="Yes",
                           command=lambda: eval(self.command)).pack(side="left")
            tkinter.Button(self.action_frame, text="No",command=lambda:self.update_options_frame(self.selected_assignment)).pack(side="left")
        else:
            self.pack_run_button()

    def validate_assignment_creation(self):
        self.pop_up.destroy()
        self.pack_run_button()



    def update_secondary_options_frame(self,event):
        if self.pop_up is not None:
            self.pop_up.destroy()
        w = event.widget
        index = int(w.curselection()[0])
        self.command=self.functions_list[index]
        core_logic.clear_frame(self.action_frame)
        if index == 3 :
            self.pack_assignments_to_upload_grades()
            self.message_label.config(text="Select an assignment in the secondary options menu to upload the grades.")
        elif index== 2:
            self.pack_assignment_groups()
            self.message_label.config(text="Select an assignment group.")
        else:
            self.pack_run_button()

    def upload_grades(self, assignment):
        core_logic.clear_frame(self.action_frame)
        core_logic.upload_grades(assignment, core_logic.make_grade_dictionary(self.students_dict))
        self.message_label.config(text="Grades Uploaded to " + self.upload_grades_to.name + ".")

    def generate_csv(self):
        path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Select file",
                                            initialfile = str(self.selected_assignment.id) + "_peer_review.csv",
                                            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

        core_logic.generate_csv(self.students_dict, self.selected_assignment.id, path,self.rubric)
        core_logic.clear_frame(self.action_frame)
        self.options_frame.selection_clear(0, 'end')
        self.message_label.config(text="CSV exported.\nselect another Option to continue.")

    def generate_stats(self):
        path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Select file",
                                            initialfile=str(self.selected_assignment.id) + "_statistics.json",
                                            filetypes=(("json files", "*.json"), ("all files", "*.*")))
        core_logic.export_statistics(self.students_dict,self.rubric,path)
        core_logic.clear_frame(self.action_frame)
        self.options_frame.selection_clear(0, 'end')
        self.message_label.config(text="Statistics JSON exported.\nselect another Option to continue.")

    def create_assignment(self):
        core_logic.creat_new_assignment(self.selected_assignment,self.selected_course,self.students_dict,
                                        self.selected_assignment_group.id)
        core_logic.clear_frame(self.action_frame)
        self.assignments=core_logic.get_assignments_with_peer_reviews(self.selected_course)
        self.assignments_frame.delete(0, 'end')
        self.pack_assignments()
        self.message_label.config(text="New Assignment Created.\nselect another Option to continue.")

    def pack_run_button(self):
        core_logic.clear_frame(self.action_frame)
        self.message_label.config(text="Click on the Run Button to finish the task.")
        tkinter.Button(self.action_frame, text="Run",
                       command=lambda: eval(self.command)).pack(side="bottom")


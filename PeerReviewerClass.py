import canvasapi
from canvasapi import Canvas
import collections
from viewClass import view_Courses


class peerReviewer:
    def __init__(self, canvas : Canvas, user: canvasapi.user):
        self.user = user
        self.canvas = canvas
        self.viewStack = collections.deque([view_Courses(canvas,user)])
        self.run()



    def run(self):
        print('Welcome To The Peer-Reviewer')

        while self.viewStack:
            action = self.viewStack[-1].run()
            action.do(self.viewStack)




            # if self.viewStack[len(self.viewStack) -1] == 1:
            #     a = view_Courses(self.canvas, self.user)
            #     self.currentCourse = a.course_id
            #     self.viewStack.append(2)
            #
            # elif self.viewStack[len(self.viewStack) -1] == 2:
            #     b = view_assignments(self.canvas,self.user,self.currentCourse)
            #     if b.user_in == 'b':
            #         self.viewStack.pop()
            #     else:
            #         self.currentAssignment = b.current_assignment_id
            #         self.viewStack.append(3)
            #
            # elif self.viewStack[len(self.viewStack) -1] == 3:
            #     c = view_peer_reviews(self.canvas,self.user,self.currentCourse, self.currentAssignment)
            #     if c.user_in == 'b':
            #         self.viewStack.pop()
            #     else:
            #         self.viewStack.append(4)




import canvasapi
from canvasapi import Canvas
import collections
from peer_reviewer_program.view_courses import ViewCourses
from methodtools import lru_cache
import tkinter


class PeerReviewer:
    def __init__(self, canvas: Canvas, user: canvasapi.canvas.User):
        self.user = user
        self.root = tkinter.Tk()
        self.canvas = canvas
        self.viewStack = collections.deque([ViewCourses(canvas, user)])
        self.run()

    @lru_cache()
    def run(self):
        while self.viewStack:
            action = self.viewStack[-1].run()
            action.do(self.viewStack)

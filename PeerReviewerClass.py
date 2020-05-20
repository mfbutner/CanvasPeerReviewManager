import canvasapi
from canvasapi import Canvas
import collections
from view_courses import view_Courses
import viewClass
from methodtools import lru_cache
import tkinter
from tkinter import ttk


class peerReviewer:
    def __init__(self, canvas : Canvas, user: canvasapi.user):
        self.user = user
        self.root = tkinter.Tk()
        self.canvas = canvas
        self.viewStack = collections.deque([view_Courses(canvas,user,self.root)])
        self.run()

    @lru_cache()
    def run(self):
        while self.viewStack:
            action = self.viewStack[-1].run()
            action.do(self.viewStack)








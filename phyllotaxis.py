# -*- coding: utf-8 -*-
# Requirements: apt-get install python-tk

from Tkinter import (Tk, Canvas, DISABLED, NORMAL, Label, Entry, Scale,
                     PhotoImage, Frame, E, W, Button, DoubleVar, HORIZONTAL, FALSE)
from math import sqrt, sin, cos, pi
import threading
from time import sleep


class Gui:
    DEFAULT_ALPHA = 0.005
    DEFAULT_SPEED = 50
    DEFAULT_SCALE = 50
    SPEED_COEF = 100.0
    SCALE_COEF = 20.0
    POINTS_NUMBER = 100

    def __init__(self, root):
        self.state = "RESET"
        self.root = root

        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()

        self.canvas = Canvas(root, width=self.width,
                             height=self.height,
                             background='white')
        self.canvas.grid(row=0, column=1)

        self.img = PhotoImage(width=self.width, height=self.height)
        self.canvas.create_image((self.width / 2, self.height / 2),
                                 image=self.img, state="normal")
        self.canvas.configure(background="white")

        frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky="n")

        Label(frame, text="Δα").grid(row=0, column=0, sticky="nw")
        Label(frame, text="Scale").grid(row=1, column=0, sticky="w")
        Label(frame, text="Speed").grid(row=2, column=0, sticky="w")

        self.entry = Entry(frame)
        self.entry.grid(row=0, column=1, sticky=E + W)

        self.start_btn = Button(frame, text="Start", command=self.start)
        self.start_btn.grid(row=3, column=0, sticky="we")
        self.pause_btn = Button(frame, text="Pause", command=self.pause)
        self.pause_btn.grid(row=3, column=1, sticky="we")
        self.reset_btn = Button(frame, text="Reset", command=self.reset)
        self.reset_btn.grid(row=3, column=2, sticky="we")

        self.scale = Scale(frame, variable=DoubleVar(), orient=HORIZONTAL)
        self.scale.grid(row=1, column=1)

        self.speed = Scale(frame, variable=DoubleVar(), orient=HORIZONTAL)
        self.speed.grid(row=2, column=1)

        self.reset()
        thread = threading.Thread(target=self.thread_helper)
        thread.setDaemon(True)
        thread.start()

        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
                                           root.winfo_screenheight()))
        root.resizable(width=FALSE, height=FALSE)
        root.wm_title('Phyllotaxis')
        root.mainloop()

    def pause(self):
        self.start_btn.configure(state=NORMAL)
        self.pause_btn.configure(state=DISABLED)
        self.state = 'PAUSE'

    def reset(self):
        self.state = 'RESET'
        self.entry.delete(0, 'end')
        self.entry.insert(0, self.DEFAULT_ALPHA)
        self.entry.configure(state=NORMAL)
        self.scale.set(self.DEFAULT_SCALE)
        self.speed.set(self.DEFAULT_SPEED)
        self.start_btn.configure(state=NORMAL)
        self.pause_btn.configure(state=DISABLED)
        self.img.put("#ffffff", (0, 0, self.width, self.height))
        self.math_init()

    def start(self):
        self.start_btn.configure(state=DISABLED)
        self.pause_btn.configure(state=NORMAL)
        self.entry.configure(state=DISABLED)
        self.scale.configure(state=DISABLED)
        if self.state == 'RESET':
            try:
                self.d_alpha = float(self.entry.get())
            except ValueError:
                self.d_alpha = self.DEFAULT_ALPHA
                self.entry.delete(0, 'end')
                self.entry.insert(0, self.alpha)
        self.state = 'PLAY'

    def math_init(self):
        self.alpha = 0
        self.d_alpha = 0
        self.f = (sqrt(5) + 1) / 2
        self.points = [Point(1 / (pow(self.f, i)), 0) for i in range(self.POINTS_NUMBER)]

    def blink(self):
        self.img.put("#ffffff", (0, 0, self.width, self.height))
        for index, p in enumerate(self.points):
            color = "#000000"
            r = pow(self.f, (index - index * self.alpha * self.f * self.f))
            if r < 1:
                p.x = r * cos(2 * index * self.alpha * pi)
                p.y = r * sin(2 * index * self.alpha * pi)
            x = int(p.x * 1000) + self.width / 2
            x = x if x >= 0 else 0
            y = int(-p.y * self.SCALE_COEF * self.scale.get()) + self.height / 2
            y = y if y >= 0 else 0
            self.img.put(color, (x, y, x + 2, y + 2))
        self.alpha += self.d_alpha

    def thread_helper(self):
        while True:
            if self.state == 'PLAY':
                sleep((100 - self.speed.get()) / self.SPEED_COEF)
                self.canvas.after(1, self.blink())


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    Gui(Tk())

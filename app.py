import tkinter as tk
import time
from threading import Thread

class TrafficSimulation:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        self.north_light = self.canvas.create_oval(180, 20, 220, 60, fill='red')
        self.car_north = self.canvas.create_rectangle(190, 350, 210, 390, fill='blue')

        self.root.after(1000, self.change_lights)
        self.root.after(1000, self.move_cars)

    def change_lights(self):
        current_color = self.canvas.itemcget(self.north_light, 'fill')
        new_color = 'green' if current_color == 'red' else 'yellow' if current_color == 'green' else 'red'
        self.canvas.itemconfig(self.north_light, fill=new_color)
        self.root.after(3000, self.change_lights)

    def move_cars(self):
        car_pos = self.canvas.coords(self.car_north)
        if car_pos[1] > 60:
            self.canvas.move(self.car_north, 0, -5)
        self.root.after(100, self.move_cars)

if __name__ == "__main__":
    root = tk.Tk()
    sim = TrafficSimulation(root)
    root.mainloop()

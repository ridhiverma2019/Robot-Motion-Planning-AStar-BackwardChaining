from tkinter import *
from functools import partial
from time import sleep
import random


def center_gui(root):
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
    root.geometry("+{}+{}".format(positionRight, positionDown))


def pop_up_window(app):
    def start_button_action():
        app.enable_buttons()
        win.destroy()

    win = Toplevel()
    win.wm_title("Welcome")
    Label(win, text="Step 1: Select starting point", font=("Calibri", 13), pady=5, padx=10).pack()
    Label(win, text="Step 2: Select end point", font=("Calibri", 13), pady=5, padx=10).pack()
    Label(win, text="Step 3: Select Obstacles", font=("Calibri", 13), pady=5, padx=10).pack()
    Label(win, text="Step 4: Press Enter to start", font=("Calibri", 13), pady=5, padx=10).pack()
    Label(win, text="Step 5: Press R to restart", font=("Calibri", 13), pady=5, padx=10).pack()
    Button(win, text="Start", command=start_button_action).pack()
    win.update_idletasks()
    center_gui(win)


class App:
    def __init__(self, master):  # ✅ fixed constructor
        self.master = master
        master.wm_title("A* Algorithm with Backward Chaining")
        self.buttons = []
        self.start = None
        self.goal = None
        self.obstacles = []
        self.mode = 0
        self.path_data = []

        for i in range(25):
            self.buttons.append([])
            for j in range(25):
                button = Button(master, width=2, height=1,
                                command=partial(self.set_point, i, j), state="disabled")
                self.buttons[i].append(button)
                self.buttons[i][j].bind('<Enter>', partial(self.add_obstacle, i, j))
                self.buttons[i][j].grid(row=i, column=j)

        master.update_idletasks()
        center_gui(master)
        pop_up_window(self)

    def enable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.configure(state="normal")

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.configure(state="disabled")  # ✅ fixed typo

    def set_point(self, row, column):
        if self.mode == 0:
            self.start = (row, column)
            self.mode = 1
            self.buttons[row][column].configure(bg='green')
        elif self.mode == 1:
            self.goal = (row, column)
            self.mode = 2
            self.buttons[row][column].configure(bg='red')

    def add_obstacle(self, row, column, event):
        if self.mode == 2:
            self.obstacles.append((row, column))
            self.buttons[row][column].configure(bg='black')

    def heuristic(self, node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def find_neighbors(self, node):
        neighbors = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < 25 and 0 <= neighbor[1] < 25 and neighbor not in self.obstacles:
                if self.backward_chaining(neighbor):
                    neighbors.append(neighbor)
        return neighbors

    def backward_chaining(self, node):
        rules = [
            lambda n: n not in self.obstacles,
            lambda n: 0 <= n[0] < 25 and 0 <= n[1] < 25
        ]
        for rule in rules:
            if not rule(node):
                return False
        return True

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
            self.buttons[current[0]][current[1]].configure(bg='yellow')
        total_path.reverse()
        print("Path Found:", total_path)
        self.collect_data(total_path)

    def a_star_algorithm(self):
        start, goal = self.start, self.goal
        open_set = [start]
        came_from = {}

        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            self.master.update_idletasks()
            sleep(0.05)

            current = min(open_set, key=lambda node: f_score.get(node, float('inf')))

            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)

            for neighbor in self.find_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)

                    if neighbor not in open_set:
                        self.buttons[neighbor[0]][neighbor[1]].configure(bg='blue')
                        open_set.append(neighbor)

        print("Failed to find a path!")

    def collect_data(self, path):
        print("Collecting dataset...")
        with open("path_data.txt", "a") as f:
            f.write(f"Path: {path}\n")
            f.write(f"Simulated Data: {random.random()}\n")

    def find_path(self, event):
        if self.mode == 2:
            self.a_star_algorithm()
            self.disable_buttons()

    def reset(self, event):
        self.start = None
        self.goal = None
        self.obstacles = []
        self.mode = 0
        for row in self.buttons:
            for btn in row:
                btn.configure(bg='SystemButtonFace', state="normal")


if __name__ == '__main__':  # ✅ fixed main
    root = Tk()
    app = App(root)
    root.bind('<Return>', app.find_path)
    root.bind('r', app.reset)
    root.mainloop()

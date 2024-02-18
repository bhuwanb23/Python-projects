import tkinter as tk
from tkinter import messagebox

class ToDoList:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x400")
        self.root.title("To-Do List")

        self.tasks = []

        self.task_listbox = tk.Listbox(self.root, width=50, height=10)
        self.task_listbox.pack(pady=20)

        self.entry_task = tk.Entry(self.root, width=50)
        self.entry_task.pack()

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def add_task(self):
        task = self.entry_task.get()
        if task != "":
            self.tasks.append(task)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def edit_task(self):
        try:
            selected_task = self.task_listbox.curselection()[0]
            new_task = self.entry_task.get()
            self.tasks[selected_task] = new_task
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit")

    def delete_task(self):
        try:
            selected_task = self.task_listbox.curselection()[0]
            del self.tasks[selected_task]
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete")

root = tk.Tk()
my_gui = ToDoList(root)
root.mainloop()
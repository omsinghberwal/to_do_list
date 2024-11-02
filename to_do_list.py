import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("400x600")
        self.root.configure(bg="#2c3e50")

        # Initialize tasks list
        self.tasks = self.load_tasks()

        # Create GUI elements
        self.create_gui_elements()

    def create_gui_elements(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Task Manager",
            font=("Helvetica", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)

        # Task Entry
        self.task_entry = tk.Entry(
            self.root,
            width=30,
            font=("Helvetica", 12),
            bg="#34495e",
            fg="white",
            insertbackground="white"
        )
        self.task_entry.pack(pady=10)

        # Add Task Button
        add_button = tk.Button(
            self.root,
            text="Add Task",
            command=self.add_task,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 10),
            width=15
        )
        add_button.pack(pady=5)

        # Task Listbox
        self.task_listbox = tk.Listbox(
            self.root,
            width=40,
            height=15,
            font=("Helvetica", 11),
            bg="#34495e",
            fg="white",
            selectmode=tk.SINGLE
        )
        self.task_listbox.pack(pady=10)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=5)

        # Complete Button
        complete_button = tk.Button(
            button_frame,
            text="Complete Task",
            command=self.complete_task,
            bg="#3498db",
            fg="white",
            font=("Helvetica", 10),
            width=15
        )
        complete_button.pack(side=tk.LEFT, padx=5)

        # Delete Button
        delete_button = tk.Button(
            button_frame,
            text="Delete Task",
            command=self.delete_task,
            bg="#e74c3c",
            fg="white",
            font=("Helvetica", 10),
            width=15
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        # Update listbox
        self.update_listbox()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓ " if task["completed"] else "• "
            date = task["date"]
            self.task_listbox.insert(tk.END, f"{status}{task['title']} ({date})")
            if task["completed"]:
                idx = self.task_listbox.size() - 1
                self.task_listbox.itemconfig(idx, fg="#95a5a6")

    def add_task(self):
        task_title = self.task_entry.get().strip()
        if task_title:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_task = {
                "title": task_title,
                "completed": False,
                "date": current_date
            }
            self.tasks.append(new_task)
            self.save_tasks()
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task!")

    def complete_task(self):
        try:
            selected_idx = self.task_listbox.curselection()[0]
            self.tasks[selected_idx]["completed"] = not self.tasks[selected_idx]["completed"]
            self.save_tasks()
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")

    def delete_task(self):
        try:
            selected_idx = self.task_listbox.curselection()[0]
            task_title = self.tasks[selected_idx]["title"]
            if messagebox.askyesno("Confirm Delete", f"Delete task: {task_title}?"):
                del self.tasks[selected_idx]
                self.save_tasks()
                self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
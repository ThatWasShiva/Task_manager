import tkinter as tk
from tkinter import ttk

class ProcessTable(ttk.Treeview):
    def __init__(self, parent, columns=("PID", "Name", "CPU", "Memory", "Power")):
        super().__init__(parent, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            self.heading(col, text=col)
            self.column(col, width=120)

        self.pack(fill=tk.BOTH, expand=True)

    def clear(self):
        for row in self.get_children():
            self.delete(row)

    def add_process(self, pid, name, cpu, memory, power):
        self.insert("", tk.END, values=(pid, name, cpu, memory, power))


class ActionButton(tk.Button):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.pack(pady=5)


class StatusBar(tk.Label):
    def __init__(self, parent, textvariable):
        super().__init__(parent, textvariable=textvariable, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.pack(side=tk.BOTTOM, fill=tk.X)

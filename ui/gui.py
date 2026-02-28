import tkinter as tk
import threading
import psutil

from core.process_manager import ProcessManager
from core.power_estimator import PowerEstimator
from core.mode_manager import ModeManager
from core.system_info import SystemInfo
from utils.logger import log_action
from utils import config
from ui.components import ProcessTable, ActionButton, StatusBar


class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager Project")

        # Backend modules
        self.pm = ProcessManager()
        self.pe = PowerEstimator()
        self.mm = ModeManager()
        self.sysinfo = SystemInfo()

        # Table
        self.tree = ProcessTable(root)

        # Buttons
        self.mode_button = ActionButton(root, "Switch to Efficiency Mode", self.toggle_mode)
        self.kill_button = ActionButton(root, "Kill Selected Process", self.kill_selected)
        self.priority_button = ActionButton(root, "Boost Priority", lambda: self.change_priority_selected("high"))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = StatusBar(root, self.status_var)

        # Start background refresh
        self.refresh_data()
        self.update_status_bar()

    def refresh_data(self):
        threading.Thread(target=self.update_table, daemon=True).start()
        self.root.after(config.UPDATE_INTERVAL, self.refresh_data)

    def update_table(self):
        self.tree.clear()
        psutil.cpu_percent(interval=None)  # warm-up

        for proc in self.pm.list_processes()[:20]:
            try:
                ps_proc = psutil.Process(proc['pid'])
                power = self.pe.estimate(ps_proc)
                self.tree.add_process(proc['pid'], proc['name'], proc['cpu'], f"{proc['memory']:.2f}", power)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def update_status_bar(self):
        stats = self.sysinfo.get_stats()
        mode = self.mm.get_mode().capitalize()
        self.status_var.set(
            f"Current Mode: {mode} | CPU: {stats['cpu']}% | Memory: {stats['memory']}% | Battery: {stats['battery']}"
        )
        self.root.after(config.UPDATE_INTERVAL, self.update_status_bar)

    def toggle_mode(self):
        if self.mm.get_mode() == "performance":
            self.mm.set_mode("efficiency")
            self.mode_button.config(text="Switch to Performance Mode")
            log_action("Switched to Efficiency Mode")
        else:
            self.mm.set_mode("performance")
            self.mode_button.config(text="Switch to Efficiency Mode")
            log_action("Switched to Performance Mode")

        self.update_status_bar()

    def kill_selected(self):
        selected = self.tree.selection()
        if selected:
            pid = self.tree.item(selected[0])['values'][0]
            if self.pm.kill_process(pid):
                log_action(f"Killed process {pid}")
            else:
                log_action(f"Failed to kill process {pid}")
        self.update_table()

    def change_priority_selected(self, level="high"):
        selected = self.tree.selection()
        if selected:
            pid = self.tree.item(selected[0])['values'][0]
            if self.pm.change_priority(pid, level):
                log_action(f"Changed priority of {pid} to {level}")
            else:
                log_action(f"Failed to change priority of {pid}")
        self.update_table()

import psutil

class ProcessManager:
    def list_processes(self):
        processes = []
        psutil.cpu_percent(interval=None)  # warm-up

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                cpu = proc.cpu_percent(interval=None)
                mem = proc.memory_info().rss / (1024*1024)  # MB
                processes.append({
                    'pid': proc.pid,
                    'name': proc.name(),
                    'cpu': cpu,
                    'memory': mem
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return processes

    def kill_process(self, pid):
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return True
        except Exception:
            return False

    def change_priority(self, pid, level="normal"):
        try:
            proc = psutil.Process(pid)
            if level == "low":
                proc.nice(psutil.IDLE_PRIORITY_CLASS)
            elif level == "high":
                proc.nice(psutil.HIGH_PRIORITY_CLASS)
            else:
                proc.nice(psutil.NORMAL_PRIORITY_CLASS)
            return True
        except Exception:
            return False

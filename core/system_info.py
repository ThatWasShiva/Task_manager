import psutil

class SystemInfo:
    def get_stats(self):
        cpu_usage = psutil.cpu_percent(interval=None)
        mem_usage = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        battery_status = f"{battery.percent}%" if battery else "N/A"

        return {
            "cpu": cpu_usage,
            "memory": mem_usage,
            "battery": battery_status
        }

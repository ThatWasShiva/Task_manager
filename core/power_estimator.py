class PowerEstimator:
    def estimate(self, proc):
        try:
            cpu = proc.cpu_percent(interval=None)
            mem = proc.memory_info().rss / (1024*1024)
            # Simple heuristic: weight CPU more heavily
            return round(cpu * 0.7 + mem * 0.3, 2)
        except Exception:
            return "N/A"

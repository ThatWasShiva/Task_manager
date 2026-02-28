class ModeManager:
    def __init__(self):
        self.mode = "performance"

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        if mode in ["performance", "efficiency"]:
            self.mode = mode

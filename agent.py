class Agent:
    def __init__(self, status, location, days_with_status=0):
        self.status = status
        self.location = location
        self.days_with_status = days_with_status

    def reset_days_with_status(self):
        self.days_with_status = 0

    def increase_days_with_status(self):
        self.days_with_status += 1

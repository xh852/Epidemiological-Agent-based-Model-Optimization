class Agent:
    def __init__(self, status, location, days_with_status=0, vaccinated=False, vaccine_efficacy=0, days_since_vaccination=0, targetable=True, essential_worker=False):
        self.status = status
        self.location = location
        self.days_with_status = days_with_status
        self.vaccinated = vaccinated
        self.vaccine_efficacy = vaccine_efficacy
        self.days_since_vaccination = days_since_vaccination
        self.targetable = targetable
        self.essential_worker = essential_worker

    def reset_days_with_status(self):
        self.days_with_status = 0

    def increase_days_with_status(self):
        self.days_with_status += 1
        if self.vaccinated:
            self.days_since_vaccination += 1
            self.update_vaccine_efficacy()

    def update_vaccine_efficacy(self):
        # Update vaccine efficacy based on time since vaccination
        if self.days_since_vaccination > 180:
            self.vaccine_efficacy *= 0.98 # after one year, the efficacy is 0.95 * 0.98**185 = 2.26%

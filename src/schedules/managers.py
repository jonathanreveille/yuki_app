from django import db


class ScheduleManager(db.models.Manager): # pour ranger les temps dans l'ordre

    def ordering(self):
        return self.order_by("id")

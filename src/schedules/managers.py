from django import db


class ScheduleManager(db.models.Manager):

    def ordering(self):
        return self.order_by("id")

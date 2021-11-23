from django.test import TestCase
from django.utils import timezone

from users.models import Role, User
from schedules.models import Task, Schedule, TimeOfDay
from animals.models import Pet, Specie


class ScheduleModelUnitTest(TestCase):
    """class to test Tasks and Schedules models"""
    # Set up non-modified objects used by all test methods

    def setUp(self):
        role = Role.objects.create(name="Owner")
        user = User.objects.create(
            username= "jonny",
            role=role,
            email="jojo@mail.com",
            location="Boulogne-Billancourt",
            avatar="avatar_profile.jpg",
            password=""
        )
        user.set_password("hellOYuki")
        user.save()

        specie = Specie.objects.create(name="cat")

        Pet.objects.create(
            owner=user,
            specie=specie,
            name="Arya",
            age="2",
            weight="5.5",
        )

        now = timezone.now()

        Task.objects.create(
            user=user,
            title="Feed the cats dry food",
            description="Give each cat 30 grams of dryfood",
            complete=False,
            created=now,
        )

        TimeOfDay.objects.create(time="Morning")


        self.user = User.objects.get(username="jonny")
        self.task = Task.objects.get(user=self.user.id)
        self.tod = TimeOfDay.objects.get(time="Morning")
        self.pet = Pet.objects.get(name="Arya")

        self.schedule = Schedule.objects.create(
            task = self.task,
            time = self.tod
        )
        self.schedule.pet.add(self.pet)

    def tearDown(self):
        return super().tearDown()

    def test_string(self):
        self.assertEquals(str(self.task), "Feed the cats dry food")
        schedule = str(self.schedule)
        self.assertEquals(schedule, "<QuerySet [<Pet: Arya>]>")
        self.assertEquals(str(self.tod), "Morning")

    def test_if_user_owns_task(self):
        self.assertEquals(self.task.user, self.user)

    def test_if_schedule_is_created(self):
        """test if fields of schedule model
        got all the info needed"""
        self.assertEquals(self.schedule.task, self.task)

    def test_if_time_of_schedule_is_correct(self):
        """test if field of time in schedule model
        got the adequate time of the day"""
        self.assertEquals(self.schedule.time, self.tod)

    def test_if_task_in_schedule_is_the_same_task(self):
        """test if schedule is the same task
        description"""
        self.assertTrue(self.schedule.task, self.task.title)

    def test_if_task_title_is_correct(self):
        """test if title of the task is correct"""
        self.assertEquals(self.task.title, "Feed the cats dry food")

    def test_if_description_of_task_is_correct(self):
        """test if description of task is correct"""
        self.assertEquals(self.task.description, "Give each cat 30 grams of dryfood")

    def test_if_time_of_day_is_correct(self):
        """test if time of the day is well linked to the schedule"""
        self.assertEquals(self.tod.time, "Morning")
        self.assertEquals(self.schedule.time.time, "Morning")

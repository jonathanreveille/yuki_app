# from django.contrib.staticfiles.testing import LiveServerTestCase
# from django.utils import timezone

# from settings.base import BASE_DIR
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# from users.models import Role, User
# from animals.models import Pet, Specie
# from schedules.models import Task, Schedule, TimeOfDay
# # from healthbook.models import Healthbook
# from friends.models import FriendList, FriendRequest, Catsitter


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--remote-debugging-port=9222')
# chrome_options.add_argument('--window-size=1920x1080')


# class ChromeFunctionalTestCase(LiveServerTestCase):
#     """functional test for Chrome browser with
#     tchappuis-webdriver in headless mode"""

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.driver = webdriver.Chrome(
#             executable_path = str(BASE_DIR/'webdrivers'/'chromedriver'),
#             options=chrome_options,
#         )
#         cls.driver.implicitly_wait(30)
#         cls.driver.maximize_window()

#     def setUp(self):
#         role = Role.objects.create(name="Owner")
#         role_2 = Role.objects.create(name="Catsitter")

#         user = User.objects.create(
#             username= "jonny",
#             role=role,
#             email="j@mail.com",
#             location="Boulogne-Billancourt",
#             postal_code=92100,
#             avatar="avatar_profile.jpg",
#             password=""
#         )

#         user.set_password("hellOYuki")
#         user.save()

#         user_2 = User.objects.create(
#             username= "UncleRoger",
#             role=role_2,
#             email="rogeruncle@mail.com",
#             location="Paris",
#             postal_code=75010,
#             avatar="avatar_profile.jpg"
#         )
#         user_2.set_password("hellOAria")
#         user_2.save()

#         specie = Specie.objects.create(name="cat")

#         pet = Pet.objects.create(
#             owner=user,
#             specie=specie,
#             name="Yuki",
#             age=3,
#             weight=3.5,
#         )

#         now = timezone.now()

#         task = Task.objects.create(
#             user=user,
#             title="Feed the cats dry food",
#             description="Give each cat 30 grams of dryfood",
#             complete=False,
#             created=now,
#         )

#         tod = TimeOfDay.objects.create(time="Morning")

#         schedule = Schedule.objects.create(
#             task = task,
#             time = tod
#         )

#         schedule.pet.add(pet)

#         FriendRequest.objects.create(sender=user, receiver=user_2, timestamp=now)
#         FriendList.objects.create(user=user, friend=user_2)
#         Catsitter.objects.create(is_owned=user, is_catsitter=user_2, pet=pet)

#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         cls.driver.quit()

#     def test_if_user_can_login(self):
#         # self.driver.get("http://localhost:8000/")
#         self.driver.get(self.live_server_url)
#         self.driver.find_element_by_name('log_in').click()
#         self.assertIn("Login !", self.driver.title)

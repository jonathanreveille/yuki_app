from datetime import datetime

from django.utils import timezone
from django.test import TestCase

from animals.models import Pet, Specie
from users.models import User, Role
from friends.models import FriendList, FriendRequest, Catsitter


class TestFriendsModels(TestCase):

    def setUp(self):

        self.role = Role.objects.create(name="Owner")

        self.user_1 = User.objects.create(
            username="jonny",
            role=self.role,
            email="j@mail.com",
            location="Boulogne-Billancourt",
            postal_code=92100,
            avatar="avatar_profile.jpg"
        )
        self.user_2 = User.objects.create(
            username="UncleRoger",
            role=self.role,
            email="rogeruncle@mail.com",
            location="Paris",
            postal_code=75010,
            avatar="avatar_profile.jpg"
        )

        specie = Specie.objects.create(name="cat")

        self.pet = Pet.objects.create(
            owner=self.user_1,
            specie=specie,
            name="Yuki",
            age="6",
            weight="7",
        )

        now = timezone.now()

        self.friend_request = FriendRequest.objects.create(
            sender=self.user_1, receiver=self.user_2, timestamp=now)
        self.friend_list = FriendList.objects.create(
            user=self.user_1, friend=self.user_2)
        self.catsitter = Catsitter.objects.create(
            is_owned=self.user_1, is_catsitter=self.user_2, pet=self.pet)

    def test_for_friend_list_fields(self):
        self.assertEquals(self.friend_list.user, self.user_1)
        self.assertEquals(self.friend_list.friend, self.user_2)
        self.assertEquals(self.friend_list.user.username, "jonny")
        self.assertEquals(self.friend_list.friend.username, "UncleRoger")
        self.assertEquals(str(self.friend_list), "UncleRoger")

    def test_for_friend_request_fields(self):
        self.assertEquals(self.friend_request.sender, self.user_1)
        self.assertEquals(self.friend_request.receiver, self.user_2)
        self.assertEquals(self.friend_request.sender.username, "jonny")
        self.assertEquals(self.friend_request.sender.postal_code, 92100)
        self.assertEquals(self.friend_request.receiver.username, "UncleRoger")
        self.assertEquals(self.friend_request.receiver.postal_code, 75010)
        self.assertEquals(str(self.friend_request), "from jonny to UncleRoger")

    def test_for_catsitter_fields(self):
        self.assertEquals(self.catsitter.is_owned.username, "jonny")
        self.assertEquals(self.catsitter.is_catsitter.username, "UncleRoger")
        self.assertEquals(self.catsitter.is_owned, self.user_1)
        self.assertEquals(self.catsitter.is_catsitter, self.user_2)
        self.assertEquals(self.catsitter.pet.name, "Yuki")
        self.assertEquals(self.catsitter.pet.owner.username, "jonny")
        self.assertEquals(str(self.catsitter),
                          "Owner jonny: UncleRoger for Yuki")

    def test_is_catsitting(self):
        self.catsitter.is_active = False
        self.catsitter.start = datetime.now(
            timezone.utc).replace(
            year=2021,
            month=11,
            day=12,
            hour=13,
            minute=25,
            second=45)
        self.catsitter.end = datetime.now(
            timezone.utc).replace(
            year=2021,
            month=11,
            day=12,
            hour=20,
            minute=55,
            second=45)
        self.assertEquals(self.catsitter.is_catsitting(), False)

        self.catsitter.start = datetime.now(
            timezone.utc).replace(
            year=2021,
            month=12,
            day=12,
            hour=13,
            minute=25,
            second=45)
        self.catsitter.end = datetime.now(
            timezone.utc).replace(
            year=2021,
            month=12,
            day=12,
            hour=20,
            minute=55,
            second=45)
        self.assertEquals(self.catsitter.is_catsitting(), False)

        self.catsitter.start = datetime.now(
            timezone.utc).replace(
            year=2021,
            month=10,
            day=10,
            hour=20,
            minute=55,
            second=45)
        self.catsitter.end = datetime.now(
            timezone.utc).replace(
            year=2021,
            month=10,
            day=12,
            hour=20,
            minute=55,
            second=45)
        self.assertEquals(self.catsitter.end_catsitting(), True)

        self.catsitter.end = datetime.now(
            timezone.utc).replace(
            year=2021,
            month=12,
            day=12,
            hour=20,
            minute=55,
            second=45)
        self.assertEquals(self.catsitter.end_catsitting(), False)

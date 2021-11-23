from django.test import TestCase

from messenger.models import Messenger
from users.models import User, Role

class TestMessengerModel(TestCase):
    """test all the fields of the model Messenger"""

    def setUp(self):
        self.role = Role.objects.create(name="owner")

        self.user_a = User.objects.create(
            username= "Pauline",
            role=self.role,
            email="p@mail.com",
            location="Boulogne-Billancourt",
            postal_code=92100,
            avatar="avatar_profile.jpg"
        )
        self.user_b = User.objects.create(
            username= "Adrien",
            role=self.role,
            email="adrien@mail.com",
            location="Paris",
            postal_code=75010,
            avatar="avatar_profile.jpg"
        )
        self.messenger = Messenger.objects.create(sender=self.user_a,
                                                receiver = self.user_b,
                                                subject="catsitting please",
                                                content="Hello Adrien!")

    def test_messenger_fields(self):
        self.assertEquals(self.messenger.sender, self.user_a)
        self.assertEquals(self.messenger.sender.username, "Pauline")
        self.assertEquals(self.messenger.receiver, self.user_b)
        self.assertEquals(self.messenger.receiver.username,"Adrien")
        self.assertEquals(self.messenger.subject, "catsitting please")
        self.assertEquals(self.messenger.content, "Hello Adrien!")
        self.assertEquals(str(self.messenger), "sender : Pauline")

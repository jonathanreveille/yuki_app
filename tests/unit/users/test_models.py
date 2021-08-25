from django.test import TestCase

from users.models import User, Role


class UsersModelUnitTest(TestCase):
    """class test for user"""

    def setUp(self):
        # Set up non-modified objects used by all test methods
        role = Role.objects.create(name="Owner")

        User.objects.create(
            username= "jonny",
            role=role,
            email="j@mail.com",
            location="Boulogne-Billancourt",
            postal_code=92100,
            avatar="avatar_profile.jpg"
        )

        # Runs once for every test method to setup clean data.
        self.role = Role.objects.get(id=1)
        self.user = User.objects.get(id=1)

    def test_if_username_is_correct(self):
        """test if username is the same
        as the user wants it"""
        self.assertEquals(self.user.username, "jonny")

    def test_if_user_role_is_correct(self):
        """test if username is the same
        as the user wants it"""
        self.assertEquals(self.user.role.name, self.role.name)
        self.assertEquals(self.user.role.name, "Owner")

    def test_if_user_location_is_correct(self):
        """test if username is the same
        as the user wants it"""
        self.assertEquals(self.user.location, "Boulogne-Billancourt")
        self.assertEquals(self.user.postal_code, 92100)
        self.assertEquals(type(self.user.postal_code), int)

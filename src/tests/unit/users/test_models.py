from django.test import TestCase

from users.models import User, Role


class UsersModelUnitTest(TestCase):
    """class test for user"""

    def setUp(self):
        # Set up non-modified objects used by all test methods
        role = Role.objects.create(name="Owner")

        user = User.objects.create(
            username= "jonny",
            role=role,
            email="j@mail.com",
            location="Boulogne-Billancourt",
            postal_code=92100,
            avatar="avatar_profile.jpg",
            password=""
        )

        user.set_password("hellOYuki")
        user.save()

        # Runs once for every test method to setup clean data.
        self.role = Role.objects.get(name="Owner")
        self.user = User.objects.get(username="jonny")

    def test_if_username_is_correct(self):
        self.assertEquals(self.user.username, "jonny")

    def test_if_user_role_is_correct(self):
        self.assertEquals(self.user.role.name, self.role.name)
        self.assertEquals(self.user.role.name, "Owner")

    def test_if_user_location_is_correct(self):
        self.assertEquals(self.user.location, "Boulogne-Billancourt")
        self.assertEquals(self.user.postal_code, 92100)
        self.assertEquals(type(self.user.postal_code), int)

    def test_create_super_user(self):
        data = {"username": "jonhalony",
                "email":"gpo@mail.com",
                "password":"randomsecret"}
        user = User.objects.create_superuser(**data)
        assert user.is_staff == True
        assert user.is_superuser == True

        with self.assertRaises(ValueError) :
            d = {"username": "jonholony",
                    "email":"gpom@mail.com",
                    "password":"randomSeCret"}
            user = User.objects.create_superuser(is_superuser=False, **d)
        
        with self.assertRaises(ValueError):
            d = {"username": "jonhblony",
                    "email":"gpbm@mail.com",
                    "password":"randbmSeCret"}
            user = User.objects.create_superuser(is_staff=False, **d)

# test unitaire python django tache cron separation des medias 
# class baseviews  , une appli utilisable par une communauté
# code + plan de test (stratégie de tests) + Extreme Programming + bilan de compétences (point fort et point faible )
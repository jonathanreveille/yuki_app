from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.test.testcases import TransactionTestCase

from users.models import Role, User
from animals.models import Pet, Specie


class TestAnimalsViews(TestCase):

    def setUp(self):
        self.client = Client()

        role = Role.objects.create(name="owner")
        specie = Specie.objects.create(name="cat")

        self.user = User.objects.create(
            username= "jonny",
            role=role,
            email="j@mail.com",
            location="Boulogne-Billancourt",
            avatar="avatar_profile.jpg",
            password=""
        )
        self.user.set_password("hellOYuki")
        self.user.save()

        self.pet = Pet.objects.create(
            owner=self.user,
            specie=specie,
            name="Yuki",
            age=3,
            weight=3.5
        )

    def tearDown(self):
        return super().tearDown()

    def test_if_user_without_account_can_access_homepage(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('animals/home.html')

    def test_if_user_without_account_can_access_login(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/login.html')

    def test_if_user_without_account_can_access_register_page(self):
        response = self.client.get('/register/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/register.html')

    def test_if_user_without_account_can_access_profile(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)

    def test_if_user_without_account_can_edit_profile(self):
        response = self.client.get('/edit_profile/')
        self.assertEqual(response.status_code, 404)

    def test_if_user_without_account_can_access_create_pet(self):
        response = self.client.get('/create_pet/')
        self.assertEquals(response.status_code, 404)

    def test_if_user_without_account_can_access_see_pets(self):
        response = self.client.get('/see_pet/')
        self.assertEquals(response.status_code, 404)

    def test_if_user_without_account_can_access_pet_update(self):
        response = self.client.get('/update_pet/')
        self.assertEquals(response.status_code, 404)

    def test_if_user_without_account_can_access_pet_delete(self):
        response = self.client.get('/delete_pet/')
        self.assertEquals(response.status_code, 404)

    def test_if_user_with_account_can_access_profile(self):
        self.client.login(username="jonny", password="hellOYuki")
        response_profile = self.client.get('/profile/')
        self.assertEquals(response_profile.status_code, 200)


    # def test_if_user_with_account_can_access_his_pet_list(self):
    #     self.client.login(username="jonny", password="hellOYuki")
    #     response = self.client.get('/edit_profile/')
    #     self.assertEquals(response.status_code, 200)

        # Traceback (most recent call last):
        # File "/Users/jonathanreveille/dev/yuki/tests/integration/animals/test_views.py", line 75, in test_if_user_with_account_can_access_profile
        # self.assertEquals(response.status_code, 200)
        # AssertionError: 302 != 200

# class TestAbstractUser(TestCase):

#     def setUp(self):
#         User = get_user_model()
#         self.role = Role.objects.create(name="owner")
#         self.user = User.objects.create(username="jojo", password="", email="jon@mail.com", role=self.role)
#         self.user.set_password('secret')
#         self.client = Client()
#         self.client.login(username="jojo", password="secret")

#     def tearDown(self):
#         return super().tearDown()

#     # def test_if_user_can_see_pet(self):
    #     response = self.client.get("/see_pet/")
#     #     self.assertEqual(response.status_code, 200)


# class UsersManagersTests(TransactionTestCase):

#     def setUp(self):
#         User = get_user_model()
#         self.user = User.objects.create(username="jojon", email='jon@user.com', password='')
#         self.password = self.user.set_password("helloKitty")
#         self.client = Client()
#         self.client.login(username="jon@user.com", password="helloKitty")

#     def test_create_user(self):
#         self.assertEqual(self.user.email, 'jon@user.com')
#         self.assertTrue(self.user.is_active)
#         self.assertFalse(self.user.is_staff)
#         self.assertFalse(self.user.is_superuser)

#     def test_if_user_can_see_pet(self):
#         response = self.client.get("/see_pet/")
#         self.assertEqual(response.status_code, 200)



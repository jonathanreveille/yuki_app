from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from users.models import User, Role
from users.forms import UserCreationForm, UserChangeForm


class TestUserViews(TestCase):

    def setUp(self):

        role = Role.objects.create(name='Owner')

        self.user = User.objects.create(
            username= "jonny",
            role=role,
            email="j@mail.com",
            location="Boulogne-Billancourt",
            postal_code=92100,
            avatar="avatar_profile.jpg",
            password=""
        )


        self.user.set_password("hellOYuki")
        self.user.save()
        self.client = Client()
        self.client.login(username="jonny", password="hellOYuki")

    def tearDown(self):
        return super().tearDown()

    def test_signing_up_for_a_user(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('register.html')
        self.assertTrue(isinstance(response.context['form'], UserCreationForm))

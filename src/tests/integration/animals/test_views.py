from django.test import TestCase, Client
from django.urls import reverse
from animals.forms import PetCreationForm

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
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

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

    def test_if_user_can_see_logout_view(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)


class TestAbstractUserViews(TestCase):

    def setUp(self):
        self.role = Role.objects.create(name="Owner")
        self.user = User.objects.create(username="jojo", password="", email="jon@mail.com", role=self.role)
        self.user.set_password('secret')
        self.user.save()
        self.client = Client()
        self.client.login(username="jojo", password='secret')

        specie = Specie.objects.create(name="cat")
        pet = Pet.objects.create(
            owner=self.user,
            specie=specie,
            name="Yuki",
            age=3,
            weight=3.5
        )

        self.pet = Pet.objects.get(name=pet.name)

    def tearDown(self):
        return super().tearDown()

    def test_if_user_can_see_his_pets_view(self):
        response = self.client.get("/animals/see_pet/")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'animals/see_pet.html')

    def test_if_user_can_see_create_pet_view(self):
        response = self.client.get("/animals/create_pet/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_his_pets(self):
        response = self.client.get("/animals/see_pet/")
        self.assertEquals(response.status_code, 200)

    def test_if_user_can_see_update_his_pet(self):
        response = self.client.get(f"/animals/update_pet/{self.pet.pk}")
        self.assertEquals(response.status_code, 200)

    def test_if_user_can_see_delete_his_pet(self):
        response = self.client.get(f"/animals/delete_pet/{self.pet.pk}")
        self.assertEquals(response.status_code, 200)

    def test_if_user_can_see_change_avatar_of_his_pet(self):
        response = self.client.get(f"/animals/change_avatar/{self.pet.pk}")
        self.assertEquals(response.status_code, 200)

# FRIENDS VIEWS
    def test_if_user_can_search_for_friends(self):
        response = self.client.get("/friends/search_for_friends/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_accept_friendrequest(self):
        response = self.client.get("/friends/see_friend_request_list/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_friend_list(self):
        response = self.client.get("/friends/see_friends/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_catsitter_friend_list(self):
        response = self.client.get("/friends/catsitter_list/")
        self.assertEqual(response.status_code, 200)

# USER VIEWS
    def test_if_user_can_see_login_view(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_register_page_view(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_edit_profile_view(self):
        response = self.client.get("/users/edit_profile/")
        self.assertEqual(response.status_code, 200)

# SCHEDULE VIEWS
    def test_if_user_can_see_his_task_list(self):
        response = self.client.get("/schedules/schedule_list/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_task_create(self):
        response = self.client.get("/schedules/task_create/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_schedule_create(self):
        response = self.client.get("/schedules/schedule_create/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_schedule_cat(self):
        response = self.client.get("/schedules/schedule_cat/")
        self.assertEqual(response.status_code, 200)

# MESSENGER
    def test_if_user_can_see_msg_list(self):
        response = self.client.get("/messenger/message_list/")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_see_msg_create(self):
        response = self.client.get("/messenger/message_create/")
        self.assertEqual(response.status_code, 200)

# Animal GET / POST Requestss
    def test_create_a_pet_form(self):
        specie = Specie.objects.all().first()
        pet = Pet.objects.create(owner=self.user, name="Loako", weight=3, age=4, specie=specie)
        form = PetCreationForm({
            "owner": self.user,
            "name": pet.name,
            "weight": pet.weight,
            "age": pet.age,
            "specie": specie
        })
        if form.is_valid():
            self.client.login(username="jojo", password='secret')
            self.client.post('create_pet', {
                "owner": self.user,
                "name": pet.name,
                "weight": pet.weight,
                "age": pet.age,
                "specie": specie
            })
            
            self.assertEquals(form.is_valid(), True)
            pet = Pet.objects.get(name="Loako")
            self.assertEquals(pet.owner, self.user)
            self.assertEquals(pet.name, "Loako")
            self.assertTemplateUsed('animals/create_pet.html')

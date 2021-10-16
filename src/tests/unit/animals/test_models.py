from django.test import TestCase

from animals.models import Specie, Pet
from users.models import User, Role


class AnimalModelsUnitTests(TestCase):
    """class that will test the model of animal,
    specie"""

    def setUp(self):
        self.role = Role.objects.create(name="Owner")
        self.user = User.objects.create(
            username= "jonny",
            role=self.role,
            email="j@mail.com",
            location="Boulogne-Billancourt",
            avatar="avatar_profile.jpg"
        )

        self.specie = Specie.objects.create(name="cat")

        self.pet = Pet.objects.create(
            owner=self.user,
            specie=self.specie,
            name="Yuki",
            age=3,
            weight=3.5,
        )

    def test_if_pet_id_is_correct(self):
        self.assertTrue(self.pet.id, "1")

    def test_if_animal_is_created_with_all_fields(self):
        """test if name of pet is well configured"""
        self.assertEquals(self.pet.name, "Yuki")
        self.assertEquals(type(self.pet.name), str)
        self.assertEquals(self.pet.owner.username, "jonny")

    def test_if_animal_owner_is_same_as_username_of_user(self):
        """test if the name of the user who created
        the pet is the same than the username"""
        self.assertTrue(self.pet.owner, self.user.username)
        self.assertEquals(self.pet.owner.username, "jonny")

    def test_if_specie_of_animal_is_the_correct_specie(self):
        """test if the specie is correct according
        to the specie name we gave to the pet"""
        self.assertTrue(self.pet.specie, self.specie.name)

    def test_if_pet_age_is_an_integer(self):
        """test if pet age is correct and integer"""
        self.assertTrue(self.pet.age, "3")

    def test_if_pet_weight_is_float(self):
        """test if pet weight is correct and float"""
        self.assertTrue(self.pet.weight, "3.5")
        self.assertTrue(type(self.pet.weight), float)

from django.test import TestCase

from healthbook.models import HealthBook, Medication
from animals.models import Pet, Specie
from schedules.models import TimeOfDay
from users.models import User, Role


class TestHealthBookandMedicationModels(TestCase):

    def setUp(self):
        self.role = Role.objects.create(name="owner")
        self.user = User.objects.create(
            username="jonny",
            role=self.role,
            email="j@mail.com",
            location="Boulogne-Billancourt",
            avatar="avatar_profile.jpg")

        self.specie = Specie.objects.create(name="cat")

        self.pet = Pet.objects.create(
            owner=self.user,
            specie=self.specie,
            name="Yuki",
            age=3,
            weight=3.5,)

        self.tod = TimeOfDay.objects.create(time="Afternoon")

        self.healthbook = HealthBook.objects.create(
            pet=self.pet,
            vaccine="YES",
            sterilize="YES",
            last_vaccine="2020-10-12",
            next_vaccine="2021-11-12",
            veterinary_name="Docteur Euzenat",
            veterinary_phone="08972348923"
        )

        self.medication = Medication.objects.create(
            pet=self.pet,
            med_name="Ventoline",
            med_start="2020-10-20",
            med_end="2020-12-20",
            time=self.tod,
            dosage="7 inhales"
        )

    def test_if_fields_of_healthbooks_are_correct(self):
        self.assertEquals(self.healthbook.pet, self.pet)
        self.assertEquals(self.healthbook.vaccine, "YES")
        self.assertEquals(self.healthbook.veterinary_name, "Docteur Euzenat")
        self.assertEquals(self.healthbook.veterinary_phone, "08972348923")

    def test_if_medication_fields_are_correct(self):
        self.assertEquals(self.medication.pet, self.pet)
        self.assertEquals(self.medication.time, self.tod)
        self.assertEquals(self.medication.dosage, "7 inhales")

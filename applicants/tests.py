from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Applicant, Application, EducationProgram
import datetime

class ApplicantModelTest(TestCase):
    def setUp(self):
        self.applicant = Applicant.objects.create(
            full_name="Иванов Иван Иванович",
            birth_date="2000-01-01",
            gender="M",
            phone="+79991234567",
            email="ivan@example.com",
            address="г. Москва"
        )

    def test_str_method(self):
        self.assertEqual(str(self.applicant), "Иванов Иван Иванович")

class EducationProgramModelTest(TestCase):
    def setUp(self):
        self.program = EducationProgram.objects.create(
            name="Программная инженерия",
            code="09.03.04",
            level="bachelor",
            description="Подготовка специалистов в области разработки ПО.",
            duration=4,
            budget_places=15,
            paid_places=10,
            tuition_fee=120000.00
        )

    def test_str_method(self):
        self.assertEqual(str(self.program), "09.03.04 - Программная инженерия")

class ApplicationModelTest(TestCase):
    def setUp(self):
        self.applicant = Applicant.objects.create(
            full_name="Петров Петр Петрович",
            birth_date="2002-03-15",
            gender="M",
            phone="+79998887766",
            email="petr@example.com",
            address="г. Санкт-Петербург"
        )
        self.program = EducationProgram.objects.create(
            name="Информатика и вычислительная техника",
            code="09.03.01",
            level="bachelor",
            description="Программа подготовки в области ИТ.",
            duration=4,
            budget_places=10,
            paid_places=5
        )
        self.application = Application.objects.create(
            applicant=self.applicant,
            program=self.program,
            status="new",
            exam_results={"Математика": 80, "Информатика": 90}
        )

    def test_application_creation(self):
        self.assertEqual(self.application.status, "new")
        self.assertEqual(self.application.exam_results["Математика"], 80)
        self.assertEqual(str(self.application), f"Заявление #{self.application.id} - {self.applicant}")

class ApplicantViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="admin", password="adminpass")
        self.client.login(username="admin", password="adminpass")

        self.applicant = Applicant.objects.create(
            full_name="Сергеев Сергей Сергеевич",
            birth_date="2001-06-15",
            gender="M",
            phone="+79990001122",
            email="sergey@example.com",
            address="г. Казань"
        )

    def test_applicant_list_view(self):
        response = self.client.get(reverse("applicants:applicant_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.applicant.full_name)

    def test_applicant_create_view(self):
        response = self.client.post(reverse("applicants:applicant_create"), {
            "full_name": "Анна Ананьева Алексеевна",
            "birth_date": "2003-05-01",
            "gender": "F",
            "phone": "+79001112233",
            "email": "anna@example.com",
            "address": "г. Новосибирск"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Applicant.objects.count(), 2)

    def test_applicant_update_view(self):
        response = self.client.post(reverse("applicants:applicant_update", args=[self.applicant.id]), {
            "full_name": "Сергеев С. С.",
            "birth_date": "2001-06-15",
            "gender": "M",
            "phone": "+79990001122",
            "email": "sergey@example.com",
            "address": "г. Казань"
        })
        self.assertEqual(response.status_code, 302)
        self.applicant.refresh_from_db()
        self.assertEqual(self.applicant.full_name, "Сергеев С. С.")

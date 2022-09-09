from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data = {
            "username":"Parvoz",
            "first_name": "Parvoz",
            "last_name": "Eshkuvvatov",
            "email":"parvozdev@mail.ru",
            "password": "somepassword"
        }
    )

        user = User.objects.get(username = 'Parvoz')

        self.assertEqual(user.first_name, "Parvoz")
        self.assertEqual(user.last_name, "Eshkuvvatov")
        self.assertEqual(user.email, "parvozdev@mail.ru")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Parvoz",
                "email": "parvozdev@mail.ru"
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Parvoz",
                "first_name": "Parvoz",
                "last_name": "Eshkuvvatov",
                "email":"invalid-email",
                "password": "somepassword"
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        # 1.create a user
        user = User.objects.create(username = 'Parvoz', first_name = 'Parvoz')
        user.set_password('somepassword')
        user.save()

        # 2. try to create another user with that same username
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Parvoz",
                "first_name": "Parvoz",
                "last_name": "Eshkuvvatov",
                "email": "invalid-email",
                "password": "somepassword"
            }
        )

        # 3.check that the second user was not created
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

        # 4. check that the form contains the error message
        self.assertFormError(response, "form", "username", "A user with that username already exists.")

class LoginTestCase(TestCase):
    def test_successfull_login(self):
        db_user = User.objects.create(username='Parvoz', first_name='Parvoz')
        db_user.set_password('somepassword')
        db_user.save()

        self.client.post(
            reverse("users:login"),
                    data = {
                        "username": "Parvoz",
                        "password": "somepassword"
                    }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        db_user = User.objects.create(username='Parvoz', first_name='Parvoz')
        db_user.set_password('somepassword')
        db_user.save()

        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "Parvoz",
                "password": "wrong-somepassword"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)






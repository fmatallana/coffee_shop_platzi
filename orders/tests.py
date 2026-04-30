from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class MyorderViewTest(TestCase):
    def test_no_loged_used_should_redirect(self):
        url = reverse("my_order")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/usuarios/login/?next=/pedidos/mi-orden")

    def test_loged_used_should_redirect(self):
        url = reverse("my_order")
        user = get_user_model().objects.create(username="test")
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

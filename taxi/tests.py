from enum import unique

from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver
from taxi.forms import DriverLicenseUpdateForm


class FormTest(TestCase):
    def test_license_number_validation(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"license_number": "ABCD2345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"],
        )


class SearchTest(TestCase):
    def test_driver_search_by_username(self):
        Driver.objects.create_user(
            username="test1",
            password="racer2242",
            license_number="ABC12345",
        )
        Driver.objects.create_user(
            username="test2",
            password="racer4424",
            license_number="CBA12345",
        )
        self.client.login(username="test1", password="racer2242")
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "unique"})
        self.assertContains(response, "test1")
        self.assertNotContains(response, "test2")


class AccessTest(TestCase):
    def test_car_list_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("/accounts/login/", response.url)

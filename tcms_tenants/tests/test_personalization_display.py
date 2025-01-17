# Copyright (c) 2022 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPL 3.0: https://www.gnu.org/licenses/gpl-3.0.txt
# pylint: disable=too-many-ancestors

from django.urls import reverse
from django_tenants.utils import schema_context

from tcms_tenants.tests import LoggedInTestCase


class WhenOrganizationValueIsSet(LoggedInTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with schema_context('public'):
            cls.tenant.organization = "Demo Instance"
            cls.tenant.name = "demonstration"
            cls.tenant.save()

    def test_display(self):
        response = self.client.get(reverse('tcms-login'))

        self.assertContains(response, 'alt="Demo Instance"')
        self.assertNotContains(response, 'alt="demonstration"')
        self.assertNotContains(response, self.tenant.schema_name)


class WhenNameValueIsSetAndOrganizationValueIsNotSet(LoggedInTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with schema_context('public'):
            cls.tenant.organization = ""
            cls.tenant.name = "demonstration"
            cls.tenant.save()

    def test_display(self):
        response = self.client.get(reverse('tcms-login'))

        self.assertNotContains(response, 'alt="Demo Instance"')
        self.assertContains(response, 'alt="demonstration"')
        self.assertNotContains(response, self.tenant.schema_name)


class WhenNameAndOrganizationValuesAreNotSet(LoggedInTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with schema_context('public'):
            cls.tenant.organization = ""
            cls.tenant.name = ""
            cls.tenant.save()

    def test_display(self):
        response = self.client.get(reverse('tcms-login'))

        self.assertNotContains(response, 'alt="Demo Instance"')
        self.assertNotContains(response, 'alt="demonstration"')
        self.assertContains(response, self.tenant.schema_name)

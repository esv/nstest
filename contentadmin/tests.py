"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from contentadmin.models import Content

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class ContentGetAllVrContract(TestCase):
    def test_basic_addition(self):
        Content.objects.all()[0].vr_contract_id_set.all()
        self.assertEqual(1 + 1, 2)
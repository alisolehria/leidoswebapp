from django.db import models
from unittest import TestCase
from models import profile

class TestProfile(TestCase):
    def test_discr(self):
        p = profile()
        self.assertRaises(Exception, p.Meta, models.Model)

    def test_demo(self):
        self.fail()
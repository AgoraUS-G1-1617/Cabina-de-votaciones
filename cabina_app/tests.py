"""
This file demonstrates writing tests using the unittest module and py.test.
Replace this with more appropriate tests for your application.
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cabina_agora_us.settings")
#from django.test import TestCase
import unittest
from services import json_as_poll, get_poll
#from cabina_app.dbConnect import *
#from cabina_app.models import *




class BasicTests(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2. For correct configuration assertion
        """
        self.assertEqual(1 + 1,2)

    def test_poll(self):
        expectedId = 1
        """
        Test that the Poll is correctly recieved from 'Recuento y Modificacion'
        """
        poll = get_poll(expectedId)
        self.assertEqual(poll.id, expectedId)

    def test_negative_poll(self):
        """
        Test that an incorret Id raises an Exception of kind KeyError
        """
        with self.assertRaises(KeyError):
            poll = get_poll(6546546)
            self.assertIsNone(poll.id)

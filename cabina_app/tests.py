"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

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
        """
        Test that the Poll is correctly recieved from 'Recuento y Modificacion'
        """
        poll = get_poll(1)
        self.assertEqual(poll.id, 1)






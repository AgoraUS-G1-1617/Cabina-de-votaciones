"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cabina_agora_us.settings")
#from django.test import TestCase
import unittest
#from cabina_app.dbConnect import *
#from cabina_app.models import *




class BasicTests(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2. For correct configuration assertion
        """
        self.assertEqual(1 + 1, 2)

    #def vote_basic_test(self):
    #    """
    #    Test basic creation of a Vote
    #    """
    #    VoteIdentifier = 26
    #    poll = get_Poll(VoteIdentifier)
    #    polls = Poll.objects.all()
    #    self.assertTrue(polls.contains(poll) )

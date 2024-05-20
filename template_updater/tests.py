from django.test import TestCase
from .models import *

# Create your tests here.
class ActionTest(TestCase):
    def test_action_creation(self):
        # Valid Action creation
        action = Action.objects.create(subject="Action test", description="1234567890123", actions_and_solutions="is it working?")
        self.assertTrue(action.id)  # Assert action
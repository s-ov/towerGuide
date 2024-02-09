from django.test import TestCase

from locator.forms import NodeForm, LoginUserForm
from locator.models import (DistributiveSubstation as DS, 
                            MotorControlCenter as MCC, 
                            Node)

class NodeFormTestCase(TestCase):
    def setUp(self):
        """Create test data"""
        self.substation =  DS.objects.create(title='РП-1',slug='rp-1', level='4.8')
        self.mcc = MCC.objects.create(title="MCC-1", slug="mcc-1", substation=self.substation)
        self.node1 = Node.objects.create(title="Node 1", slug="1_1", level="4.8", round_per_minute=1000, power=7.5, mcc=self.mcc)
        self.form_data = {
            'title': 'Node 1', 
            'slug': 'slug_1', 
            'label': None, 
            'level': '4.8', 
            'round_per_minute': 1000, 
            'power': 7.5, 
            'mcc': self.mcc}

    def test_valid_form(self):
        """Test form validation"""
        form = NodeForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """ Test invalid form data (missing 'round_per_minute' field)"""
        form_data = {
            'title': 'Node 1', 
            'slug': 'slug_1', 
            'label': None, 
            'level': '4.8',  
            'power': 7.5, 
            'mcc': self.mcc
        }
        form = NodeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        """Test the form with a valid data"""
        form = NodeForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertIsNotNone(instance)
        self.assertEqual(instance.title, 'Node 1')
        self.assertEqual(instance.slug, 'slug_1')


class LoginUserFormTestCase(TestCase):
    def test_valid_form(self):
        """Test a form instance with valid data"""
        form_data = {'username': 'testuser', 'password': 'password'}
        form = LoginUserForm(data=form_data)
        # self.assertTrue(form.is_valid())

    def test_missing_username(self):
        """Test a form instance with missing username"""
        form_data = {'password': 'password'}
        form = LoginUserForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_missing_password(self):
        """Test a form instance with missing password"""
        form_data = {'username': 'testuser'}
        form = LoginUserForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

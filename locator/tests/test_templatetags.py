from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.contrib.auth.models import User
from locator.models import DistributiveSubstation as DS
from locator.templatetags.locator_tags import show_substations

class TemplateTagsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create some test data"""
        DS.objects.create(title='Substation 1', slug='substation-1')
        DS.objects.create(title='Substation 2', slug='substation-2')

    def test_show_substations_tag(self):
        """Test if the rendered content is a dictionary containing the expected queryset"""
        rendered = show_substations()

        self.assertIsInstance(rendered, dict)
        self.assertIn('rooms', rendered)
        self.assertEqual(list(rendered['rooms']), list(DS.objects.all()))

    def test_template_rendering(self):
        """Test if the rendered template contains the expected content"""
        template_to_render = Template("{% load locator_tags %}{% show_substations %}")
        rendered_template = template_to_render.render(Context())        
        self.assertIn('Substation 1', rendered_template)
        self.assertIn('Substation 2', rendered_template)

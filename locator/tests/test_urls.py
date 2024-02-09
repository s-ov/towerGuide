from django.test import TestCase
from django.test import SimpleTestCase, Client
from django.urls import reverse, resolve

from locator import views, models


class TestUrls(TestCase):

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, views.HomeView)

    def test_substation_view_with_sub_num(self):
        url = reverse('substation', kwargs={'sub_num': 1})
        self.assertEqual(resolve(url).func.view_class, views.SubstationView)

    def test_mcc_view_with_mcc_slug(self):
        url = reverse('mcc', kwargs={'mcc_slug': '1'})
        self.assertEqual(resolve(url).func.view_class, views.MCCView)

    def test_node_view_with_slug(self):
        url = reverse('node-detail', kwargs={'slug': '1'})
        self.assertEqual(resolve(url).func.view_class, views.NodeView)

    def test_add_node_view_with_slug(self):
        url = reverse('add_node')
        self.assertEqual(resolve(url).func.view_class, views.AddNodeView)

    def test_edit_node_view_with_slug(self):
        url = reverse('edit_node', kwargs={'slug': '1'})
        self.assertEqual(resolve(url).func.view_class, views.UpdateNodeView)

    def test_search_node_view_with_slug(self):
        url = reverse('search_node')
        self.assertEqual(resolve(url).func.view_class, views.SearchNodeView)

    def test_node_delete_view_with_slug(self):
        url = reverse('node_delete', kwargs={'slug': '1'})
        self.assertEqual(resolve(url).func.view_class, views.NodeDeleteView)

    def test_node_delete_confirm_view(self):
        url = reverse('node_delete_confirm')
        self.assertEqual(resolve(url).func.view_class, views.NodeDeleteConfirmView)

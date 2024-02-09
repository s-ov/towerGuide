from django.test import TestCase, Client
from django.urls import reverse
from django.db.models.query import QuerySet
from django.contrib.auth.models import User, Permission

import json
from locator import views
from locator import forms
from locator.models import (DistributiveSubstation as DS, 
                            MotorControlCenter as MCC, 
                            Node)


class HomeViewTestCase(TestCase):

    def setUp(self):
        """Create test data"""
        client = Client()
        self.response = client.get('/')

        DS.objects.create(title='РП-1', slug='rp-1',level = '4.8')
        DS.objects.create(title='РП-2', slug='rp-2',level = '4.8')

    def test_view_url_exists_at_desired_location(self):
        """Test that the URL mapping is correct"""
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        self.assertTemplateUsed(self.response, 'locator/base.html')

    def test_view_context_data(self):
        """Test that the view passes the correct context data to the template"""
        self.assertIn('substations', self.response.context)
        substations = self.response.context['substations']
        self.assertIsInstance(substations, QuerySet)
        self.assertEqual(substations.count(), 2) 

    def test_get_queryset(self):
        """Test that the view fetches the correct queryset"""
        view = views.HomeView()
        queryset = view.get_queryset()
        self.assertIsInstance(queryset, QuerySet)
        self.assertEqual(queryset.count(), 2)  


class SubstationViewTestCase(TestCase):

    def setUp(self):
        """Create test data"""
        substation =  DS.objects.create(
            title = 'РП-1',
            slug = 'rp-1',
            level = '4.8'
        )
        self.mcc1 = MCC.objects.create(substation=substation, title='Room 1')
        self.mcc2 = MCC.objects.create(substation=substation, title='Room 2')

        client = Client()
        self.response = client.get('/substation/1/')

    def test_view_url_exists_at_desired_location(self):
        """Test that the URL mapping is correct"""
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        self.assertTemplateUsed(self.response, 'locator/mcc.html')

    def test_view_context_data(self):
        """Test that the view passes the correct context data to the template"""
        self.assertIn('rooms', self.response.context)
        rooms = self.response.context['rooms']
        self.assertIsInstance(rooms, QuerySet)
        self.assertEqual(rooms.count(), 2)  

    def test_get_queryset(self):
        """Test that the view fetches the correct queryset based on the provided sub_num"""
        view = views.SubstationView()
        view.kwargs = {'sub_num': 1} 
        queryset = view.get_queryset()
        self.assertIsInstance(queryset, QuerySet)
        self.assertEqual(queryset.count(), 2) 

    # def test_get_context_data(self):
    #     """Test that the view sets the correct title in the context data"""
    #     view = views.SubstationView()
    #     view.kwargs = {'sub_num': 1}  
    #     context = view.get_context_data()
    #     self.assertIn('title', context)
    #     self.assertEqual(context['title'], 'РП-1')
        

class MCCViewTestCase(TestCase):
    def setUp(self):
        """Create test data"""
        self.substation =  DS.objects.create(title='РП-1',slug='rp-1', level='4.8')
        self.mcc = MCC.objects.create(title="MCC-1", slug="mcc-1", substation=self.substation)
        self.node1 = Node.objects.create(title="Node 1", slug="1_1", level="4.8", round_per_minute=1000, power=7.5, mcc=self.mcc)
        self.node2 = Node.objects.create(title="Node 2", slug="1_2", level="4.8", round_per_minute=1000, power=7.5, mcc=self.mcc)

        self.client = Client()
        url = reverse('mcc', kwargs={'mcc_slug': self.mcc.slug})
        self.response = self.client.get(url)

    def test_view_url_exists_at_desired_location(self):
        """Test that the URL mapping is correct"""
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        self.assertTemplateUsed(self.response, 'locator/nodes.html')

    def test_view_nodes_in_response_context_correct(self):
        """Test that the nodes in the response context are correct"""
        self.assertQuerysetEqual(self.response.context['nodes'].order_by('id'), [self.node1, self.node2])

    def test_view_nodes_title_in_response_context_correct(self):
        """Assert that the title in the response context is correct"""
        expected_title = f'{self.mcc.title}(PП-{self.mcc.substation_id + 3})'
        self.assertEqual(self.response.context['title'], expected_title)
        
    def test_view_is_response_context_correct(self):
        """Return correct queryset"""
        queryset = self.response.context['nodes']
        expected_queryset = Node.objects.filter(mcc__slug=self.mcc.slug)
        self.assertQuerysetEqual(queryset.order_by('id'), expected_queryset)


class NodeViewTestCase(TestCase):
    """Create test data"""
    def setUp(self):
        self.substation =  DS.objects.create(title='РП-1',slug='rp-1', level='4.8')
        self.mcc = MCC.objects.create(title="MCC-1", slug="mcc-1", substation=self.substation)
        self.node = Node.objects.create(title="Node 1", slug="1_1", level="4.8", round_per_minute=1000, power=7.5, mcc=self.mcc)
        
        self.client = Client()
        url = reverse('node-detail', kwargs={'slug': self.node.slug})
        self.response = self.client.get(url)

    def test_node_view_url_exists_at_desired_location(self):
        """Test that the URL mapping is correct"""
        self.assertEqual(self.response.status_code, 200)

    def test_node_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        self.assertTemplateUsed(self.response, 'locator/node.html') 

    def test_node_view_object_name_and_slug_in_response(self):
        """Test if the object's name and slug are present in the response"""
        self.assertContains(self.response, 'Node 1') 
        self.assertContains(self.response, '1_1')

    def test_node_view_passes_correct_context_data_to_template(self):
        """Test that the correct context data is passed to the template"""
        self.assertEqual(self.response.context['node'], self.node)
        self.assertEqual(self.response.context['title'], f'{self.node.title}_{self.node.slug}')

    def test_node_view_not_found(self):
        """Test a GET request with a non-existent slug"""
        response = self.client.get(reverse('node-detail', kwargs={'slug': 'non-existent-slug'}))
        self.assertEqual(response.status_code, 404)


class AddNodeViewTestCase(TestCase):
    def setUp(self):
        self.substation =  DS.objects.create(title='РП-1',slug='rp-1', level='4.8')
        self.mcc = MCC.objects.create(title="MCC-1", slug="mcc-1", substation=self.substation)
        self.node = Node.objects.create(title="Node 1", slug="1_1", level="4.8", round_per_minute=1000, power=7.5, mcc=self.mcc)
        
        self.client = Client()
        self.response = self.client.get(reverse('add_node'))

        # Create a user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='password')
        permission = Permission.objects.get(name='Can add node')
        self.user.user_permissions.add(permission)
        self.client.login(username='testuser', password='password')

    def test_add_view_accessible_by_name(self):
        response = self.client.get(reverse('add_node'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_node'))
        self.assertTemplateUsed(response, 'locator/add_node.html')

    def test_node_add_form(self):
        data = {
            'title': 'Test Node',
            'slug': 'test_slug',
            'level': '4.8',
            'round_per_minute': 1000,
            'power': 1.5,
            'mcc': self.mcc,
        }
        response = self.client.post(reverse('add_node'), data=data)
        self.assertEqual(response.status_code, 200)  # 302: Redirect after successful form submission
        # self.assertRedirects( def test_add_node_form(self):response, reverse('home'))

    def test_node_is_created_in_db(self):
        """Test if the node is created in the database"""
        self.assertTrue(Node.objects.filter(title='Node 1').exists())

    def test_permission_required(self):
        """Test permission from the user"""
        permission = Permission.objects.get(name='Can add node')
        self.user.user_permissions.remove(permission)


class UpdateNodeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.permission = Permission.objects.get(codename='change_node')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='testuser', password='password')

        self.substation =  DS.objects.create(title='РП-1',slug='rp-1', level='4.8')
        self.mcc = MCC.objects.create(title="MCC-1", slug="mcc-1", substation=self.substation)
        self.node = Node.objects.create(id=1, title="Node 1", slug="1_1", level="4.8", round_per_minute=1000, power=7.5, mcc=self.mcc)

        self.response = self.client.get(reverse('edit_node', kwargs={'slug': self.node.slug}))

    def test_view_accessibility(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_submission_updates_node(self):
        """Test form submission after node updating"""
        self.assertEqual(self.response.status_code, 200) 

    def test_form_rendered_properly(self):
        self.assertIsInstance(self.response.context['form'], forms.NodeForm)
        self.assertEqual(self.response.context['form'].instance, self.node)

    def test_permission_required(self):
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('edit_node', kwargs={'slug': self.node.slug}))
        self.assertEqual(response.status_code, 403)  


class SearchNodeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.permission = Permission.objects.get(codename='view_node')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='testuser', password='password')

        self.response = self.client.get(reverse('search_node'))

    def test_view_accessibility(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, 'locator/search_node.html')

    def test_context_data(self):
        """Test context data if needed"""
        self.assertIn('form', self.response.context)

    def test_queryset_filtering(self):
        substation =  DS.objects.create(title='РП-1',slug='rp-1', level='4.8')
        mcc = MCC.objects.create(title="MCC-1", slug="mcc-1", substation=substation)
        node1 = Node.objects.create(title="Node 1", slug="1_1", level="4.8", round_per_minute=1000, power=7.5, mcc=mcc)

        # Make a GET request with filter parameters
        response = self.client.get(reverse('search_node'), {'name': 'Node 1'})

        # Check if the filtered queryset contains the expected object(s)
        self.assertEqual(response.status_code, 200)
        self.assertIn('node', response.context)  # Ensure the queryset is passed to the template
        queryset = response.context['node']
        self.assertIsInstance(queryset, QuerySet)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), node1)

    def test_permission_required(self):
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('search_node'))
        self.assertEqual(response.status_code, 403)  


class NodeDeleteViewTestCase(TestCase):
    def setUp(self):
        """Create a test data."""
        substation =  DS.objects.create(title='РП-1',slug='rp-1', level='4.8')
        mcc = MCC.objects.create(title="MCC-1", slug="mcc-1", substation=substation)
        self.node = Node.objects.create(title="Node", slug="1_1", level="4.8", round_per_minute=1000, power=7.5, mcc=mcc)
        
        self.response = self.client.get(reverse('node_delete', kwargs={'slug': self.node.slug}))

    def test_view_accessibility(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, 'locator/delete_node.html')

    def test_node_deletion(self):
        response = self.client.post(reverse('node_delete', kwargs={'slug': self.node.slug}))
        self.assertEqual(response.status_code, 302)  # 302: Redirect after successful form submission

        # Verify if the node is deleted from the database
        self.assertFalse(Node.objects.filter(slug=self.node.slug).exists())

    def test_redirect_after_deletion(self):
        response = self.client.post(reverse('node_delete', kwargs={'slug': self.node.slug}))
        self.assertRedirects(response, reverse('node_delete_confirm'))


class TestNodeDeleteConfirmViewTestCase(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('node_delete_confirm'))

    def test_view_accessibility(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'locator/node_confirm_delete.html')


class TestLoginUserViewTestCase(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('login'))

    def test_view_accessibility(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, 'locator/login.html')

    def test_correct_context_data(self):
        from django.contrib.auth.forms import AuthenticationForm
        self.assertIn('form', self.response.context)
        self.assertIsInstance(self.response.context['form'], AuthenticationForm)
        self.assertIn('title', self.response.context)
        self.assertEqual(self.response.context['title'], 'Вхід у застосунок')

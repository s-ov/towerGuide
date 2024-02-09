from django.test import TestCase, Client
from django.urls import reverse, resolve

from locator import models



class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.station = models.DistributiveSubstation(
            title='Station 1',
            slug='station1',
            level='4.5'
        )
        self.station.save()

        self.mcc_1 = models.MotorControlCenter.objects.create(
            title='MCC 1',
            substation=self.station,
        )
        self.mcc_1.save()

        self.node = models.Node(
            title='Node1',
            slug='node_1',
            level='4.5',
            round_per_minute=100,
            power=5.0,
            mcc=self.mcc_1
        )

    def test_station_str_representation(self):
        self.assertEqual(str(self.station), 'Station 1')

    def test_station_get_absolute_url(self):
        url = self.station.get_absolute_url()
        expected_url = reverse('substation', kwargs={'sub_num': self.station.pk})
        self.assertEqual(url, expected_url)

    def test_mcc_slug_creation(self):   
        self.assertEqual(self.mcc_1.slug, 'mcc-1')

    def test_mcc_str_representation(self):
        self.assertEqual(str(self.mcc_1), 'MCC 1')

    def test_mcc_get_absolute_url(self):
        url = self.mcc_1.get_absolute_url()
        expected_url = reverse('mcc', kwargs={'mcc_slug': self.mcc_1.slug})
        self.assertEqual(url, expected_url)

    def test_node_str_representation(self):
        self.assertEqual(str(self.node), 'Node1_node_1')

    def test_node_get_absolute_url(self):
        url = self.node.get_absolute_url()
        expected_url = reverse('node-detail', args=(self.node.slug,))
        self.assertEqual(url, expected_url)
    
from urllib.parse import urlencode

from django.test import TestCase

from autoria.serializers import MonitorQuerySerializer


class MonitorQuerySerializerTestCase(TestCase):

    def setUp(self):
        self.test_post_data = {
            'category_id': 0,
            'marka_id': 0,
            'model_id': 0,
            'gearbox': 0,
            'bodystyle': 0
        }
        self.test_api_data = {
            'category_id[0]': 0,
            'marka_id[0]': 0,
            'model_id[0]': 0,
            'gearbox[0]': 0,
            'bodystyle[0]': 0
        }

    def test_create_api_url(self):
        serializer = MonitorQuerySerializer(data=self.test_post_data)
        if serializer.is_valid():
            url = serializer._create_api_urls(key='key')
            test_query = urlencode(self.test_api_data)
            self.assertEqual(
                url, f'https://developers.ria.com/auto/search?api_key=key&{test_query}')

    def test_create_url_without_fields(self):
        self.test_post_data['bodystyle'] = None
        self.test_api_data['bodystyle'] = None
        serializer = MonitorQuerySerializer(data=self.test_post_data)
        if serializer.is_valid():
            url = serializer._create_api_urls(key='key')
            test_query = urlencode(self.test_api_data)
            self.assertEqual(
                url, f'https://developers.ria.com/auto/search?api_key=key&{test_query}')

    def test_empty_api_response(self):
        pass

    def test_limited_api_response(self):
        pass

    def test_monitoring_limit_per_user(self):
        pass

    def test_new_monitoring_fields(self):
        pass

# standard library
# import json

# third-party
from rest_framework.test import APIClient

# Django
from django.test import TestCase

# local Django
from apps.collection.models import Collection
from apps.collection.serializers import CollectionHeavySerializer
from apps.tests.auth import create_user
from apps.tests.db import DBpopulate

class CRUDTest(TestCase):

  def setUp(self):
    # user an token
    auth = create_user(True)
    self.client = APIClient()
    self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + auth['token'].key)
    # data
    DBpopulate(theme= 1, category= 1, collection= 1)

  def test_create_collection(self):
    data = {
      'name': 'YSON',
      'description': '---',
      'updated': '2019-09-19 10:00:00',
      'theme_id': 1,
    }
    response = self.client.post('/api/collections/', data)
    # print(response)
    serializer = CollectionHeavySerializer(
      Collection.objects.get(id = response.data['id']),
    )
    self.assertEqual(response.status_code, 201)
    self.assertEqual(serializer.data, response.data)

  def test_create_error_params(self):
    data = {
      'name': 'YSON',
      'description': '---',
      'updated': '2019-09-19',
    }
    response = self.client.post('/api/collections/', data)
    self.assertEqual(response.status_code, 400)

  def test_create_error_duplicate(self):
    data = {
      'name': 'TEST',
      'description': '---',
      'updated': '2019-09-19',
    }
    response = self.client.post('/api/collections/', data)
    self.assertEqual(response.status_code, 400)
  
  def test_get_collection(self):
    response  = self.client.get('/api/collection/' + str(1) + '/')
    serializer = CollectionHeavySerializer(
      Collection.objects.get(id= response.data['id'])
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(serializer.data, response.data)
  
  def test_update_collection(self):
    collection = Collection.objects.get(id= 1)
    oldvalues = CollectionHeavySerializer(collection)
    newdata = {
      'name': 'YSON2',
      'description': 'updated',
      'theme_id': 1,
    }
    response = self.client.put('/api/collection/' + str(1) + '/', newdata)
    # print(response.data)
    newvalues = CollectionHeavySerializer(
      Collection.objects.get(id= 1)
    )
    self.assertEqual(response.status_code, 200)
    self.assertNotEqual(newvalues.data, oldvalues.data)
    self.assertEqual(newvalues.data, response.data)

  def test_delete_collection(self):
    response = self.client.delete('/api/collection/' + str(1) + '/')
    self.assertEqual(response.status_code, 204)
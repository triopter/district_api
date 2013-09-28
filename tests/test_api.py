import requests
import json
from unittest import TestCase
from mock import patch, Mock

from district_api.api import DistrictApi, District, DistrictApiError, \
    ApiUnavailable, LocationUnavailable, AuthorizationError, QuotaExceeded, \
    BadRequest, InvalidResponse

class ApiTestCase(TestCase):
    api_key = 'dummy'
    url = 'http://api.nytimes.com/svc/politics/v2/districts.json'
    err_response_dict = { 
        "errors": [
            { "error": "Record not found", }, 
        ],
        "copyright": "Copyright (c) 2013 The New York Times Company. All Rights "
            "Reserved.",
        "status":"ERROR",
    }
    success_response_dict = {
        "results": [
            {
                "district": "07",
                "level": "Community District",
                "kml_url": "http://graphics8.nytimes.com/packages/xml/represent/167.xml"
            },
            {
                "district": "Upper West Side",
                "level": "Neighborhood",
                "kml_url": None,
            },
            {
                "district": "31",
                "level": "State Senate",
                "kml_url": "http://graphics8.nytimes.com/packages/xml/represent/1396.xml"
            },
        ],
        "copyright": "Copyright (c) 2013 The New York Times Company. All Rights Reserved.",
        "num_results": 7,
        "status": "OK"
    }
    success_data = {
        'Community District': District('07', 'Community District', 
            'http://graphics8.nytimes.com/packages/xml/represent/167.xml'),
        'Neighborhood': District('Upper West Side', 'Neighborhood', None),
        'State Senate': District('31', 'State Senate', 'http://graphics8.nytimes.com/packages/xml/represent/1396.xml'),
    }
    success_response_str = """
    {
          "results": [
            {
              "district": "07",
              "level": "Community District",
              "kml_url": "http:\/\/graphics8.nytimes.com\/packages\/xml\/represent\/167.xml"
            },
            {
              "district": "Upper West Side",
              "level": "Neighborhood",
              "kml_url": null
            },
            {
              "district": "31",
              "level": "State Senate",
              "kml_url": "http:\/\/graphics8.nytimes.com\/packages\/xml\/represent\/1396.xml"
            }
          ],
          "copyright": "Copyright (c) 2013 The New York Times Company. All Rights Reserved.",
          "num_results": 7,
          "status": "OK"
        }
    """

    def setUp(self):
        self.client = DistrictApi(self.api_key)
        
    def test_construction(self):
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.url, self.url)

        other_client = DistrictApi(self.api_key, url='http://www.example.com')
        self.assertEqual(other_client.url, 'http://www.example.com')

    def test_validation(self):
        mock_get_data = Mock()
        mock_get_data.return_value = {}
        mock_construct = Mock()
        mock_construct.return_value = {}
        
        with patch.multiple(self.client, get_data=mock_get_data, 
            construct_single_location_data=mock_construct):

            with self.assertRaises(TypeError):
                self.client.get_districts(12.3456, 10.432)
            
            with self.assertRaises(ValueError):
                self.client.get_districts(('a', 10.432))
            
            with self.assertRaises(ValueError):
                self.client.get_districts((10.432, 'a'))
            
            try:
                self.client.get_districts((12.3456, 10.432))
                self.client.get_districts((12.3456, -10.432))
                self.client.get_districts((12, 10))
                self.client.get_districts((12, -10))
                self.client.get_districts(('12.3456', '10.432'))
                self.client.get_districts(('12.3456', '-10.432'))
                self.client.get_districts(('12', '10'))
                self.client.get_districts(('12', '-10'))
            except (TypeError, ValueError):
                self.fail('get_districts should accept float, int, and strings that '
                    'can be converted to floats/ints')
                
    def test_construct_query_vars(self):
        qv = self.client.construct_query_vars(lat_lng=(12.3456, -10.432))
        self.assertEqual(qv, {
                'lat': 12.3456,
                'lng': -10.432, 
                'api-key': self.api_key,
            })
    
    @patch('requests.get')
    def test_send_request(self, get):
        self.client.send_request(lat_lng=(12.3456, -10.432))
        self.assertTrue(get.called)
        get.assert_called_with(self.url, params={
                'lat': 12.3456,
                'lng': -10.432, 
                'api-key': self.api_key,
            })
            
        self.client.send_request()
        self.assertTrue(get.called)
        get.assert_called_with(self.url, params={
                'api-key': self.api_key,
            })
            
    def test_validate_status(self):
        with self.assertRaises(ApiUnavailable):
            mock_resp = Mock(None)
            mock_resp.status_code = 404
            self.client.validate_response(mock_resp)
            
        with self.assertRaises(ApiUnavailable):
            mock_resp = Mock(None)
            mock_resp.status_code = 500
            self.client.validate_response(mock_resp)
            
        with self.assertRaises(BadRequest):
            mock_resp = Mock(None)
            mock_resp.status_code = 400
            self.client.validate_response(mock_resp)
            
        with self.assertRaises(AuthorizationError):
            mock_resp = Mock(None)
            mock_resp.status_code = 403
            self.client.validate_response(mock_resp)
            
        with self.assertRaises(DistrictApiError):
            mock_resp = Mock(None)
            mock_resp.status_code = 406
            self.client.validate_response(mock_resp)
            
        # Make sure it doesn't raise on 200:
        try:
            mock_resp = Mock(None)
            mock_resp.status_code = 200
            self.client.validate_response(mock_resp)
        except:
            self.fail('validate_response should not raise any errors for a 200 '
                'status code')
            
    def test_validate_body(self): 
        with self.assertRaises(LocationUnavailable):
            self.client.validate_response_body({ 'status': 'ERROR' })
            
        with self.assertRaises(InvalidResponse):
            self.client.validate_response_body({ 'a': 'ERROR' })       
            
    def test_construct_single_location(self):
        # success case
        districts = self.client.construct_single_location_data(
            self.success_response_dict)
        
        self.assertEqual(districts, self.success_data)
        
        with self.assertRaises(InvalidResponse):
            self.client.construct_single_location_data(self.err_response_dict)
        
        with self.assertRaises(InvalidResponse):
            self.client.construct_single_location_data({
                'results': [ 1, 2, 3 ]
            })
            
        with self.assertRaises(InvalidResponse):
            self.client.construct_single_location_data({
                'results': [ { 'a': 'b', }, { 'c': 'd', } ]
            })
    
    @patch('requests.get')
    def test_single_location_integration(self, get):
        mock_resp = Mock()
        mock_resp.text = self.success_response_str
        mock_resp.status_code = 200
        mock_resp.json.return_value = self.success_response_dict
        
        get.return_value = mock_resp
        
        districts = self.client.get_districts((12.3456, -10.432))
            
        self.assertEqual(districts, self.success_data)
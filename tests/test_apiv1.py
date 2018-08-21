import json
import unittest

from webob import Request

from modelate import app as application


# from web.thelog import logs
#
# from web.bootstrap_db import prepares
#
# logger = logs(__name__)

# def test_get_id_with_slash(self):
#     request = Request.blank('/recipes/21/', content_type='application/json', environ=self.get)
#     response = request.get_response(application)
#
#     self.assertEqual(response.json.get("result")[0].get('id'), 21)

class APITest(unittest.TestCase):
    def setUp(self):
        self.post = {'REQUEST_METHOD': 'POST'}
        # self.get = {'REQUEST_METHOD': 'GET'}
        # self.options = {'REQUEST_METHOD': 'OPTIONS'}
        # self.put = {'REQUEST_METHOD': 'PUT'}
        # self.patch = {'REQUEST_METHOD': 'PATCH'}
        # self.delete = {'REQUEST_METHOD': 'DELETE'}

    def test_index(self):
        data = json.dumps({'name': 'ichux'})

        request = Request.blank('/api/v1.0', content_type='application/json', environ=self.post, POST=data)
        response = request.get_response(application)
        self.assertEqual(response.json['result']['message']['name'], "ichux")


if __name__ == '__main__':
    unittest.main()

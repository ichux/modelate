import json
import unittest

from webob import Request

from tests import set_env_variables

# this line is necessary before the app is imported!
set_env_variables()

from modelate import app


class APITest(unittest.TestCase):
    def setUp(self):
        self.post = {'REQUEST_METHOD': 'POST'}

    def test_index(self):
        data = json.dumps({'name': 'ichux'})

        request = Request.blank('/api/v1.0', content_type='application/json', environ=self.post, POST=data)
        response = request.get_response(app)
        self.assertEqual(response.json['result']['message']['name'], "ichux")


if __name__ == '__main__':
    unittest.main()

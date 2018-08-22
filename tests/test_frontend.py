import json
import unittest

from webob import Request

from tests import set_env_variables

# this line is necessary before the app is imported!
set_env_variables()

from modelate import app


class FrontendTest(unittest.TestCase):
    def setUp(self):
        self.get = {'REQUEST_METHOD': 'GET'}

    def test_index(self):
        request = Request.blank('/', environ=self.get)
        response = request.get_response(app)
        self.assertIn("Index for Frontend", response.text)


if __name__ == '__main__':
    unittest.main()

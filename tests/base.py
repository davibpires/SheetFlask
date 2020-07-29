import unittest

from sheet import app
from client.generate_jwt import generate_jwt


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestConfig')
        self.client = app.test_client()

        jwt_token = generate_jwt('lucas@sheetgo.com')
        self.headers = {'authorization': f'Bearer {jwt_token}'}

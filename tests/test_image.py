from client.generate_jwt import generate_jwt
from tests.base import BaseTestCase


class TestImage(BaseTestCase):

    # Endpoint /image/convert

    def test_image_convert_missing_jwt(self):
        response = self.client.post('/image/convert')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing Authorization headers', response.data)

    def test_image_convert_have_jwt(self):
        response = self.client.post('/image/convert', headers=self.headers)
        self.assertNotIn(b'Missing Authorization headers', response.data)

    def test_image_convert_no_file(self):
        response = self.client.post('/image/convert', headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file was sent', response.data)

    def test_image_convert_no_format(self):
        with open('client/test.png', 'rb') as image:
            payload = {'file': image}
            response = self.client.post('/image/convert', headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing format parameter', response.data)

    def test_image_convert_format_now_allowed(self):
        with open('client/test.png', 'rb') as image:
            payload = {'file': image, 'format': 'jpg'}
            response = self.client.post('/image/convert', headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Format not allowed', response.data)

    def test_image_convert_wrong_file(self):
        with open('client/test.xlsx', 'rb') as image:
            payload = {'file': image, 'format': 'jpeg'}
            response = self.client.post('/image/convert', headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'The file is not an image', response.data)

    def test_image_convert_image_converted(self):
        with open('client/test.png', 'rb') as image:
            payload = {'file': image, 'format': 'jpeg'}
            response = self.client.post('/image/convert', headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 200)

    # Endpoint /image/convert/fromdropbox

    def test_image_convert_fromdropbox_missing_jwt(self):
        response = self.client.post('/image/convert/fromdropbox')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing Authorization headers', response.data)

    def test_image_convert_fromdropbox_have_jwt(self):
        response = self.client.post('/image/convert/fromdropbox', headers=self.headers)
        self.assertNotIn(b'Missing Authorization headers', response.data)

    def test_image_convert_fromdropbox_missing_access_token(self):
        response = self.client.post('/image/convert/fromdropbox', headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing access_token parameter', response.data)

    def test_image_convert_fromdropbox_have_access_token(self):
        jwt_token = generate_jwt('lucas@sheetgo.com', 'dropbox-access-token')
        headers = {'authorization': f'Bearer {jwt_token}'}
        response = self.client.post('/image/convert/fromdropbox', headers=headers)
        self.assertNotIn(b'Missing access_token parameter', response.data)

    def test_image_convert_fromdropbox_missing_path(self):
        jwt_token = generate_jwt('lucas@sheetgo.com', 'dropbox-access-token')
        headers = {'authorization': f'Bearer {jwt_token}'}
        response = self.client.post('/image/convert/fromdropbox', headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing path parameter', response.data)

    def test_image_convert_fromdropbox_missing_format(self):
        jwt_token = generate_jwt('lucas@sheetgo.com', 'dropbox-access-token')
        headers = {'authorization': f'Bearer {jwt_token}'}
        payload = {'path': '/test.png'}
        response = self.client.post('/image/convert/fromdropbox', headers=headers, data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing format parameter', response.data)

    def test_image_convert_fromdropbox_invalid_access_token(self):
        jwt_token = generate_jwt('lucas@sheetgo.com', 'dropbox-access-token')
        headers = {'authorization': f'Bearer {jwt_token}'}
        payload = {'path': '/test.png', 'format': 'jpeg'}
        response = self.client.post('/image/convert/fromdropbox', headers=headers, data=payload)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid Dropbox access token', response.data)

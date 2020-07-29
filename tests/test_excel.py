from tests.base import BaseTestCase


class TestExcel(BaseTestCase):

    # Endpoint /excel/info

    def test_excel_info_missing_jwt(self):
        response = self.client.post('/excel/info')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing Authorization headers', response.data)

    def test_excel_info_have_jwt(self):
        response = self.client.post('/excel/info', headers=self.headers)
        self.assertNotIn(b'Missing Authorization headers', response.data)

    def test_excel_info_no_binary_file(self):
        response = self.client.post('/excel/info', headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No binary file was sent', response.data)

    def test_excel_info_wrong_file(self):
        with open('client/test.png', 'rb') as file:
            payload = file.read()
            response = self.client.post('/excel/info', headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'The file is not a Excel file', response.data)

    def test_excel_info_get_tabs(self):
        with open('client/test.xlsx', 'rb') as file:
            payload = file.read()
            response = self.client.post('/excel/info', headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'tabs', response.data)

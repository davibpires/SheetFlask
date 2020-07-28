#!/usr/bin/env python3

import optparse
import requests

from generate_jwt import generate_jwt


parser = optparse.OptionParser()
parser.add_option('-e', '--email', action='store', dest='email', help='your email', default='')
parser.add_option('-f', '--file', action='store', dest='file', help='excel file', default='test.xlsx')
options, args = parser.parse_args()

jwt_token = generate_jwt(options.email)

try:
    with open(options.file, 'rb') as file:
        url = 'http://127.0.0.1:5000/excel/info'
        headers = {
            'content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'authorization': f'Bearer {jwt_token}'
        }

        payload = file.read()

        response = requests.post(url, data=payload, headers=headers)

    if response.status_code == requests.codes.ok:
        print(response.json().get('tabs'))
    else:
        print(response.json().get('message', response.json()))
except FileNotFoundError:
    print('File not found.')

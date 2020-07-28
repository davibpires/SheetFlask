#!/usr/bin/env python3

import io
import optparse
import requests

from generate_jwt import generate_jwt


parser = optparse.OptionParser()
parser.add_option('-e', '--email', action='store', dest='email', help='your email', default='')
parser.add_option('-t', '--token', action='store', dest='token', help='Dropbox access token', default='')
parser.add_option('-p', '--path', action='store', dest='path', help='Dropbox image file path', default='')
parser.add_option('-f', '--format', action='store', dest='format', help='conversion format', default='jpeg')
options, args = parser.parse_args()

jwt_token = generate_jwt(options.email, options.token)

url = 'http://127.0.0.1:5000/image/convert/fromdropbox'
headers = {'authorization': f'Bearer {jwt_token}'}

payload = {
    'path': options.path,
    'format': options.format
}

response = requests.post(url, data=payload, headers=headers)

if response.status_code == requests.codes.ok:
    with io.open(f'converted.{options.format}', 'wb') as file:
        file.write(response.content)
    print('Image converted')
else:
    print(response.json().get('message', response.json()))

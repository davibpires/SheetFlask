#!/usr/bin/env python3

import io
import optparse
import requests

from generate_jwt import generate_jwt


parser = optparse.OptionParser()
parser.add_option('-e', '--email', action='store', dest='email', help='your email', default='')
parser.add_option('-i', '--image', action='store', dest='image', help='image file', default='test.png')
parser.add_option('-f', '--format', action='store', dest='format', help='conversion format', default='jpeg')
options, args = parser.parse_args()

token = generate_jwt(options.email)

try:
    with open(options.image, 'rb') as image:
        url = 'http://127.0.0.1:5000/image/convert'
        headers = {'authorization': f'Bearer {token}'}

        files = {'file': image}
        payload = {'format': options.format}

        response = requests.post(url, files=files, data=payload, headers=headers)

    if response.status_code == requests.codes.ok:
        with io.open(f'converted.{options.format}', 'wb') as file:
            file.write(response.content)
        print('Image converted')
    else:
        print(response.json().get('message', response.json()))
except FileNotFoundError:
    print('File not found.')

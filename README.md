# SheetFlask
> Flask API for working with spreadsheets and images.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Authentication using JWT](#authentication-using-jwt)
  - [Tabs from the Excel file](#tabs-from-the-excel-file)
  - [Convert the format of an image](#convert-the-format-of-an-image)
- [Tests with client functions](#tests-with-client-functions)
- [License](#license)
- [Contact](#contact)

## Getting Started

[Python](https://www.python.org/) version >= 3.6 is required to run the project.
You also need the [Docker](https://www.docker.com/) 17.06.0+ and Docker-Compose if you want run it with Docker container.

## Usage

On CLI, in the project directory, type:

```bash
docker-compose up
```

## Endpoints

The application uses [JWT](https://jwt.io/) to authenticate the user.
You need to send a valid JWT token to use it.

## Authentication using JWT

The JWT encryption key is set on config.py on SECRET_KEY parameter.
You also need to set a list of authorized e-mails on parameter AUTHORIZED_USERS on config.py

**The data sent with the token must follow the structure:**

`{"email": "email@company.com"}`

**The token must be sent with the header:**

`Authorization: Bearer <token>`

**Error Responses**

- `401 Unauthorized` missing Authorization headers.
- `401 Unauthorized` invalid Authorization headers.
- `401 Unauthorized` missing email parameter.
- `401 Unauthorized` email not authorized.
- `401 Unauthorized` invalid signature.
- `401 Unauthorized` expired signature.
- `401 Unauthorized` invalid token.

## Tabs from the Excel file

**Definition**

Send a Excel file as Binary File and return a JSON with the list of the tabs from the file, ordered alphabetically.

**Request**

`POST /excel/info/`

**Authorization Header**

`Authorization: Bearer <token>`

**Parameters**

- `binary file` excel binary file *(required)*

**Response**

- [JWT Error Responses](#authentication-using-jwt)
- `400 Bad Request` no binary file was sent.
- `500 Internal Server Error` error reading file.
- `200 OK` on success.

```json
{
  "tabs": [
    "Hello",
    "Python",
    "World"
  ]
}
```
## Convert the format of an image

**Definition**

Send a image file and the "format" as Multipart Form and return the image converted. The formats can be: jpeg or png.

**Request**

`POST /image/convert/`

**Authorization Header**

`Authorization: Bearer <token>`

**Parameters**

- `file` image file *(required)*
- `format` "jpeg" or "png" *(required)*

**Response**

- [JWT Error Responses](#authentication-using-jwt)
- `400 Bad Request` no file was sent.
- `400 Bad Request` you need to specify the format: jpeg, png.
- `400 Bad Request` format not allowed. Allowed conversion formats: jpeg, png.
- `200 OK` with the `converted image` on success,

## Tests with client functions

In the folder `tests`, you will find Python scripts to test the Endpoints as a Client.

All commands here need to be used on CLI in the tests folder.

## excel_info.py

Client test for endpoint [Tabs from the Excel file](#tabs-from-the-excel-file).

**Options**

- `-h`, `--help` show help message
- `-e EMAIL`, `--email=EMAIL` your email *(required)*
- `-f FILE`, `--file=FILE` excel file

**Commands**

```bash
python3 excel_info.py -e email@company.com
```

```bash
python3 excel_info.py -e email@company.com -f PATH/excel-file.xlsx
```

**Response**

- `Missing email parameter` on missing email.
- `File not found` on file path error.
- `Error message` on error.
- `List of tabs` on success.

## convert_img.py

Client test for endpoint [Convert the format of an image](#convert-the-format-of-an-image).

**Options**

- `-h`, `--help` show help message
- `-e EMAIL`, `--email=EMAIL` your email *(required)*
- `-i IMAGE`, `--image=IMAGE` image file
- `-f FORMAT`, `--format=FORMAT` conversion format

**Command**

```bash
python3 convert_img.py -e email@company.com
```

```bash
python3 convert_img.py -e email@company.com -i PATH/image-file.png
```

```bash
python3 convert_img.py -e email@company.com -i PATH/image-file.png -f jpeg
```

**Response**

- `Missing email parameter` on missing email.
- `File not found` on file path error.
- `Error message` on error.
- `Image converted` and save the image with the name `converted` on the test folder on success.

## License
SheetFlask is an open source project by Davi Barros Pires that is licensed under [MIT](https://opensource.org/licenses/MIT).

## Contact
If you like this project, let me know.<br>
Davi Barros Pires <contact@davibarros.com>

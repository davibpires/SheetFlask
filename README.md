# SheetFlask
> Flask API for working with spreadsheets and images.


## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Authentication using JWT](#authentication-using-jwt)
  - [Tabs from the Excel file](#tabs-from-the-excel-file)
  - [Convert the format of an image](#convert-the-format-of-an-image)
  - [Convert the format of a Dropbox image](#convert-the-format-of-a-dropbox-image)
- [Client test functions](#client-test-functions)
- [Unit Tests](#unit-tests)
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

To run the Docker in background, type:

```bash
docker-compose up -d
```


## Endpoints

The application uses [JWT](https://jwt.io/) to authenticate the user.
You need to send a valid JWT token to use it.


## Authentication using JWT

The JWT encryption key is set on config.py on SECRET_KEY parameter.
You also need to set a list of authorized e-mails on parameter AUTHORIZED_USERS on config.py

**The data sent with the token must follow the structure:**

`{"email": "email@company.com"}`

**The Dropbox access token sent together with data must follow the structure:**

`{"email": "email@company.com", "access_token": "dropbox-access-token"}`

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

Send a image file and the format as Multipart Form and return the image converted. The formats can be: jpeg or png.

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
- `400 Bad Request` missing format parameter.
- `400 Bad Request` format not allowed. Allowed conversion formats: jpeg, png.
- `200 OK` with the `converted image` on success,


## Convert the format of a Dropbox image

**Definition**

Send the path for a image file in Dropbox and the format as Multipart Form and return the image converted. The formats can be: jpeg or png.

It's also required the JWT token have the Dropbox access_token inside. See [Authentication using JWT](#authentication-using-jwt).

**Request**

`POST /image/convert/fromdropbox`

**Authorization Header**

`Authorization: Bearer <token>`

**Parameters**

- `path` Dropbox image file path *(required)*
- `format` "jpeg" or "png" *(required)*

**Response**

- [JWT Error Responses](#authentication-using-jwt)
- `401 Unauthorized` invalid Dropbox access token.
- `404 Not Found` dropbox file not found.
- `400 Bad Request` invalid Dropbox path.
- `400 Bad Request` missing access_token parameter.
- `400 Bad Request` missing path parameter.
- `400 Bad Request` missing format parameter.
- `400 Bad Request` format not allowed. Allowed conversion formats: jpeg, png.
- `200 OK` with the `converted image` on success,


## Client test functions

In the folder `client`, you will find Python scripts to test the Endpoints as a Client.

All commands here need to be used on CLI in the client folder.


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

- `File not found` on file path error.
- `Error message` on error.
- `Image converted` and save the image with the name `converted` on the client folder on success.


## convert_fromdropbox.py

Client test for endpoint [Convert the format of a Dropbox image](#convert-the-format-of-a-dropbox-image).

**Options**

- `-h`, `--help` show help message
- `-e EMAIL`, `--email=EMAIL` your email *(required)*
- `-t TOKEN`, `--token=TOKEN` Dropbox access token *(required)*
- `-p PATH`, `--path=PATH` Dropbox image file path *(required)*
- `-f FORMAT`, `--format=FORMAT` conversion format

**Command**

```bash
python3 convert_fromdropbox.py -e email@company.com -t dropbox-access-token -p /dropbox-image.png

```

```bash
python3 convert_fromdropbox.py -e email@company.com -t dropbox-access-token -p /dropbox-image.png -f jpeg
```

**Response**

- `Error message` on error.
- `Image converted` and save the image with the name `converted` on the client folder on success.


## Unit Tests

In the folder `tests`, you will find the Unit Tests for the Endpoints.


**Running unit tests**

With the Docker running (See [Usage](#usage)), open the bash in the Docker, type:

```bash
docker exec -it sheetflask bash
```

To run the unit tests, type:


```bash
pytest -v
```


## License
SheetFlask is an open source project by Davi Barros Pires that is licensed under [MIT](https://opensource.org/licenses/MIT).


## Contact
If you like this project, let me know.<br>
Davi Barros Pires <contact@davibarros.com>

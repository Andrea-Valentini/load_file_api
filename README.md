# Overview

A simple Tornado backend that provides an API endpoint to receive pdf files and to stores files metadata (filename and upload date) into a Postgres database.

## Local Deployment

Clone the repository

```bash
git clone https://github.com/SoFish1/load_file_api.git

cd load_file_api
```

To set up the environment, copy .env_file in the current folder.
Then run the following commands

```bash
docker-compose --env-file .env_file up
```

## Data Validation

The backend validates the input data by checking the following requirements:
* The request header content-type shall be ```bash multipart/form-data ```
* The request body shall be of the following type ```bash {'file': file_content} ``` where only one file per request is allowed
* The filename shall be shorter than 20 chars
* The file shall be a PDF
* A sanity check is performed on the file thanks to the  [Cloudmersive API provider](https://api.cloudmersive.com/python-client.asp)

## Testing

A testing module is also provided to test the endpoint.
To perform the tests run the following command in the project folder:

```bash
    python -m unittest .\tests\test.py   
```
A PGAdmin service is also provided to visualize the database and to check that everyting is as expected.

## Linting
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

The code is linted with Pylint VSCode extension

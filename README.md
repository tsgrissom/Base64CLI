# Base64CLI

A quick CLI written in Python for interacting with base64 hashes in a user-friendly manner.

To run this on Windows from Windows Run (Windows Key+R), put the following line in a `b64d.batch`, the folder for which should be added to your Windows PATH:

`python PATH/TO/REPOSITORY/base64_decode.py %1`

[b64d_sample.bat](https://github.com/tsgrissom/Base64CLI/blob/main/b64d_sample.bat)

### Requirements

The following packages are required and can be installed via the pip command below:
* [colorama](https://pypi.org/project/colorama/)
* [pybase64](https://pypi.org/project/pybase64/)
* [pyperclip](https://pypi.org/project/pyperclip/)
* [virtualenv](https://pypi.org/project/virtualenv/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)

`pip install -r REQUIREMENTS.txt`
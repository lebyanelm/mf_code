## MFCode (Morse Facecode) - python-mfcode

Created and Designed by [@lebyanelm](https://github.com/lebyanelm)
Written in pure Python.

Uses `morse and binary` language to encode string messages onto an image file, similar to **QR Codes** but with **morse code**.

This project is intended to be used in the Facecode software base, but has been released as open source software under the **MIT License**, meaning it can be used by anyone to generate **MFCodes**.

Although the idea of generating **MFCodes** to be scanned to find a certain user biography has been patented by [Nextify Technologies (PTY) LTD](https://www.nextify.co.za) it is allowed to generate your own **MFCodes**.

## Installation

Software source code has been released here in GitHub and [PyPi.org](pypi.org). So you can clone the repository or install this into your own project with **pip**, **pipenv** or any python package manager tool you use.

#### Using PIP
```bash
pip install python-mfcode
```

#### Using PIPENV
```shell
pipenv install python-mfcode
```

## Usage

### Encoding
```python
# Dependencies
import mfcode
import cv2

# The path of the image you want to write the MF encodings on
image_path = 'path/to/your-image.png'
string = 'string_to_encode'

# Encode the MF Code - Returns an array of Pixels of the encoded image
image = mfcode.encode(image_path=image_path, data=string)

# Show the encoded image
cv2.imshow('Encoded Image', image)

```

### Decoding
```python
# Dependencies
import mfcode

encoded_image_path = 'path/to/an_encoded_image.png'

# Decode the encoded image
data = mfcode.decode(encoded_image_path)
print(data) => 'string_encoded'
```


## Versioning
Version numbers follow the MAJOR.MINOR.PATCH scheme. Backwards compatibility breaking changes will be kept to a minimum but be aware that these can occur. Lock your dependencies for production and test your code when upgrading


## License
This bundle is under the MIT license. For the full copyright and license information please view the LICENSE file that was distributed with this source code.

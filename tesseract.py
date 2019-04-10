from io import BytesIO

import pytesseract
import requests
from PIL import Image

# pass image url here
URL = 'https://politdir.de/wp-content/uploads/sites/16/2015/10/mckinsey.png'


def analyze():
    response = requests.get(URL)
    image = Image.open(BytesIO(response.content))
    return pytesseract.image_to_string(image)

print(analyze())

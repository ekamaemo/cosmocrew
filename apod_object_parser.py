import requests
import json
import os
from PIL import Image


def download_image(url, date):
    if not os.path.isfile(f'/static/img/{date}.png'):
        raw_image = requests.get(url).content
        with open(f'static/img/{date}.jpg', 'wb') as file:
            file.write(raw_image)
    else:
        return FileExistsError


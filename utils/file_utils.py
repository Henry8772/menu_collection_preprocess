import os
import json
import io
from google.cloud import vision


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_counter(filename="../output/counter.json"):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('count', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_counter(count, filename="../output/counter.json"):
    with open(filename, 'w') as file:
        json.dump({'count': count}, file)


def save_json(content, filename):
    dir_name = os.path.dirname(filename)
    create_dir(dir_name)
    with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)




def prepare_image_local(image_path):
    try:
        # Loads the image into memory
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        return image
    except Exception as e:
        print(e)
        return

def prepare_image_web(url):
    try:
        # Loads the image into memory
        image = vision.Image()
        image.source.image_uri = url
        return image
    except Exception as e:
        print(e)
        return
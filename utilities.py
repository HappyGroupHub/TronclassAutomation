"""This python will handle some extra functions."""
import sys
from os.path import exists

import ddddocr
import yaml
from yaml import SafeLoader


def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""# ++--------------------------------++
# | TronclassAutomation              |
# | Made by LD (MIT License)         |
# ++--------------------------------++

# FJU Account
username: ''
password: ''

# Headless mode
# If you want to run this script in headless mode, please set this to true.
headless: false
"""
                )
    sys.exit()


def read_config():
    """Read config file.

    Check if config file exists, if not, create one.
    if exists, read config file and return config with dict type.

    :rtype: dict
    """
    if not exists('./config.yml'):
        print("Config file not found, create one by default.\nPlease finish filling config.yml")
        with open('config.yml', 'w', encoding="utf8"):
            config_file_generator()

    try:
        with open('config.yml', 'r', encoding="utf8") as f:
            data = yaml.load(f, Loader=SafeLoader)
            config = {
                'username': data['username'],
                'password': data['password'],
                'headless': data['headless']
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


def get_ocr_answer(ocr_image_path):
    """Get the answer of ocr.

    :rtype: str
    """
    ocr = ddddocr.DdddOcr()
    with open(ocr_image_path, 'rb') as f:
        image = f.read()
    answer = ocr.classification(image)
    return answer

import datetime
import json
import tabulate
import time
import os

def print_dict(data: dict, level: int = 0):
    for key, value in data.items():
        print(level * 4 * " ", end='')
        if type(value) is dict and not len(dict(value)) == 0:
            print(f"{key: <30}")
            print_dict(value, level + 1)
        elif type(value) is list and all(isinstance(n, dict) for n in value):
            print(f"{key: <30}")
            for item in value:
                print_dict(item, level + 1)
        else:
            print(f"{key: <30}{value}")

def print_json(data: dict):
    print(json.dumps(data, indent=4))


def print_table(headers: list, data: list):
    print(tabulate.tabulate(data, headers=headers))


def print_dict_table(data: dict, headers: list = None):
    if headers:
        print(tabulate.tabulate(data, headers=headers))
    else:
        print(tabulate.tabulate(data, headers="keys"))


def to_date(epoch: int) -> str:
    date = datetime.datetime.fromtimestamp(epoch / 1000)
    return date.strftime("%d/%m/%Y, %H:%M:%S")


def now():
    return round(time.time() * 1000)


def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        raise JsonLoadError(f"Error decoding JSON from file {file_path}: {e}")

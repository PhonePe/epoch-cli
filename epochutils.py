import datetime
import json
from collections import OrderedDict
import tabulate
import time


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
    print()


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


def populate_topology_details(raw: json):
    data = OrderedDict()
    data["Id"] = raw["id"]
    data["Topology"] = raw["topology"]
    data["State"] = raw["state"]
    data["Created"] = to_date(raw.get("created"))
    data["Updated"] = to_date(raw.get("updated"))
    return data


def populate_topology_highlights(raw: json):
    data = OrderedDict()
    data["Id"] = raw["id"]
    data["Cron"] = raw["topology"].get("trigger").get("timeSpec")
    data["State"] = raw["state"]
    list_of_resources = raw["topology"].get("task").get("resources")
    for resource in list_of_resources:
        if resource.get("type") == "CPU":
            data["CPU"] = resource.get("count")
        elif resource.get("type") == "MEMORY":
            data["Memory"] = resource.get("sizeInMB")
    data["Created"] = to_date(raw.get("created"))
    data["Updated"] = to_date(raw.get("updated"))
    return data


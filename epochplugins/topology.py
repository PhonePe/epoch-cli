import argparse

import epochclient
import epochplugins
from collections import OrderedDict
import json
import epochutils
from types import SimpleNamespace


class Applications(epochplugins.EpochPlugin):
    def __init__(self) -> None:
        pass

    def populate_options(self, epoch_client: epochclient.EpochClient, subparser: argparse.ArgumentParser):
        parser = subparser.add_parser("topology", help="Epoch topology related commands")

        commands = parser.add_subparsers(help="Available commands for topology management")

        sub_parser = commands.add_parser("list", help="Show all the topologies on the cluster")
        sub_parser.set_defaults(func=self.list)

        sub_parser = commands.add_parser("run", help="Run the given topology")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.set_defaults(func=self.run)

        sub_parser = commands.add_parser("get", help="Get Topology on cluster")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.set_defaults(func=self.get)

        sub_parser = commands.add_parser("pause", help="Pause Topology on cluster")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.set_defaults(func=self.pause)

        sub_parser = commands.add_parser("unpause", help="Unpause Topology on cluster")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.set_defaults(func=self.unpause)

        sub_parser = commands.add_parser("delete", help="Delete Topology on cluster")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.set_defaults(func=self.delete)

        sub_parser = commands.add_parser("create", help="Create Topology on cluster")
        sub_parser.add_argument("spec_file", metavar="spec-file", help="JSON spec file for the application")
        sub_parser.set_defaults(func=self.create)

        sub_parser = commands.add_parser("update", help="Update Topology on cluster")
        sub_parser.add_argument("spec_file", metavar="spec-file", help="JSON spec file for the application")
        sub_parser.set_defaults(func=self.update)

        super().populate_options(epoch_client, parser)

    def list(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies")
        headers = ["Id", "Cron", "State", "CPU", "Memory", "Created", "Updated"]
        rows = []
        for app_data in data:
            row = [app_data["id"], app_data["topology"].get("trigger").get("timeSpec"), app_data["state"]]
            list_of_resources = app_data["topology"].get("task").get("resources")
            for resource in list_of_resources:
                if resource.get("type") == "CPU":
                    row.append(resource.get("count"))
                elif resource.get("type") == "MEMORY":
                    row.append(resource.get("sizeInMB"))
            row.append(epochutils.to_date(app_data.get("created")))
            row.append(epochutils.to_date(app_data.get("updated")))
            rows.append(row)
        epochutils.print_table(headers, rows)

    def run(self, options: SimpleNamespace):
        data = self.epoch_client.put("/apis/v1/topologies/{topology_id}/run".format(topology_id=options.topology_id),
                                     None)
        epochutils.print_json(data)

    def get(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies/{topology_id}".format(topology_id=options.topology_id))
        app_data = OrderedDict()
        app_data["Id"] = data["id"]
        app_data["Topology"] = data["topology"]
        app_data["State"] = data["state"]
        app_data["Created"] = epochutils.to_date(data.get("created"))
        app_data["Updated"] = epochutils.to_date(data.get("updated"))
        epochutils.print_dict(app_data)

    def pause(self, options: SimpleNamespace):
        data = self.epoch_client.put("/apis/v1/topologies/{topology_id}/pause".format(topology_id=options.topology_id),
                                     None)
        epochutils.print_json(data)

    def unpause(self, options: SimpleNamespace):
        data = self.epoch_client.put(
            "/apis/v1/topologies/{topology_id}/unpause".format(topology_id=options.topology_id), None)
        epochutils.print_json(data)

    def delete(self, options: SimpleNamespace):
        data = self.epoch_client.delete("/apis/v1/topologies/{topology_id}".format(topology_id=options.topology_id),
                                        None)
        epochutils.print_json(data)

    def create(self, options: SimpleNamespace):
        try:
            with open(options.spec_file, 'r') as fp:
                spec = json.load(fp)
            self.epoch_client.post("/apis/v1/topologies", spec)
            print("Topology created : {topology_id}".format(topology_id=spec["name"]))
        except (OSError, IOError) as e:
            print("Error creating topology. Error: " + str(e))

    def update(self, options: SimpleNamespace):
        try:
            with open(options.spec_file, 'r') as fp:
                spec = json.load(fp)
            self.epoch_client.put("/apis/v1/topologies", spec)
            print("Topology updated : {topology_id}".format(topology_id=spec["name"]))
        except (OSError, IOError) as e:
            print("Error creating topology. Error: " + str(e))

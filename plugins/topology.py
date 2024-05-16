import argparse

import epochclient
import plugins
import json
import epochutils
from types import SimpleNamespace


class Applications(plugins.EpochPlugin):
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
        headers = ["Id", "Cron", "State", "CPU", "Memory","Created", "Updated"]
        print("\t".join(headers))
        for app_data in data:
            app_details = list(epochutils.populate_topology_highlights(app_data).values())
            padding_map = {0: 60, 1: 20, 2: 6, 3: 5}
            print("\t".join([str(val).ljust(padding_map.get(i, 10)) for i, val in enumerate(app_details)]))

    def run(self, options: SimpleNamespace):
        data = self.epoch_client.put("/apis/v1/topologies/{topology_id}/run".format(topology_id=options.topology_id), None)
        epochutils.print_json(data)

    def get(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies/{topology_id}".format(topology_id=options.topology_id))
        epochutils.print_dict(epochutils.populate_topology_details(data))

    def pause(self, options: SimpleNamespace):
        data = self.epoch_client.put("/apis/v1/topologies/{topology_id}/pause".format(topology_id=options.topology_id), None)
        epochutils.print_json(data)

    def unpause(self, options: SimpleNamespace):
        data = self.epoch_client.put("/apis/v1/topologies/{topology_id}/unpause".format(topology_id=options.topology_id), None)
        epochutils.print_json(data)

    def delete(self, options: SimpleNamespace):
        data = self.epoch_client.delete("/apis/v1/topologies/{topology_id}".format(topology_id=options.topology_id), None)
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

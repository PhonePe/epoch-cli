import argparse

import epochclient
import plugins

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

        sub_parser = commands.add_parser("Create", help="Create Topology on cluster")
        sub_parser.set_defaults(func=self.create)

        super().populate_options(epoch_client, parser)

    def list(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies")
        for app_data in data:
            epochutils.print_dict(epochutils.populate_topology_details(app_data))

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
        data = self.epoch_client.delete("/apis/v1/topologies/{topology_id}".format(topology_id=options.topology_id), None)
        epochutils.print_json(data)

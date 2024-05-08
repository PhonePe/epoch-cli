import argparse
import json
from collections import OrderedDict

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

        sub_parser = commands.add_parser("get-runs", help="Get the runs for the given topology")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.set_defaults(func=self.get_runs)

        sub_parser = commands.add_parser("get", help="Get Topology on cluster")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.set_defaults(func=self.get)

        super().populate_options(epoch_client, parser)

    def list(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies")
        for app_data in data:
            epochutils.print_dict(self.populate_topology_details(app_data))

    def get_runs(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies/{topology_id}/runs".format(topology_id=options.topology_id))
        epochutils.print_json(data)

    def get(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies/{topology_id}".format(topology_id=options.topology_id))
        data = self.populate_topology_details(data)
        epochutils.print_dict(data)

    def populate_topology_details(self, raw: json):
        data = OrderedDict()
        data["Id"] = raw["id"]
        data["Topology"] = raw["topology"]
        data["State"] = raw["state"]
        data["Created"] = epochutils.to_date(raw.get("created"))
        data["Updated"] = epochutils.to_date(raw.get("updated"))
        return data

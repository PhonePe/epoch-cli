import argparse

import epochclient
import plugins

from types import SimpleNamespace

class Applications(plugins.EpochPlugin):
    def __init__(self) -> None:
        pass

    def populate_options(self, epoch_client: epochclient.EpochClient, subparser: argparse.ArgumentParser):
        parser = subparser.add_parser("cluster", help="Epoch Cluster related commands")

        commands = parser.add_subparsers(help="Available commands for Cluster management")

        sub_parser = commands.add_parser("leader", help="Get the leader on the cluster")
        sub_parser.set_defaults(func=self.leader)

        super().populate_options(epoch_client, parser)

    def leader(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/housekeeping/v1/leader")
        print(data)

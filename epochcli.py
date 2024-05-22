import argparse
from types import SimpleNamespace
import epochclient
from epochplugins import EpochPlugin


class EpochCli:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser
        self.epoch_client = epochclient.EpochClient()
        self.plugins: list = []
        self.debug = False
        subparsers = parser.add_subparsers(help="Available plugins")
        for plugin_class in EpochPlugin.plugins:
            plugin = plugin_class()
            plugin.populate_options(epoch_client=self.epoch_client, subparser=subparsers)
            self.plugins.append(plugin)
        parser.set_defaults(func=self.show_help)

    def run(self):
        args = self.parser.parse_args()
        self.debug = args.debug
        epoch_client = epochclient.build_epoch_client(self.epoch_client, args=args)
        if epoch_client is None:
            return None
        self.epoch_client = epoch_client
        args.func(args)

    def show_help(self, options: SimpleNamespace) -> None:
        self.parser.print_help()
        exit(-1)
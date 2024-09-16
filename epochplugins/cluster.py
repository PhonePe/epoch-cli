import argparse

import epochclient
import epochplugins
import json

from types import SimpleNamespace

import epochutils


class Applications(epochplugins.EpochPlugin):
    def __init__(self) -> None:
        pass

    def populate_options(self, epoch_client: epochclient.EpochClient, subparser: argparse.ArgumentParser):
        parser = subparser.add_parser("cluster", help="Epoch Cluster related commands")

        commands = parser.add_subparsers(help="Available commands for Cluster management")

        sub_parser = commands.add_parser("leader", help="Get the leader on the cluster")
        sub_parser.set_defaults(func=self.leader)

        sub_parser = commands.add_parser("save", help="save the topologies in a json")
        sub_parser.add_argument("file_name", metavar="file-name", help="Name of file to be saved")
        sub_parser.set_defaults(func=self.save)

        sub_parser = commands.add_parser("load", help="load the topologies to the given cluster")
        sub_parser.add_argument("-file_name", metavar="file-name", help="Name of file to be loaded")
        sub_parser.add_argument("--override", metavar="override_flag",
                                help="For controlling overriding of the existing topologies", default=False)
        sub_parser.add_argument("--paused", metavar="paused", help="Load all paused topologies", default=False)
        # sub_parser.add_argument("--override", metavar="p", help="Load all paused topologies", default=False)

        # sub_parser.add_argument('--override', action='override', help='Override existing topologies if the topology exists')
        # sub_parser.add_argument("run_id", metavar="run-id", help="Run ID")
        # sub_parser.add_argument("task_name", metavar="task-name", help="Task Name")
        sub_parser.set_defaults(func=self.load)

        super().populate_options(epoch_client, parser)

    def leader(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/housekeeping/v1/leader")
        print(data)

    def save(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies")
        file_name = options.file_name
        with open(file_name + ".json", 'w') as f:
            json.dump(data, f)

    def load(self, options: SimpleNamespace):
        current_cluster_data = self.epoch_client.get("/apis/v1/topologies")
        json_data = epochutils.load_json(options.file_name)
        topologies_to_load = self.filter_topologies(current_cluster_data, json_data, options)
        try:
            for data in topologies_to_load:
                self.epoch_client.post("/apis/v1/topologies", data.get("topology"))
                print("Topology created : {topology_id}".format(topology_id=data.get("name")))
        except Exception as ex:
            print("Error creating topology. Error: " + str(ex))

    def filter_topologies(self, current_cluster_data, topologies_from_json, options: SimpleNamespace):
        if options.paused:
            topologies_from_json = [topology for topology in topologies_from_json if topology.get('state') == "PAUSED"]
        if not options.override:
            return topologies_from_json
        ids = set()
        for topology in topologies_from_json:
            ids.add(topology.get("id"))
        topologies_overriden = [topology for topology in current_cluster_data if (topology.get("id") in ids)]
        print(topologies_overriden)
        for topology in topologies_overriden:
            data = self.epoch_client.delete("/apis/v1/topologies/{topology_id}".format(topology.get("id"), None))
            epochutils.print_json(data)
        return topologies_from_json

import argparse

import epochclient
import epochplugins
import json
from epochplugins.filter_topologies import FilteredTopologies
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

        sub_parser = commands.add_parser("export", help="export the topologies in a json file")
        sub_parser.add_argument("file_name", metavar="file-name", help="Name of file to be saved")
        sub_parser.set_defaults(func=self.export_topologies)

        sub_parser = commands.add_parser("import", help="load the topologies to the given cluster")
        sub_parser.add_argument("file_name", metavar="file-name", help="Name of file to be loaded")
        sub_parser.add_argument("--overwrite", metavar="overwrite_flag",
                                help="Set this, if you wish to overwrite topologies that already exist, during the import",
                                default=False)
        sub_parser.add_argument("--paused", metavar="paused", help="import all topologies in PAUSED state",
                                default=False)
        sub_parser.add_argument("--skip", metavar="skipped topologies",
                                help="Comma separated values of Topologies to need to be explicitly skipped during import",
                                default="")
        sub_parser.set_defaults(func=self.import_topologies)

        sub_parser = commands.add_parser("pause-all", help="pause all the topologies to the given cluster")
        sub_parser.set_defaults(func=self.pause_all_topologies)

        super().populate_options(epoch_client, parser)

    def leader(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/housekeeping/v1/leader")
        print(data)

    def pause_all_topologies(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies")
        for topology in data:
            try:
                self.epoch_client.put("/apis/v1/topologies/{topology_id}/pause".format(topology_id=topology.get("id")),
                                      None)
                print("Topology paused : {topology_id}".format(topology_id=topology.get("id")))
            except Exception as ex:
                print("Error pausing topology. Error: " + str(ex))

    def export_topologies(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies")
        file_name = options.file_name
        with open(file_name + ".json", 'w') as f:
            json.dump(data, f)

    def import_topologies(self, options: SimpleNamespace):
        current_cluster_data = self.epoch_client.get("/apis/v1/topologies")
        json_data = epochutils.load_json(options.file_name)
        filtered_topologies = self.filter_topologies(current_cluster_data, json_data, options)
        topologies_to_overwrite = filtered_topologies.topologies_to_overwrite
        topologies_to_create = filtered_topologies.topologies_to_create
        self.overrwrite_topologies(options, topologies_to_overwrite)
        self.create_topologies(options, topologies_to_create)

    def create_topologies(self, options, topologies_to_create):
        if topologies_to_create:
            for data in topologies_to_create:
                try:
                    self.epoch_client.post("/apis/v1/topologies", data.get("topology"))
                    print("Topology created : {topology_id}".format(topology_id=data.get("id")))
                    self.pause_topology(data, options)
                except Exception as ex:
                    print("Error creating topology " + data.get("id") + " Error: " + str(ex))

    def pause_topology(self, data, options):
        if options.paused:
            self.epoch_client.put(
                "/apis/v1/topologies/{topology_id}/pause".format(topology_id=data.get("id")),
                None)

    def overrwrite_topologies(self, options, topologies_to_overwrite):
        if topologies_to_overwrite:
            for data in topologies_to_overwrite:
                try:
                    self.epoch_client.put("/apis/v1/topologies", data.get("topology"))
                    print("Topology updated : {topology_id}".format(topology_id=data.get("id")))
                    self.pause_topology(data, options)
                except Exception as ex:
                    print("Error updating topology " + data.get("id") + " Error: " + str(ex))

    def filter_topologies(self, current_cluster_data, topologies_from_json,
                          options: SimpleNamespace) -> FilteredTopologies:
        filtered_topologies = FilteredTopologies()
        skipped_topologies = options.skip.split(',')

        if len(skipped_topologies) > 0:
            topologies_from_json = [topology for topology in topologies_from_json if
                                    topology.get('id') not in skipped_topologies]

        if not options.overwrite:
            for topology in topologies_from_json:
                filtered_topologies.add_to_create_topology(topology)
            return filtered_topologies

        ids = set(topology.get("id") for topology in topologies_from_json)
        overwritten_topologies_ids = {topology.get("id") for topology in current_cluster_data if
                                      topology.get("id") in ids}

        for topology in topologies_from_json:
            if topology.get("id") in overwritten_topologies_ids:
                filtered_topologies.add_to_overwrite_topology(topology)
            else:
                filtered_topologies.add_to_create_topology(topology)

        return filtered_topologies

import argparse

import epochclient
import plugins

import epochutils
from types import SimpleNamespace


class Applications(plugins.EpochPlugin):
    def __init__(self) -> None:
        pass

    def populate_options(self, epoch_client: epochclient.EpochClient, subparser: argparse.ArgumentParser):
        parser = subparser.add_parser("runs", help="Epoch Runs related commands")

        commands = parser.add_subparsers(help="Available commands for run management")

        sub_parser = commands.add_parser("list", help="Show all the runs on given topology")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.set_defaults(func=self.list)

        sub_parser = commands.add_parser("get", help="Get the run for the given topology and run Id")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.add_argument("run_id", metavar="run-id", help="Run ID")
        sub_parser.set_defaults(func=self.get)

        sub_parser = commands.add_parser("kill", help="Kill task")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.add_argument("run_id", metavar="run-id", help="Run ID")
        sub_parser.add_argument("task_id", metavar="task-id", help="Task ID")
        sub_parser.set_defaults(func=self.kill)

        sub_parser = commands.add_parser("log", help="Get the log for the task")
        sub_parser.add_argument("topology_id", metavar="topo-id", help="Topology ID")
        sub_parser.add_argument("run_id", metavar="run-id", help="Run ID")
        sub_parser.add_argument("task_id", metavar="task-id", help="Task ID")
        sub_parser.set_defaults(func=self.log)

        super().populate_options(epoch_client, parser)

    def list(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies/{topology_id}/runs".format(
            topology_id=options.topology_id))
        for app_data in data:
            epochutils.print_dict(app_data)
    def kill(self, options: SimpleNamespace):
        data = self.epoch_client.post("/apis/v1/topologies/{topology_id}/runs/{run_id}/tasks/{task_id}/kill".format(
            topology_id=options.topology_id, run_id=options.run_id, task_id=options.task_id), None)
        print(data)

    def get(self, options: SimpleNamespace):
        data = self.epoch_client.get(
            "/apis/v1/topologies/{topology_id}/runs/{run_id}".format(topology_id=options.topology_id,
                                                                   run_id=options.run_id))
        epochutils.print_dict(data)

    def log(self, options: SimpleNamespace):
        data = self.epoch_client.get("/apis/v1/topologies/{topology_id}/runs/{run_id}/tasks/{task_id}/log".format(
            topology_id=options.topology_id, run_id=options.run_id, task_id=options.task_id))
        epochutils.print_json(data)

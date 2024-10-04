from typing import List, Dict, Any


class FilteredTopologies:
    def __init__(self):
        self.topologies_to_create: List[Dict[str, Any]] = []
        self.topologies_to_overwrite: List[Dict[str, Any]] = []

    def add_to_create_topology(self, topology: Dict[str, Any]):
        self.topologies_to_create.append(topology)

    def add_to_overwrite_topology(self, topology: Dict[str, Any]):
        self.topologies_to_overwrite.append(topology)

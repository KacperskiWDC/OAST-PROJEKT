# AI

import  re

from    typing import Dict, List

class DemandPath:
    
    def __init__(
        self, 
        demand_id:  int, 
        path_id:    int, 
        links:      List
    ) -> None:
        self.demand_id = demand_id
        self.path_id = path_id
        self.links = links


def loadDemandPaths(
    path: str
) -> Dict:
    demand_paths = {}

    pattern = re.compile(
        r"set\s+DemandPath_links\[(\d+),(\d+)\]\s*:=\s*([\d\s]+);"
    )

    with open(path, "r") as file:
        for line in file:
            match = pattern.search(line)

            if match:
                demand_id = int(match.group(1))
                path_id = int(match.group(2))
                links = [int(x) for x in match.group(3).split()]

                if demand_id not in demand_paths:
                    demand_paths[demand_id] = {}

                demand_paths[demand_id][path_id] = DemandPath(
                    demand_id,
                    path_id,
                    links
                )

    return demand_paths
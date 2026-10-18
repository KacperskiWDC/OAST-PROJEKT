from    typing import List, Dict

class Demand:

    def __init__(
        self, 
        demand_id: int, 
        src:       int, 
        dst:       int, 
        volume:    int, 
        max_paths: int
    ) -> None:
        self.id        = demand_id+1
        self.src       = src
        self.dst       = dst
        self.volume    = volume
        self.max_paths = max_paths

def _importDemands(
    content: str
) -> Dict[int, Demand]:

    section = content.split("param: Demands:")[1].split(";")[0]
    rows    = section.split(":=")[1].strip().splitlines()
    demands = {}
    for i, row in enumerate(rows):
        data = list(map(int, row.split()))
        demands[i] = Demand(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4]
        )

    return demands

def openLinkDemands(
    path: str=""
) -> Dict[int, Demand] | None:

    data = ""
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError | FileExistsError:
        pass

    if data == "":
        return

    return _importDemands(data)


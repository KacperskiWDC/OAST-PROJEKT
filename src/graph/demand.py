from    typing import List, Dict

from    .utils import importData

class Demand:

    def __init__(
        self, 
        demand_id: int, 
        src:       int, 
        dst:       int, 
        volume:    int, 
        maxPaths: int
    ) -> None:
        self.id        = demand_id
        self.src       = src
        self.dst       = dst
        self.volume    = volume
        self.maxPaths  = maxPaths

    def __repr__(
        self
    ) -> str:
        print(
            f'''
            demand   = {self.id}
            src      = {self.src}
            dst      = {self.dst}
            volume   = {self.volume}
            maxPaths = {self.maxPaths}            
            '''
        )
        return ""

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

    data = importData(path=path)

    if data == "":
        return

    return _importDemands(data)


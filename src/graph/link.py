import re
from typing import Dict
from .utils import importData


class Link:
    def __init__(self, nodeA: int, nodeZ: int, value: int):
        self.nodeA = nodeA
        self.nodeZ = nodeZ
        #liczba modułów (DAP) albo koszt modułu (DDAP)
        self.value = value


class Links:
    def __init__(self, moduleCapacity: int, links: Dict[int, Link]):
        self.moduleCapacity = moduleCapacity
        self.links = links

    def getLink(self) -> Dict[int, Link]:
        return self.links


def _importLink(content: str) -> Links:
    capacity_match = re.search(r"param\s+moduleCapacity\s*:=\s*(\d+);", content)
    module_capacity = int(capacity_match.group(1)) if capacity_match else 1

    section = content.split("param: Links:")[1].split(";")[0]
    rows = section.split(":=")[1].strip().splitlines()

    links_dict = {}
    for row in rows:
        data = list(map(int, row.split()))
        link_id = data[0]
        links_dict[link_id] = Link(data[1], data[2], data[3])

    return Links(module_capacity, links_dict)


def openLinkParams(path: str = "") -> Links | None:
    data = importData(path=path)
    if data == "":
        return None
    return _importLink(data)
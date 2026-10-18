from    typing import List, Dict

class Links:

    def __init__(
        self,
        rawData: List
    ) -> None:
        
        self._connections = {}
        for i, row in enumerate(rawData):
            data = row.split(sep=' ')
            self._connections[i] = (
                data[1], data[2], data[3]
            )

        print(self._connections)

    def getLink(
        self
    ) -> Dict:
        return self._connections


def _importLink(
    content: str
) -> Links:

    section = content.split("param: Links:")[1].split(";")[0]
    rows    = section.split(":=")[1].strip().splitlines()
    return Links(rows)

def openLinkParams(
    path: str=""
) -> Links | None:

    data = ""
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError | FileExistsError:
        pass

    if data == "":
        return

    return _importLink(data)
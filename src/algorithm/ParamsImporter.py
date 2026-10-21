import  os
import  json

from    typing import Tuple

class ParamsImporter:

    def __init__(
        self,
        population:  int=100,
        crossovers:  int=20,
        pc:          float=0.1,
        pm:          float=0.1,
        seed:        int=13,
        epochs_num:  int=1000
    ) -> None:

        self._population    = population
        self._crossovers    = crossovers
        self._pc            = pc
        self._pm            = pm
        self._seed          = seed
        self._epochs_num    = epochs_num

    def getPopulationSize(
        self
    ) -> int:
        return self._population

    def getCrossovers(
        self
    ) -> int:
        return self._crossovers

    def getCrossoverProbabilty(
        self
    ) -> float:
        return self._pc

    def getMutationProbabilty(
        self
    ) -> float:
        return self._pm

    def getSeed(
        self
    ) -> int:
        return self._seed

    def getEpochsNum(
        self
    ) -> int:
        return self._epochs_num

def _checkProblemType(
    type: str="",
    *,
    _problemTypes=[
        "DAP",
        "DDAP"
    ]
) -> bool:
    for problemType in _problemTypes:
        if type == problemType:
            return True
    return False

def importAlgParams(
    path:   str
) -> Tuple[ParamsImporter, str] | None:

    if not os.path.exists(path=path):
        return

    try:
        file = open(path, mode="r+")
    except FileExistsError as FileNotFoundError:
        return
    else:
        with file as fp:

            params  = json.load(fp=fp)
            content = params["alg_params"]
            paramImporter = ParamsImporter(
                population=content["population"],
                crossovers=content["N"],
                pc=content["pc"],
                pm=content["pm"],
                seed=content["seed"],
                epochs_num=content["epochs_num"]            
            )
            problem_type = params["problem_type"]

            if not _checkProblemType(problem_type):
                return

            return paramImporter, problem_type 

import os

from typing                     import Dict, List, Any

from algorithm.ParamsImporter   import ParamsImporter, importAlgParams
from algorithm.solver           import solver

from graph.link                 import Links, openLinkParams
from graph.demand               import Demand, openLinkDemands
from graph.DemandPathLink       import DemandPath, loadDemandPaths


DEFAUTL_PATH = os.getcwd() + "/params.json"

def _setupProblemPath(
    problemType: str
) -> str:

    if problemType.lower() == "dap":
        return os.getcwd() + "/alg_params/dap-net4-26Z.txt"

    if problemType.lower() == "ddap":
        return os.getcwd() + "/alg_params/ddap-net4-26Z.txt"
    
    return ""

def main() -> None:

    # import data
    algParams, problemType = importAlgParams(path=DEFAUTL_PATH)
    problemTypePath        = _setupProblemPath(problemType)
    links                  = openLinkParams(path=problemTypePath)
    demands                = openLinkDemands(path=problemTypePath)
    demandPathLink         = loadDemandPaths(path=problemTypePath)

    solver(
        algParams=algParams,
        links=links,
        demands=demands,
        demandPathLink=demandPathLink
    )

if __name__ == "__main__":
    main()
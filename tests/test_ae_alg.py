from src.algorithm.ParamsImporter import ParamsImporter 

def test_default_params_init() -> None:

    paramsImporter = ParamsImporter()

    assert paramsImporter.getPopulationSize()       == 100
    assert paramsImporter.getChromosomesNum()       == 20
    assert paramsImporter.getCrossoverProbabilty()  == 0.1
    assert paramsImporter.getMutationProbabilty()   == 0.1
    assert paramsImporter.getSeed()                 == 13
    assert paramsImporter.getEpochsNum()            == 1000
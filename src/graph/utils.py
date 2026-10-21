def importData(
    path: str="" 
) -> str:

    data = ""
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError | FileExistsError:
        pass

    return data
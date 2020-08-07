def build_path(path : str) -> str:
    resultpath = path
    if resultpath == "":
        resultpath = "/"
    elif resultpath[-1] != "/":
        resultpath = f"{resultpath}/"
    return resultpath

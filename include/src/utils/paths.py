from pathlib import Path


def find_root(reference="docker-compose.yaml") -> Path:
    cwd = Path(__file__).resolve().parent

    if (cwd / reference).is_file():
        return cwd

    for parent in [cwd, *cwd.parents]:
        if (parent / reference).is_file():
            return parent

    for children in cwd.rglob(reference):
        return children.parent

    raise FileNotFoundError("não mapeado")


ROOT = find_root()

# mapeando tudo a partir de root para ficar mais fácil de identificar
# poderia ser com:
#   os.environ["INCLUDE"] = f"{ROOT}/include"
ENTRYPOINTS = f"{ROOT}/entrypoints"
INCLUDE = f"{ROOT}/include"
ASSETS = f"{ROOT}/include/assets"
PIPELINES = f"{ROOT}/include/pipelines"
SRC = f"{ROOT}/include/src"
TMP = f"{ROOT}/tmp"
LOGS = f"{ROOT}/logs/"

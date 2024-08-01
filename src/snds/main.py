import pathlib
from snds.transform import transform
from snds.io.schemas import get_schemas_files

get_schemas_files()

snds_graph = transform(pathlib.Path.cwd() / "temp" / "schemas" / "ER_PRS_F.json")

jsonld = snds_graph.serialize(format="json-ld")

print(jsonld[:1000])

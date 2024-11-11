import pathlib
from snds.transform import transform
from snds.io.schemas import get_schemas_files

from snds.model.base import Base

get_schemas_files()
arg1 = [pathlib.Path.cwd() / "temp" / "schemas" / "ER_PRS_F.json"]
arg2 = pathlib.Path.cwd() / "temp" / "schemas" / "ER_PRS_F.json"
snds_graph = transform(arg1)
ld = snds_graph.serialize(format="json-ld")
print(ld)

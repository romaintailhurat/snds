import pathlib
from snds.transform import transform
from snds.io.schemas import get_schemas_files

schema_paths = get_schemas_files()
snds_graph = transform(schema_paths[0])
graph_json_ld = snds_graph.serialize(format="json-ld")
print(graph_json_ld)

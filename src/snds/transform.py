import pathlib
import json
import uuid
import logging
from typing import Any, cast
from snds.model.snds import Schema
from snds.model.variable import Variable
from rdflib import Graph

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def snds_to_ddi(table: Schema):
    """Transform a SNDS table schema to a DDI-L RDF object."""
    # TODO type the table parameter, it's probably a dict
    fields = table["fields"]
    table_graph = Graph()

    for snds_var in fields:
        var = Variable(str(uuid.uuid4()), "1", "agency", snds_var["name"])
        var.add_representation_from_snds_variable(snds_var)
        table_graph = table_graph + var.to_rdf()

    return table_graph


class IllegalArgumentError(ValueError):
    """Raised when a bad argument is provided."""
    pass


def transform_one(source: pathlib.Path):
    with open(source, "r") as source_file:
        table = json.load(source_file)
        result_graph = snds_to_ddi(table)
        return result_graph


def transform(source: pathlib.Path | list[pathlib.Path]):
    """Transform from a file path or a list of file paths."""
    graph = Graph()
    # Source is a list of paths.
    if type(source) is list and issubclass(type(source[0]), pathlib.Path):
        for file_path in source:
            subgraph = transform_one(file_path)
            graph = graph + subgraph
    # Source is a unique path.
    elif issubclass(type(source), pathlib.Path):
        graph = transform_one(cast(pathlib.Path, source))
    else:
        raise IllegalArgumentError
    return graph

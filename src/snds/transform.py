import pathlib
import json
import uuid
from typing import Any
from snds.model.variable import Variable
from rdflib import Graph


def snds_to_ddi(table: Any):
    """Transform a SNDS table schema to a DDI-L RDF object."""
    # TODO type the table parameter, it's probably a dict
    fields = table["fields"]
    table_graph = Graph()

    for field in fields:
        source_var = field
        var = Variable(str(uuid.uuid4()), "1", "agency", field["name"])
        table_graph = table_graph + var.to_rdf()

    return table_graph

class IllegalArgumentError(ValueError):
    """Raised when a bad argument is provided."""
    pass

def transform(source: pathlib.Path | list[pathlib.Path]):
    """Transform from a file path or a list of file paths."""

    if type(source) is list and issubclass(type(source[0]),  pathlib.Path) :
        print("a list of Path")
    elif issubclass(type(source), pathlib.Path):
        print("a Path")
    else:
        raise IllegalArgumentError

    # if issubclass(type(source), pathlib.Path):
    #     with open(source, "r") as source_file:
    #         table = json.load(source_file)
    #         result_graph = snds_to_ddi(table)
    #         return result_graph
    # elif type(source) is list[pathlib.PosixPath]:
    #     return NotImplemented("TODO")
    # else:
    #     raise Exception("You should provide a PosixPath or a list of PosixPath.")

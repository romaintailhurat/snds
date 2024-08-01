import pathlib
import json
import uuid
from typing import Any
from snds.model.variable import Variable
from rdflib import Graph


def snds_to_ddi(table: Any):
    """Transform a SNDS table schemas to a DDI L JSON-LD object."""
    # TODO type the table parameter, it's probably a dictr
    fields = table["fields"]
    table_graph = Graph()

    for field in fields:
        source_var = field
        var = Variable(str(uuid.uuid4()), "1", "agency", field["name"])
        table_graph = table_graph + var.to_rdf()

    return table_graph


def transform(source: pathlib.Path):
    with open(source, "r") as source_file:
        table = json.load(source_file)
        result_graph = snds_to_ddi(table)

    return result_graph

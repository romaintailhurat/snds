import dataclasses

from rdflib.term import Literal
from snds.model.base import Base, DDI
from rdflib import Graph, URIRef, RDF

class Variable(Base):
    VariableName: str

    def __init__(self, ID, Version, Agency, VariableName) -> None:
        super().__init__(ID, Version, Agency)
        self.VariableName = VariableName

    def to_rdf(self) -> Graph:
        g = Graph()
        var = URIRef(f"http://snds.org/{self.ID}")
        g.add((var, RDF.type, DDI.Variable))
        g.add((var, DDI.VariableName, Literal(self.VariableName)))
        return g

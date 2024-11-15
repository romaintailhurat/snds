from typing import Annotated
import uuid
from annotated_types import Ge
from rdflib.term import Literal
from snds.model.base import URIIdentifiable, Versionable, DDI, SNDS
from rdflib import Graph, URIRef, RDF

from snds.model.snds import SNDSVariable

PositiveInt = Annotated[int, Ge(0)]


class Representation(URIIdentifiable):
    """Super class for various representations.
    Not used directly but provides a method to return the correct implementation."""

    @staticmethod
    def from_snds_variable(variable: SNDSVariable):
        """Return the right `Representation`subclass from a SNDS variable type."""
        match variable["type"]:
            case "string":
                return TextRepresentationBase()
            case _:
                return TextRepresentationBase()

    def to_rdf(self) -> Graph:
        return Graph()


class TextRepresentationBase(Representation, URIIdentifiable):
    """Text representation, see https://ddialliance.github.io/ddimodel-web/DDI-L-3.3/composite-types/TextRepresentationBaseType/"""

    MaxLength: PositiveInt
    MinLength: PositiveInt

    def __init__(self) -> None:
        super().__init__()
        self._uri = SNDS[f"TextRepresentation/{self._id}"]

    def to_rdf(self):
        g = Graph()
        g.add((self._uri, RDF.type, DDI.TextRepresentation))
        return g


class VariableRepresentationType:
    ValueRepresentation: Representation
    _id: uuid.UUID

    def __init__(self, ValueRepresentation):
        self.ValueRepresentation = ValueRepresentation
        self._id = uuid.uuid4()

    def to_rdf(self):
        g = Graph()
        valuerep = URIRef(f"http://snds.org/{self._id}")
        g.add((valuerep, RDF.type, DDI.VariableRepresentation))
        g.add((valuerep, DDI.ValueRepresentation, self.ValueRepresentation.uri))
        g += self.ValueRepresentation.to_rdf()
        return g


class Variable(Versionable):
    VariableName: str
    VariableRepresentation: VariableRepresentationType

    def __init__(self, ID, Version, Agency, VariableName) -> None:
        super().__init__(ID, Version, Agency)
        self.VariableName = VariableName

    # static def from_snds_variable -> new Variable instance ???

    def add_representation_from_snds_variable(self, svar: SNDSVariable):
        self.VariableRepresentation = VariableRepresentationType(
            Representation.from_snds_variable(svar)
        )

    def to_rdf(self) -> Graph:
        g = Graph()
        var = URIRef(f"http://snds.org/{self.ID}")
        vrep = URIRef(f"http://snds.org/{self.VariableRepresentation._id}")
        g.add((var, RDF.type, DDI.Variable))
        g.add((var, DDI.VariableName, Literal(self.VariableName)))
        g.add((var, DDI.VariableRepresentation, vrep))
        g += self.VariableRepresentation.to_rdf()
        return g

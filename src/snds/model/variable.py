from typing import Annotated
import uuid
from annotated_types import Ge
from rdflib.term import Literal
from snds.model.base import Base, DDI
from rdflib import Graph, URIRef, RDF

from snds.model.snds import SNDSVariable

PositiveInt = Annotated[int, Ge(0)]


class Representation:
    """Super class for various representations.
    Not used directly but provides a method to return the correct implementation."""

    _id: uuid.UUID
    _ref: URIRef

    @staticmethod
    def from_snds_variable(variable: SNDSVariable):
        """Return the right `Representation`subclass from a SNDS variable type."""
        match variable["type"]:
            case "string":
                return TextRepresentationBase()
            case _:
                return TextRepresentationBase()

    @property
    def id(self):
        return self._id

    @property
    def uriref(self):
        return self._ref

    def to_rdf(self) -> Graph:
        return Graph()


class TextRepresentationBase(Representation):
    """Text representation, see https://ddialliance.github.io/ddimodel-web/DDI-L-3.3/composite-types/TextRepresentationBaseType/"""

    MaxLength: PositiveInt
    MinLength: PositiveInt

    def __init__(self) -> None:
        self._id = uuid.uuid4()
        self._ref = URIRef(f"http://snds.org/{self._id}")

    def to_rdf(self):
        g = Graph()
        trep = URIRef(f"http://snds.org/{self._id}")
        g.add((trep, RDF.type, DDI.TextRepresentation))
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
        g.add((valuerep, DDI.ValueRepresentation, self.ValueRepresentation.uriref))
        g += self.ValueRepresentation.to_rdf()
        return g


class Variable(Base):
    VariableName: str
    VariableRepresentation: VariableRepresentationType

    def __init__(self, ID, Version, Agency, VariableName) -> None:
        super().__init__(ID, Version, Agency)
        self.VariableName = VariableName

    # static def from_snds_variable ???

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

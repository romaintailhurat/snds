import dataclasses
from snds.model.base import Base, DDI_NAMESPACE
from rdflib import Graph, URIRef,RDF


@dataclasses.dataclass
class Variable(Base):
    VariableName: str

    def __init__(self, ID, Version, Agency) -> None:
        super().__init__(ID, Version, Agency)

    def to_ld(self):
        compound_id = self.VariableName + self.ID
        return {
            "@id": f"http://ddi-alliance/snds/{compound_id}/",
            "ddi:id": self.ID,
            "ddi:agency": self.Agency,
            "ddi:version": self.Version,
            "ddi:urn": self.URN,
        }

    def to_rdf(self):
        g = Graph()
        var = URIRef(f"http://snds.org/{self.ID}")
        variable_uri = URIRef(f"{DDI_NAMESPACE}Variable")
        g.add((var, RDF.type, variable_uri))
        return g

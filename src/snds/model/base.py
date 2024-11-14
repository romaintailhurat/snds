from rdflib import Namespace

DDI = Namespace("http://rdf-vocabulary.ddialliance.org/lifecycle#")


class Base:
    """This implements the Versionable trait of DDI L elements."""

    ID: str
    Version: str
    Agency: str
    URN: str | None

    def __init__(self, ID, Version, Agency) -> None:
        # TODO provide default when None for every parameter.
        self.ID = ID
        self.Version = Version
        self.Agency = Agency
        self.URN = f"urn:ddi:{self.Agency}:{self.Version}:{self.ID}"

    def to_rdf(self):
        raise NotImplementedError(
            f"Can't directly produce a graph from {self.__class__.__qualname__}"
        )

from rdflib import Namespace, URIRef
import uuid

DDI = Namespace("http://rdf-vocabulary.ddialliance.org/lifecycle#")
SNDS = Namespace("http://snds.org/")

class URIIdentifiable():
    _id: uuid.UUID
    _uri: URIRef

    def __init__(self) -> None:
        self._id = uuid.uuid4()

    @property
    def id(self):
        return self._id

    @property
    def uri(self):
        return self._uri

class Versionable:
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

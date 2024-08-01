DDI_NAMESPACE = "http://rdf-vocabulary.ddialliance.org/lifecycle#"

class Base:
    """This implements the Versionable trait of DDI L elements."""

    ID: str
    Version: str
    Agency: str
    URN: str | None

    def __init__(self, ID, Version, Agency) -> None:
        self.ID = ID
        self.Version = Version
        self.Agency = Agency
        self.URN = f"urn:ddi:{self.Agency}:{self.Version}:{self.ID}"

    def to_ld(self):
        raise NotImplementedError("Can't be directly serialized;")

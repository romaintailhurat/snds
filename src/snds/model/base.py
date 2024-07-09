import dataclasses


@dataclasses.dataclass
class Base:
    ID: str
    Version: str
    Agency: str
    URN: str | None

    # TODO use a constructor to have a proper URN from the start ?
    def get_urn(self) -> str:
        if self.URN is None:
            return f"urn:ddi:{self.Agency}:{self.Version}:{self.ID}"
        else:
            return self.URN

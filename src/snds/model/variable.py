import dataclasses
from snds.model.base import Base


@dataclasses.dataclass
class Variable(Base):
    VariableName: str

    def to_ld(self):
        compound_id = self.VariableName + self.ID
        return {
            "@id": f"http://ddi-alliance/snds/{compound_id}/",
            "ddi:id": self.ID,
            "ddi:agency": self.Agency,
            "ddi:version": self.Version,
            "ddi:urn": self.get_urn(),
        }

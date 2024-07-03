import json
import dataclasses
from pyld import jsonld
import pprint
import uuid

# pydantic -> json pseudo ddi

# ---- Model
@dataclasses.dataclass
class Base():
    ID: str
    Version: str
    Agency: str
    URN: str

@dataclasses.dataclass
class VariableRepresentation:
    Representation: object


@dataclasses.dataclass
class NumericRepresentation:
    pass


@dataclasses.dataclass
class TextRepresentation:
    pass


@dataclasses.dataclass
class CodeRepresentation:
    CodeListReference: str


@dataclasses.dataclass
class TodoRepresentation:
    pass


@dataclasses.dataclass
class Variable(Base):
    VariableName: str
    Description: str
    VariableRepresentation: VariableRepresentation

    def to_ld(self):
        return {"ddi:VariableName": self.VariableName, "ddi:URN": self.URN}

# ---- Fns


def infer_representation(type: str):
    match type:
        case "integer":
            return NumericRepresentation()
        case "string":
            return TextRepresentation()
        case "IR_AMA_V":
            return CodeRepresentation(CodeListReference="IR_AMA_V_URN_TODO")
        case _:
            return TodoRepresentation()


def pseudo_ddi(data):
    in_vars = data["fields"]
    out_vars = []
    for v in in_vars:
        type = v["nomenclature"] if v["nomenclature"] != "-" else v["type"]
        rep = infer_representation(type)
        identifier = uuid.uuid4()
        var = Variable(
            ID=str(identifier),
            Version="1",
            Agency="eu.casd",
            URN=f"uri:ddi:eu.casd:{str(identifier)}:1",
            VariableName=v["name"],
            Description=v["description"],
            VariableRepresentation=VariableRepresentation(Representation=rep),
        )
        out_vars.append(var)
    return out_vars

# ---- Run

with open("./schemas/ER_PRS_F.json") as f:
    data = json.load(f)
    vars = pseudo_ddi(data)
    context = {
        "ddi": "http://rdf-vocabulary.ddialliance.org/lifecycle"
    }

    res_vars = []
    for thing in vars[0:10]:
        var_obj = {"ddi:Variable": thing.to_ld()}
        res_vars.append(var_obj)

    doc = {"ddi:variables": res_vars}
    res = jsonld.compact(doc, context)
    with open("prs.json", "w") as out:
        json.dump(res, out, indent=2)

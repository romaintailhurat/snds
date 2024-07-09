import json
import dataclasses
from pyld import jsonld
import pprint
import uuid
import pathlib
import glob
import os

# ---- Model


@dataclasses.dataclass
class Base:
    ID: str
    Version: str
    Agency: str
    URN: str


@dataclasses.dataclass
class VariableRepresentation(Base):
    Representation: object


@dataclasses.dataclass
class NumericRepresentation(Base):
    NumberRange: int

    def to_ld(self):
        return {"ddi:NumberRange": self.NumberRange, "ddi:URN": self.URN}


@dataclasses.dataclass
class TextRepresentation(Base):
    MaxLength: int

    def to_ld(self):
        return {"ddi:MaxLength": self.MaxLength, "ddi:URN": self.URN}


@dataclasses.dataclass
class CodeRepresentation(Base):
    CodeListReference: str

    def to_ld(self):
        return {"ddi:CodeListReference": self.CodeListReference, "ddi:URN": self.URN}


@dataclasses.dataclass
class DateTimeRepresentation(Base):
    DateFieldFormat: str
    Range: int

    def to_ld(self):
        return {
            "ddi:DateFieldFormat": self.DateFieldFormat,
            "ddi:Range": self.Range,
            "ddi:URN": self.URN,
        }


@dataclasses.dataclass
class AccessRestrictionDate(Base):
    StartDate: int
    EndDate: int

    def to_ld(self):
        return {
            "ddi:StartDate": self.StartDate,
            "ddi:EndDate": self.EndDate,
            "ddi:URN": self.URN,
        }


@dataclasses.dataclass
class Variable(Base):
    VariableName: str
    Description: str
    VariableRepresentation: VariableRepresentation
    ValidityDates: AccessRestrictionDate
    belongsTo: str

    def to_ld(self):
        return {
            "ddi:VariableName": self.VariableName,
            "ddi:URN": self.URN,
            "ddi:VariableRepresentation": self.VariableRepresentation.URN,
            "ddi:ValidityDates": self.ValidityDates.URN,
            "ddi:belongsTo": self.belongsTo,
        }


def get_representation(var):
    identifier = uuid.uuid4()

    type = var["type"]
    match type:
        case "integer":
            rep = NumericRepresentation(
                ID=str(identifier),
                Version="1",
                Agency="eu.casd",
                URN=f"uri:ddi:eu.casd:{str(identifier)}:1",
                NumberRange=var["length"],
            )
        case "string":
            rep = TextRepresentation(
                ID=str(identifier),
                Version="1",
                Agency="eu.casd",
                URN=f"uri:ddi:eu.casd:{str(identifier)}:1",
                MaxLength=var["length"],
            )
        case "date":
            rep = DateTimeRepresentation(
                ID=str(identifier),
                Version="1",
                Agency="eu.casd",
                URN=f"uri:ddi:eu.casd:{str(identifier)}:1",
                DateFieldFormat=var["format"],
                Range=var["length"],
            )
        case "number":
            rep = NumericRepresentation(
                ID=str(identifier),
                Version="1",
                Agency="eu.casd",
                URN=f"uri:ddi:eu.casd:{str(identifier)}:1",
                NumberRange=var["length"],
            )
        case "year":
            rep = DateTimeRepresentation(
                ID=str(identifier),
                Version="1",
                Agency="eu.casd",
                URN=f"uri:ddi:eu.casd:{str(identifier)}:1",
                DateFieldFormat=var["format"],
                Range=var["length"],
            )
        case "yearmonth":
            rep = DateTimeRepresentation(
                ID=str(identifier),
                Version="1",
                Agency="eu.casd",
                URN=f"uri:ddi:eu.casd:{str(identifier)}:1",
                DateFieldFormat=var["format"],
                Range=var["length"],
            )
        case _:
            pass
    # if var["nomenclature"] != "-":
    #    rep = CodeRepresentation(ID=str(identifier), Version="1", Agency="eu.casd", CodeListReference="IR_AMA_V_URN_TODO", URN=f"uri:ddi:eu.casd:{str(identifier)}:1")

    return rep


def generate_variables(data, table_name):
    in_vars = data["fields"]
    out_vars, out_reps, out_dates = [], [], []
    for v in in_vars:
        rep = get_representation(v)
        identifier, id_date, id_rep = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
        validityDates = AccessRestrictionDate(
            ID=id_date,
            Version="1",
            Agency="eu.casd",
            URN=f"uri:ddi:eu.casd:{id_date}:1",
            StartDate=v["dateCreated"],
            EndDate=v["dateDeleted"],
        )
        representation = VariableRepresentation(
            ID=id_rep,
            Version="1",
            Agency="eu.casd",
            URN=f"uri:ddi:eu.casd:{id_rep}:1",
            Representation=rep,
        )

        var = Variable(
            ID=str(identifier),
            Version="1",
            Agency="eu.casd",
            URN="http://ddi-alliance/snds/" + table_name + "/" + v["name"],
            belongsTo=table_name,
            VariableName=v["name"],
            Description=v["description"],
            VariableRepresentation=representation,
            ValidityDates=validityDates,
        )
        out_vars.append(var)
        out_reps.append(representation)
        out_dates.append(validityDates)

    return out_vars, out_reps, out_dates


def get_alias_table_name(table_name):
    match table_name:
        case "ER_PHA_F":
            return "DCIR_PHA"
        case "ER_PRS_F":
            return "DCIR_PRS"
        case "ER_BIO_F":
            return "DCIR_BIO"
        case "ER_CAM_F":
            return "DCIR_CAM"
        case _:
            return table_name


def treat_table(tableJson):
    table_name = pathlib.PurePath(tableJson).stem
    table_name = get_alias_table_name(table_name)
    with open(tableJson) as f:
        data = json.load(f)
        vars, reps, dates = generate_variables(data, table_name)
        context = {"ddi": "http://rdf-vocabulary.ddialliance.org/lifecycle"}

        res_vars = []
        for thing in vars:
            var_obj = {"ddi:Variable": thing.to_ld()}
            res_vars.append(var_obj)

        res_reps = []
        for thing in reps:
            rep_obj = {"ddi:Representation": thing.Representation.to_ld()}
            res_reps.append(rep_obj)

        res_dates = []
        for thing in dates:
            date_obj = {"ddi:AccessRestrictionDate": thing.to_ld()}
            res_dates.append(date_obj)

        doc = {
            "ddi:variables": res_vars,
            "ddi:representations": res_reps,
            "ddi:dates": res_dates,
        }
        res = jsonld.compact(doc, context)
        with open("./json/" + table_name + ".json", "w") as out:
            json.dump(res, out, indent=2)


for file_path in glob.glob("./schemas/*/*.json", recursive=True):
    treat_table(tableJson=file_path)

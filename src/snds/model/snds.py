"""This module contains classes in the form of `TypedDict` for representing SNDS schemas."""

from typing import TypedDict


class SNDSVariable(TypedDict):
    """One variable or column in a dataset schema."""

    name: str
    description: str
    type: str
    nomenclature: str
    length: str
    format: str
    dateCreated: str
    dateDeleted: str
    dateMissing: str
    observation: str
    regle_gestion: str
    type_oracle: str


class History(TypedDict):
    """History of a file."""

    dateCreated: str
    dateDeleted: str
    dateMissing: list[str]


class Schema(TypedDict):
    """Represent a schema file (e.g. https://gitlab.com/healthdatahub/applications-du-hdh/schema-snds/-/blob/master/schemas/DCIR/ER_ANO_F.json?ref_type=heads)"""

    fields: list[SNDSVariable]
    missingValues: list[str]
    name: str
    title: str
    produit: str
    history: History
    champ: str
    observation: str
    primaryKey: list[str]

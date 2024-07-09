from snds.model.base import Base
from snds.model.variable import Variable

import pyld
import json

base = Base(ID="123456789", Version="1", Agency="eu.casd", URN="truc")

test_var = Variable(
    ID="123456789", Version="1", Agency="eu.casd", URN="truc", VariableName="TEST_VAR"
)

context = {"ddi": "http://rdf-vocabulary.ddialliance.org/lifecycle"}

result = pyld.jsonld.compact(test_var.to_ld(), context)
print(json.dumps(result, indent=2))

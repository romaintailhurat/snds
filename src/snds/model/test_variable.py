from snds.model.variable import Variable

import pytest


@pytest.fixture
def test_variable_without_urn():
    return Variable(
        ID="123456789",
        Agency="org.example",
        Version="1",
        VariableName="TEST_VAR",
    )


def test_get_urn_from_a_test_variable_without_urn(test_variable_without_urn: Variable):
    urn = test_variable_without_urn.URN
    assert urn is not None
    prefix, domain, agency, version, var_id = urn.split(":")
    assert prefix == "urn"
    assert domain == "ddi"

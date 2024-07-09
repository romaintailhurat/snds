from snds.model.variable import Variable

import pytest


@pytest.fixture
def test_variable_without_urn():
    return Variable(
        ID="123456789",
        Agency="org.example",
        Version="1",
        URN=None,
        VariableName="TEST_VAR",
    )


def test_variable_id_is_there(test_variable_without_urn):
    var_ld = test_variable_without_urn.to_ld()
    assert "@id" in var_ld.keys()


def test_get_urn_from_a_test_variable_without_urn(test_variable_without_urn: Variable):
    urn = test_variable_without_urn.get_urn()
    assert urn is not None
    prefix, domain, agency, version, var_id = urn.split(":")
    assert prefix == "urn"
    assert domain == "ddi"

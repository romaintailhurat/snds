from snds.model.variable import Variable


def test_variable_id_is_there():
    var = Variable(
        ID="123456789",
        Agency="org.example",
        Version="1",
        URN=None,
        VariableName="TEST_VAR",
    )
    var_ld = var.to_ld()
    assert "@id" in var_ld.keys()

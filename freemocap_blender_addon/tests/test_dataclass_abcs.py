from typing import List

import pytest

from freemocap_blender_addon.models.skeleton.abstract_base_classes import NamedDataclassABC, CompoundDataclassABC, \
    SimpleDataclassABC


class ExampleNamedDataclass(NamedDataclassABC):
    pass


class ExampleNamedDataclass2(NamedDataclassABC):
    pass


class ExampleNamedDataclass3(NamedDataclassABC):
    pass


class ExampleSimpleDataclass(SimpleDataclassABC):
    parent: NamedDataclassABC
    child: NamedDataclassABC


class ExampleCompoundDataclass(CompoundDataclassABC):
    parent: NamedDataclassABC
    children: List[NamedDataclassABC]


@pytest.fixture
def example_named_instance_fixture() -> ExampleNamedDataclass:
    instance = ExampleNamedDataclass()
    assert instance.name == "ExampleNamedDataclass"
    assert isinstance(instance, NamedDataclassABC)
    assert isinstance(instance, ExampleNamedDataclass)
    yield instance


@pytest.fixture
def example_named_instance2_fixture() -> ExampleNamedDataclass2:
    instance = ExampleNamedDataclass2()
    assert instance.name == "ExampleNamedDataclass2"
    assert isinstance(instance, NamedDataclassABC)
    assert isinstance(instance, ExampleNamedDataclass2)
    yield instance


@pytest.fixture
def example_named_instance3_fixture() -> ExampleNamedDataclass3:
    instance = ExampleNamedDataclass3()
    assert instance.name == "ExampleNamedDataclass3"
    assert isinstance(instance, NamedDataclassABC)
    assert isinstance(instance, ExampleNamedDataclass3)
    yield instance


@pytest.fixture
def simple_instance(example_named_instance_fixture: ExampleNamedDataclass,
                    example_named_instance2_fixture: ExampleNamedDataclass2) -> SimpleDataclassABC:
    return ExampleSimpleDataclass(parent=example_named_instance_fixture, child=example_named_instance2_fixture)


@pytest.fixture
def compound_instance(example_named_instance_fixture: ExampleNamedDataclass,
                      example_named_instance2_fixture: ExampleNamedDataclass2,
                      example_named_instance3_fixture: ExampleNamedDataclass3
                      ) -> CompoundDataclassABC:
    return ExampleCompoundDataclass(parent=example_named_instance_fixture, children=[example_named_instance2_fixture,
                                                                                     example_named_instance3_fixture])


def test_named_dataclass(example_named_instance_fixture: NamedDataclassABC) -> None:
    """
    Test attributes and methods of NamedDataclassABC
    """
    assert example_named_instance_fixture.name == ExampleNamedDataclass.__name__
    assert example_named_instance_fixture.name == ExampleNamedDataclass.__name__
    assert hash(example_named_instance_fixture) == hash(example_named_instance_fixture)
    assert str(example_named_instance_fixture) == ExampleNamedDataclass.__name__


def test_simple_dataclass(simple_instance: SimpleDataclassABC) -> None:
    """
    Test attributes and methods of SimpleDataclassABC
    """
    assert simple_instance.name == "ExampleSimpleDataclass"
    assert str(
        simple_instance) == f"ExampleSimpleDataclass\n\tParent: {simple_instance.parent}\n\tChild: {simple_instance.child}"


def test_compound_dataclass(compound_instance: ExampleCompoundDataclass) -> None:
    """
    Test attributes and methods of CompoundDataclassABC
    """
    assert compound_instance.name == "ExampleCompoundDataclass"
    assert "Parent" in str(compound_instance)
    with pytest.raises(NotImplementedError):
        assert compound_instance.positive_x
    with pytest.raises(NotImplementedError):
        assert compound_instance.approximate_positive_y


def test_simple_dataclass_post_init_check_parent_child_not_equal(example_named_instance_fixture: ExampleNamedDataclass,
                                                                 example_named_instance2_fixture: ExampleNamedDataclass2) -> None:
    """
    Test post-init validation of SimpleDataclassABC
    """
    with pytest.raises(ValueError):
        ExampleSimpleDataclass(parent=example_named_instance_fixture, child=example_named_instance_fixture)


def test_compound_dataclass_post_init(example_named_instance_fixture: NamedDataclassABC) -> None:
    """
    Test post-init validation of CompoundDataclassABC
    """
    child1 = ExampleNamedDataclass()
    child2 = ExampleNamedDataclass()
    with pytest.raises(ValueError):
        ExampleCompoundDataclass(parent=example_named_instance_fixture, children=[child1, child1])
    with pytest.raises(ValueError):
        ExampleCompoundDataclass(parent=example_named_instance_fixture, children=[child1])



def test_compound_dataclass_no_duplicate_children(example_named_instance_fixture: NamedDataclassABC,
                                                  example_named_instance2_fixture: NamedDataclassABC) -> None:
    with pytest.raises(ValueError):
        ExampleCompoundDataclass(parent=example_named_instance_fixture, children=[example_named_instance_fixture,
                                                                                  example_named_instance2_fixture])
    with pytest.raises(ValueError):
        ExampleCompoundDataclass(parent=example_named_instance_fixture, children=[example_named_instance2_fixture,
                                                                                  example_named_instance2_fixture])


def test_compound_dataclass_not_enough_children(example_named_instance_fixture: NamedDataclassABC,
                                                example_named_instance2_fixture: NamedDataclassABC) -> None:
    with pytest.raises(ValueError):
        ExampleCompoundDataclass(parent=example_named_instance_fixture, children=[example_named_instance2_fixture])

def test_get_child(compound_instance: CompoundDataclassABC) -> None:
    """
    Test get_child method of CompoundDataclassABC
    """
    child = compound_instance.children[0]
    assert compound_instance.get_child(child) == child
    with pytest.raises(ValueError):
        compound_instance.get_child(ExampleNamedDataclass())

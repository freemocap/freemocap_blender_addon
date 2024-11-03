from dataclasses import dataclass
from typing import List, Dict

import pytest

from skellyblender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass, TypeHintError, \
    enforce_type_hints


@dataclass
class SampleDataClass(TypeSafeDataclass):
    number: int
    text: str
    data_list: List[int]
    data_dict: Dict[str, int]


@dataclass
class NestedDataClass(TypeSafeDataclass):
    nested: SampleDataClass
    extra_field: float


@dataclass
class DeeplyNestedDataClass(TypeSafeDataclass):
    deeply_nested: NestedDataClass
    additional_field: bool


@dataclass
class InheritedDataClass(SampleDataClass):
    extra_inherited_field: float


def test_correct_input():
    """
    Test SampleDataClass with correct input.
    """
    instance = SampleDataClass(number=1, text="test", data_list=[1, 2, 3], data_dict={"key": 1})
    enforce_type_hints(instance)


def test_incorrect_number_type():
    """
    Test SampleDataClass with incorrect type for 'number' field.
    """
    with pytest.raises(TypeHintError):
        instance = SampleDataClass(number="wrong_type", text="test", data_list=[1, 2, 3], data_dict={"key": 1})


def test_incorrect_list_type():
    """
    Test SampleDataClass with incorrect type for 'data_list' field.
    """
    with pytest.raises(TypeHintError):
        instance = SampleDataClass(number=1, text="test", data_list="not_a_list", data_dict={"key": 1})


def test_incorrect_dict_type():
    """
    Test SampleDataClass with incorrect type for 'data_dict' field.
    """
    with pytest.raises(TypeHintError):
        instance = SampleDataClass(number=1, text="test", data_list=[1, 2, 3], data_dict={"key": "not_an_int"})


def test_empty_list_dict():
    """
    Test SampleDataClass with empty list and dict.
    """
    instance = SampleDataClass(number=1, text="test", data_list=[], data_dict={})
    enforce_type_hints(instance)


def test_large_numbers():
    """
    Test SampleDataClass with large numbers.
    """
    instance = SampleDataClass(
        number=10 ** 18,
        text="test",
        data_list=[i for i in range(1000)],
        data_dict={f"key{i}": i for i in range(1000)}
    )
    enforce_type_hints(instance)


def test_nested_data_class():
    """
    Test NestedDataClass with correct input.
    """
    nested_instance = SampleDataClass(number=1, text="test", data_list=[1, 2, 3], data_dict={"key": 1})
    instance = NestedDataClass(nested=nested_instance, extra_field=1.0)
    enforce_type_hints(instance)


def test_deeply_nested_data_class():
    """
    Test DeeplyNestedDataClass with correct input.
    """
    nested_instance = SampleDataClass(number=1, text="test", data_list=[1, 2, 3], data_dict={"key": 1})
    deeply_nested_instance = NestedDataClass(nested=nested_instance, extra_field=1.0)
    instance = DeeplyNestedDataClass(deeply_nested=deeply_nested_instance, additional_field=True)
    enforce_type_hints(instance)


def test_inherited_data_class():
    """
    Test InheritedDataClass with correct input.
    """
    instance = InheritedDataClass(number=1, text="test", data_list=[1, 2, 3], data_dict={"key": 1},
                                  extra_inherited_field=1.0)
    enforce_type_hints(instance)


def test_incorrect_nested_data_class():
    """
    Test NestedDataClass with incorrect type in nested SampleDataClass.
    """
    with pytest.raises(TypeHintError):
        nested_instance = SampleDataClass(number="wrong_type", text="test", data_list=[1, 2, 3], data_dict={"key": 1})
        instance = NestedDataClass(nested=nested_instance, extra_field=1.0)
        enforce_type_hints(instance)


def test_incorrect_deeply_nested_data_class():
    """
    Test DeeplyNestedDataClass with incorrect type in deeply nested SampleDataClass.
    """
    with pytest.raises(TypeHintError):
        nested_instance = SampleDataClass(number=1, text="test", data_list=[1, 2, 3], data_dict={"key": "not_an_int"})
        deeply_nested_instance = NestedDataClass(nested=nested_instance, extra_field=1.0)
        instance = DeeplyNestedDataClass(deeply_nested=deeply_nested_instance, additional_field=True)
        enforce_type_hints(instance)

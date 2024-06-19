# import numpy as np
#
# from freemocap_blender_addon.utilities.named_ndarray import NamedNdarray
#
#
# def test_named_ndarray_creation(filled_array_fixture, dtype_fixture):
#     """
#     Test the creation of NamedNdarray instances
#     """
#     array = NamedNdarray(filled_array_fixture, "test_array")
#     assert isinstance(array, NamedNdarray)
#     assert array.name == "test_array"
#     assert array.dtype == dtype_fixture
#     assert array.shape == filled_array_fixture.shape
#
#
# def test_named_ndarray_dimension_names(filled_array_fixture):
#     """
#     Test the assignment and retrieval of dimension names
#     """
#     dimension_names = [f"dim_{i}" for i in range(filled_array_fixture.ndim)]
#     if len(set(dimension_names)) > filled_array_fixture.size:
#         # If the number of unique dimension names exceeds the number of dimensions, the creation should fail
#         try:
#             array = NamedNdarray(filled_array_fixture, "test_array", dimension_names)
#             assert False, "Dimension names should not be more than the number of dimensions"
#         except ValueError:
#             return
#     array = NamedNdarray(filled_array_fixture, "test_array", dimension_names)
#     assert array.dimension_names == dimension_names
#
#     # Testing default dimension names
#     default_array = NamedNdarray(filled_array_fixture, "test_array")
#     assert default_array.dimension_names == [f"dimension_{i}" for i in range(filled_array_fixture.ndim)]
#
#
# def test_named_ndarray_getitem(filled_array_fixture):
#     """
#     Test the __getitem__ method with both integer and named indexing
#     """
#     dimension_names = [f"dim_{i}" for i in range(filled_array_fixture.ndim)]
#     if len(set(dimension_names)) > filled_array_fixture.size:
#         # If the number of unique dimension names exceeds the number of dimensions, the creation should fail
#         try:
#             array = NamedNdarray(filled_array_fixture, "test_array", dimension_names)
#             assert False, "Dimension names should not be more than the number of dimensions"
#         except ValueError:
#             return
#     array = NamedNdarray(filled_array_fixture, "test_array", dimension_names)
#
#     # Test integer indexing
#     result = array[0]
#     assert result.dtype == filled_array_fixture.dtype
#
#     # Test named indexing
#     if filled_array_fixture.ndim > 1:
#         result = array["dim_0"]
#         assert isinstance(result, NamedNdarray) or isinstance(result, np.ndarray)
#
#
# def test_named_ndarray_getattr(filled_array_fixture):
#     """
#     Test the __getattr__ method for retrieving dimensions by name
#     """
#     dimension_names = [f"dim_{i}" for i in range(filled_array_fixture.ndim)]
#     if len(set(dimension_names)) > filled_array_fixture.size:
#         # If the number of unique dimension names exceeds the number of dimensions, the creation should fail
#         try:
#             array = NamedNdarray(filled_array_fixture, "test_array", dimension_names)
#             assert False, "Dimension names should not be more than the number of dimensions"
#         except ValueError:
#             return
#     array = NamedNdarray(filled_array_fixture, "test_array", dimension_names)
#
#     for dim_name in dimension_names:
#         result = getattr(array, dim_name)
#         dimension_index = array.dimension_names.index(dim_name)
#         if result is None:
#             f=9
#         assert result.dtype == filled_array_fixture.dtype
#         # TODO - more checks that the shapes and slicing methods work as they should
#
#
# def test_named_ndarray_str_repr(filled_array_fixture):
#     """
#     Test the __str__ and __repr__ methods
#     """
#     array = NamedNdarray(filled_array_fixture, "test_array")
#     str_repr = str(array)
#     repr_repr = repr(array)
#
#     assert "NamedNumpyArray" in str_repr
#     assert "NamedNumpyArray" in repr_repr
#
#
# def test_named_ndarray_dir(filled_array_fixture):
#     """
#     Test the __dir__ method to ensure dimension names are included
#     """
#     dimension_names = [f"dim_{i}" for i in range(filled_array_fixture.ndim)]
#     array = NamedNdarray(filled_array_fixture, "test_array", dimension_names)
#     dir_list = dir(array)
#
#     for dim_name in dimension_names:
#         assert dim_name in dir_list

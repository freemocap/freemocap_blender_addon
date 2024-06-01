# import pytest
#
# from freemocap_blender_addon.experiments.fixed_size_bytes_str import DEFAULT_FIXED_SIZE, FixedSizeBytes, FixedSizeStr, \
#     DEFAULT_FIXED_SIZE_STRING_ENCODING
#
#
# @pytest.fixture(params=[8, 16, 24, DEFAULT_FIXED_SIZE])
# def bytes_size_fixture(request) -> int:
#     return (request.param)
#
# @pytest.fixture(params=[DEFAULT_FIXED_SIZE + 1, DEFAULT_FIXED_SIZE * 2, DEFAULT_FIXED_SIZE * 10])
# def too_big_bytes_size_fixture(request) -> int:
#     return request.param
#
#
# def test_fixed_size_bytes_creation(bytes_size_fixture: int):
#     content = b'1234'
#     fixed_size = bytes_size_fixture
#     fsb = FixedSizeBytes(content, fixed_size)
#     assert isinstance(fsb, FixedSizeBytes)
#     assert fsb.fixed_size == fixed_size
#
#
# def test_fixed_size_bytes_to_fixed_size(bytes_size_fixture: int):
#     content = b'1234'
#     fsb = FixedSizeBytes(content=content, fixed_size=bytes_size_fixture)
#     fixed_size_bytes = fsb.to_fixed_size()
#     assert len(fixed_size_bytes) == bytes_size_fixture
#     assert fixed_size_bytes.startswith(content)
#
#
# def test_fixed_size_bytes_from_fixed_size(bytes_size_fixture: int):
#     content = b'1234'
#     fsb = FixedSizeBytes(content=content, fixed_size=bytes_size_fixture)
#     fixed_size_bytes = fsb.to_fixed_size()
#     fsb_restored = FixedSizeBytes.from_fixed_size(fixed_size_bytes, bytes_size_fixture)
#     assert fsb_restored== fsb
#
#
# def test_fixed_size_str_creation(bytes_size_fixture: int):
#     content = 'test'
#     fss = FixedSizeStr(content=content, fixed_size=bytes_size_fixture)
#     assert isinstance(fss, FixedSizeStr)
#     assert fss.fixed_size == bytes_size_fixture
#
#
# def test_fixed_size_str_to_fixed_size_bytes(bytes_size_fixture: int):
#     content = 'test'
#     fss = FixedSizeStr(content=content, fixed_size=bytes_size_fixture)
#     fixed_size_bytes = fss.to_fixed_size_bytes()
#     assert len(fixed_size_bytes) == bytes_size_fixture
#     assert fixed_size_bytes.startswith(content.encode(DEFAULT_FIXED_SIZE_STRING_ENCODING))
#
#
# def test_fixed_size_str_from_fixed_size_bytes(bytes_size_fixture: int):
#     content = 'test'
#     fss = FixedSizeStr(content=content, fixed_size=bytes_size_fixture)
#     fixed_size_bytes = fss.to_fixed_size_bytes()
#     fss_restored = FixedSizeStr.from_fixed_size_bytes(fixed_size_element=fixed_size_bytes, fixed_size=bytes_size_fixture)
#     assert fss_restored == fss

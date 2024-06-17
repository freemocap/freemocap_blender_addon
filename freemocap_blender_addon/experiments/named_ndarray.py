from typing import List, Any, Tuple

import numpy as np

DimensionName = str
DimensionNames = List[DimensionName]
DimensionIndex = int
ArrayIndex = Tuple[DimensionIndex, ...]


class NamedNdarray(np.ndarray):
    name: str
    dimension_names: DimensionNames

    def __new__(cls,
                data: Any,
                name: str,
                dimension_names: List[str] = None):
        obj = np.asarray(data).view(cls)
        obj.name = name
        if dimension_names:
            if len(dimension_names) != obj.ndim:
                raise ValueError(f"Dimension names {dimension_names} do not match shape {obj.shape}")
            if len(set(dimension_names)) != len(dimension_names):
                raise ValueError(f"Dimension names {dimension_names} contain duplicates")
            if len(dimension_names) > obj.size:
                raise ValueError(f"Dimension names {dimension_names} are more than the number of dimensions {obj.size}")
            obj.dimension_names = dimension_names
        else:
            obj.dimension_names = [f"dimension_{i}" for i in range(obj.ndim)]
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.name = getattr(obj, 'name', None)
        self.dimension_names = getattr(obj, 'dimension_names', [f"dim_{i}" for i in range(self.ndim)])

    def __getitem__(self, key: Any):
        if isinstance(key, tuple) and not isinstance(key, str):
            key = tuple(self.dimension_names.index(k) if isinstance(k, str) else k for k in key)
        elif isinstance(key, DimensionName):
            key = self.dimension_names.index(key)
        result = super().__getitem__(key)
        if isinstance(result, NamedNdarray):
            if isinstance(key, tuple):
                remaining_dims = [self.dimension_names[i] for i in range(len(self.dimension_names)) if i not in key]
                result.dimension_names = remaining_dims
            else:
                result.dimension_names = self.dimension_names[1:]
        return result

    def __getattr__(self, item):
        try:
            if item in self.dimension_names:
                index = self.dimension_names.index(item)
                return self.take(indices=index, axis=0)
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")
        except Exception as e:
            f = 9

    def __dir__(self):
        return list(super().__dir__()) + self.dimension_names

    def __str__(self):
        return f"NamedNumpyArray(name={self.name}, shape={self.shape}, dimension_names={self.dimension_names})\ndata=\n{np.array2string(self, threshold=5)}"

    def __repr__(self):
        return (f"NamedNumpyArray(name={self.name!r}, shape={self.shape!r}, "
                f"dimension_names={self.dimension_names!r}, "
                f"data={np.array2string(self, threshold=5)})")


if __name__ == "__main__":
    test_data = [[1, 2, 3], [4, 5, 6]]  # shape (2, 3)
    named_array = NamedNdarray(test_data, "example_array", ["x", "y"])
    print(f"named_array.__str__: \n {named_array.__str__()}\n\n")
    print(f"named_array.__repr__: \n {named_array.__repr__()}\n\n")
    print(f"named_array.__dir__: \n {named_array.__dir__()}\n\n")
    print(f"named_array.name: \n {named_array.name}\n\n")
    print(f"named_array.dimension_names: \n {named_array.dimension_names}\n\n")
    print(f"named_array.x: \n {named_array.x}\n\n")
    print(f"named_array['x']: \n {named_array['x']}\n\n")
    print(f"named_array['x', 0]: \n {named_array['x', 0]}\n\n")

"""Tests for public API exports."""

from cfdb_models.data_models import DataType

from cfdb_vars import coord_var_defs, data_var_defs, short_name_map, time_dtype_params, var_defs


def test_var_defs_is_combined():
    assert len(var_defs) == len(coord_var_defs) + len(data_var_defs)
    for key, val in coord_var_defs.items():
        assert var_defs[key] is val
    for key, val in data_var_defs.items():
        assert var_defs[key] is val


def test_no_key_overlap():
    coord_keys = set(coord_var_defs.keys())
    data_keys = set(data_var_defs.keys())
    assert coord_keys.isdisjoint(data_keys), f'Overlapping keys: {coord_keys & data_keys}'


def test_short_name_map_values_are_valid():
    for short_name, cf_name in short_name_map.items():
        assert cf_name in var_defs, f'short_name_map[{short_name!r}] = {cf_name!r} not in var_defs'


def test_short_name_map_covers_all_vars():
    mapped_cf_names = set(short_name_map.values())
    assert mapped_cf_names == set(var_defs.keys())


def test_time_dtype_params_count():
    assert len(time_dtype_params) == 8


def test_time_dtype_params_types():
    for key, val in time_dtype_params.items():
        assert isinstance(val, DataType), f'{key} is not a DataType'
        assert val.name == key
        assert val.dtype_encoded is not None
        assert val.offset is not None

"""Tests for coordinate variable definitions."""

import msgspec
from cfdb_models.data_models import CoordVarDef

from cfdb_vars.coord_vars import coord_var_defs


def test_coord_var_count():
    assert len(coord_var_defs) == 12


def test_coord_var_types():
    for name, var_def in coord_var_defs.items():
        assert isinstance(var_def, CoordVarDef), f'{name} is not a CoordVarDef'


def test_coord_vars_have_attrs():
    for name, var_def in coord_var_defs.items():
        assert var_def.attrs is not None, f'{name} has no attrs'
        assert 'long_name' in var_def.attrs, f'{name} missing long_name'


def test_axis_present_where_expected():
    axis_vars = {'longitude': 'X', 'latitude': 'Y', 'height': 'Z', 'altitude': 'Z', 'time': 'T', 'x': 'X', 'y': 'Y', 'depth': 'Z', 'pressure': 'Z'}
    for name, expected_axis in axis_vars.items():
        assert coord_var_defs[name].attrs['axis'] == expected_axis, f'{name} has wrong axis'


def test_geometry_vars_have_axis():
    for name in ('point', 'line', 'polygon'):
        assert coord_var_defs[name].attrs['axis'] == 'XY', f'{name} should have axis XY'


def test_longitude_definition():
    lon = coord_var_defs['longitude']
    assert lon.dtype.name == 'float64'
    assert lon.dtype.precision == 6
    assert lon.dtype.dtype_encoded == 'uint32'
    assert lon.dtype.offset == -180.000001
    assert lon.dtype.fillvalue == 0
    assert lon.attrs['units'] == 'degrees_east'
    assert lon.attrs['standard_name'] == 'longitude'
    assert lon.attrs['odm2_variable_name'] == 'longitude'


def test_time_definition():
    t = coord_var_defs['time']
    assert t.dtype.name == 'datetime64[m]'
    assert t.dtype.dtype_encoded == 'int32'
    assert t.dtype.offset == -36816481
    assert t.attrs['standard_name'] == 'time'
    assert t.attrs['axis'] == 'T'
    assert 'odm2_variable_name' not in t.attrs


def test_odm2_variable_names():
    odm2_vars = {'longitude': 'longitude', 'latitude': 'latitude', 'height': 'height', 'altitude': 'altitude'}
    for name, expected_odm2 in odm2_vars.items():
        assert coord_var_defs[name].attrs['odm2_variable_name'] == expected_odm2

    no_odm2 = ('time', 'x', 'y', 'depth', 'pressure', 'point', 'line', 'polygon')
    for name in no_odm2:
        assert 'odm2_variable_name' not in coord_var_defs[name].attrs, f'{name} should not have odm2_variable_name'


def test_msgspec_roundtrip():
    for name, var_def in coord_var_defs.items():
        encoded = msgspec.json.encode(var_def)
        decoded = msgspec.json.decode(encoded, type=CoordVarDef)
        assert decoded == var_def, f'{name} roundtrip failed'

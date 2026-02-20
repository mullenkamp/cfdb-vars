"""Tests for data variable definitions."""

import msgspec
from cfdb_models.data_models import DataVarDef

from cfdb_vars.data_vars import data_var_defs


def test_data_var_count():
    assert len(data_var_defs) == 30


def test_data_var_types():
    for name, var_def in data_var_defs.items():
        assert isinstance(var_def, DataVarDef), f'{name} is not a DataVarDef'


def test_data_vars_have_attrs():
    for name, var_def in data_var_defs.items():
        assert var_def.attrs is not None, f'{name} has no attrs'
        assert 'long_name' in var_def.attrs, f'{name} missing long_name'


def test_no_axis_in_attrs():
    for name, var_def in data_var_defs.items():
        assert 'axis' not in var_def.attrs, f'{name} should not have axis in attrs'


def test_precipitation_definition():
    precip = data_var_defs['precipitation']
    assert precip.dtype.name == 'float32'
    assert precip.dtype.precision == 2
    assert precip.dtype.dtype_encoded == 'uint16'
    assert precip.dtype.offset == -1
    assert precip.dtype.fillvalue == 0
    assert precip.attrs['units'] == 'mm'
    assert precip.attrs['standard_name'] == 'precipitation_amount'
    assert precip.attrs['odm2_variable_name'] == 'precipitation'


def test_air_temperature_definition():
    air_temp = data_var_defs['air_temperature']
    assert air_temp.dtype.name == 'float32'
    assert air_temp.dtype.precision == 2
    assert air_temp.dtype.offset == -61
    assert air_temp.attrs['units'] == 'K'
    assert air_temp.attrs['standard_name'] == 'air_temperature'
    assert 'odm2_variable_name' not in air_temp.attrs


def test_odm2_variable_names():
    odm2_vars = {
        'precipitation': 'precipitation',
        'wind_speed': 'windSpeed',
        'wind_direction': 'windDirection',
        'relative_humidity': 'relativeHumidity',
        'dew_point_temperature': 'temperatureDewPoint',
        'shortwave_radiation': 'radiationIncomingShortwave',
        'longwave_radiation': 'radiationIncomingLongwave',
        'snow_depth': 'snowDepth',
        'sensible_heat_flux': 'sensibleHeatFlux',
        'albedo': 'albedo',
    }
    for name, expected_odm2 in odm2_vars.items():
        assert data_var_defs[name].attrs['odm2_variable_name'] == expected_odm2

    no_odm2 = (
        'modified_date',
        'band',
        'censor_code',
        'air_temperature',
        'u_wind',
        'v_wind',
        'soil_temperature',
        'lwe_soil_moisture',
        'surface_pressure',
        'specific_humidity',
        'mixing_ratio',
        'mslp',
        'vorticity',
        'vertical_velocity',
        'moisture_flux',
        'emissivity',
        'terrain_height',
        'potential_temperature',
        'equivalent_potential_temperature',
        'land_use_modis',
    )
    for name in no_odm2:
        assert 'odm2_variable_name' not in data_var_defs[name].attrs, f'{name} should not have odm2_variable_name'


def test_msgspec_roundtrip():
    for name, var_def in data_var_defs.items():
        encoded = msgspec.json.encode(var_def)
        decoded = msgspec.json.decode(encoded, type=DataVarDef)
        assert decoded == var_def, f'{name} roundtrip failed'

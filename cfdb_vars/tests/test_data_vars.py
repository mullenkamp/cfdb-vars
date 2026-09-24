"""Tests for data variable definitions."""

import msgspec
from cfdb_models.data_models import DataVarDef

from cfdb_vars.data_vars import data_var_defs


def test_data_var_count():
    assert len(data_var_defs) == 95


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
    # units are a length (mm), so the liquid-water-equivalent thickness; 'precipitation_amount' is kg m-2
    assert precip.attrs['standard_name'] == 'lwe_thickness_of_precipitation_amount'
    assert precip.attrs['odm2_variable_name'] == 'precipitation'


def test_air_temperature_definition():
    air_temp = data_var_defs['air_temperature']
    assert air_temp.dtype.name == 'float32'
    assert air_temp.dtype.precision == 2
    assert air_temp.dtype.offset == -61
    assert air_temp.attrs['units'] == 'K'
    assert air_temp.attrs['standard_name'] == 'air_temperature'
    assert 'odm2_variable_name' not in air_temp.attrs


def test_relative_humidity_is_a_fine_fraction():
    rh = data_var_defs['relative_humidity']
    assert rh.attrs['units'] == '1'
    assert rh.dtype.precision == 3 and rh.dtype.offset == -0.001


def test_height_floors_allow_below_sea_level():
    for name in ('terrain_height', 'geopotential_height'):
        d = data_var_defs[name].dtype
        assert d.dtype_encoded == 'uint32' and d.offset == -1001, name


def test_wind_gust_definition():
    g = data_var_defs['wind_gust']
    assert g.attrs['standard_name'] == 'wind_speed_of_gust' and g.attrs['units'] == 'm/s'


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
        'geopotential_height',
        'land_sea_mask',
        'sea_ice',
        'sea_surface_temp',
        'snow_water_equiv',
        'soil_moisture',
        'soil_layer_temp',
        'pwat',
        'vimf_u',
        'vimf_v',
        'skin_temperature',
        'snow_layer_temperature',
        'ice_surface_temperature',
        'cape',
        'snow_density',
        'snow_albedo',
        'skin_reservoir_content',
        'surface_roughness',
        'surface_roughness_heat',
        'charnock',
        'total_cloud_cover',
        'low_cloud_cover',
        'medium_cloud_cover',
        'high_cloud_cover',
        'cloud_cover',
        'total_column_water',
        'total_column_liquid_water',
        'total_column_ice_water',
        'total_column_rain_water',
        'total_column_snow_water',
        'total_column_ozone',
        'divergence',
        'potential_vorticity',
        'ozone_mixing_ratio',
        'cloud_liquid_water_content',
        'cloud_ice_water_content',
        'rain_water_content',
        'snow_water_content',
        'boundary_layer_height',
        'surface_stress_east',
        'surface_stress_north',
        'uv_albedo_direct',
        'uv_albedo_diffuse',
        'nir_albedo_direct',
        'nir_albedo_diffuse',
        'leaf_area_index_low',
        'leaf_area_index_high',
        'low_vegetation_cover',
        'high_vegetation_cover',
        'low_vegetation_type',
        'high_vegetation_type',
        'lake_cover',
        'lake_depth',
        'lake_bottom_temperature',
        'lake_total_layer_temperature',
        'lake_shape_factor',
        'lake_ice_temperature',
        'lake_ice_depth',
        'soil_type',
        'std_dev_orography',
        'std_dev_filtered_orography',
        'orography_anisotropy',
        'orography_angle',
        'orography_slope',
    )
    for name in no_odm2:
        assert 'odm2_variable_name' not in data_var_defs[name].attrs, f'{name} should not have odm2_variable_name'


def test_msgspec_roundtrip():
    for name, var_def in data_var_defs.items():
        encoded = msgspec.json.encode(var_def)
        decoded = msgspec.json.decode(encoded, type=DataVarDef)
        assert decoded == var_def, f'{name} roundtrip failed'


# (template, standard_name, canonical units in the CF standard name table v94) for the templates corrected in
# 0.2.5: each name exists in the table and its canonical units match the template's units dimensionally.
CF_CHECKED = [
    ('precipitation', 'lwe_thickness_of_precipitation_amount', 'm'),
    ('snow_water_equiv', 'surface_snow_amount', 'kg m-2'),
    ('total_column_water', 'atmosphere_mass_content_of_water', 'kg m-2'),
    ('total_column_ozone', 'atmosphere_mass_content_of_ozone', 'kg m-2'),
    ('vorticity', 'atmosphere_upward_relative_vorticity', 's-1'),
    ('equivalent_potential_temperature', 'air_equivalent_potential_temperature', 'K'),
    ('snow_density', 'surface_snow_density', 'kg m-3'),
    ('total_column_snow_water', 'atmosphere_mass_content_of_snow', 'kg m-2'),
    ('snow_water_content', 'mass_fraction_of_snow_in_air', '1'),
]


def test_cf_standard_names_corrected():
    """A length unit needs the lwe_thickness_* name, a mass/area unit the *_amount / mass_content name."""
    length = {'mm': 'm', 'm': 'm'}
    for name, standard_name, canonical in CF_CHECKED:
        attrs = data_var_defs[name].attrs
        assert attrs['standard_name'] == standard_name, name
        units = attrs['units']
        assert length.get(units, units) == canonical or (units == 'kg kg-1' and canonical == '1'), (name, units)

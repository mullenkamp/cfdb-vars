"""Tests for data variable definitions."""

import msgspec
from cfdb_models.data_models import DataVarDef

from cfdb_vars.data_vars import data_var_defs


def test_data_var_count():
    assert len(data_var_defs) == 100


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


def test_wind_direction_is_from_direction():
    """The producer (cfdb-ingest) stores the meteorological FROM direction; the label must say so (0.2.8)."""
    assert data_var_defs['wind_direction'].attrs['standard_name'] == 'wind_from_direction'


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


def test_sensible_heat_flux_range_covers_wrf_extremes():
    """Local 1-3 km WRF sensible heat flux spans -1811 .. +1028 W m-2 (535 files, 2026-09-27; the -1811 in a 1 km
    nest's first hour); below the floor cfdb stores a value as missing. uint16 at 0.1 W m-2, code 0 = fill."""
    d = data_var_defs['sensible_heat_flux'].dtype
    assert d.dtype_encoded == 'uint16' and d.precision == 1 and d.fillvalue == 0
    lo = 1 / 10 ** d.precision + d.offset          # code 1 (0 is the fill)
    hi = 65535 / 10 ** d.precision + d.offset
    assert lo <= 1.5 * -1811 and hi >= 1.5 * 1028, (lo, hi)   # the measured extremes with a 1.5x margin
    assert round(lo, 1) == -3000.0 and round(hi, 1) == 3553.4


# 12-year C1 extremes (WRF 12 km NZ, 2013-2024 sim-years, every 3-hourly frame and region; health-scan shards,
# 2026-10-20). precip_tr is a 3-hourly increment, floored at 0 by the producer and bounded by the total's 413 mm.
# vimf_u/vimf_v reached -4363 against their old -5000 floor (widened to -10000 in 0.2.9).
WVT_EXTREMES = {
    'vimf_u': (-4167.714355, 3998.096436),
    'vimf_v': (-4363.066406, 3698.450439),
    'precip_tr': (0.0, 413.0),
    'pwat_tr': (-0.193935, 88.313431),
    'vimf_tr_u': (-3468.710938, 3580.417480),
    'vimf_tr_v': (-3926.415527, 3458.536865),
    'ivt': (0.002659, 4645.840820),
}


def storable_range(name):
    """The lowest and highest decodable values: code 0 is the fill, so the range starts at code 1."""
    d = data_var_defs[name].dtype
    q = 1 / 10**d.precision
    imax = {'uint16': 2**16 - 1, 'uint32': 2**32 - 1}[d.dtype_encoded]
    return q + d.offset, imax * q + d.offset


def test_wvt_templates_cover_c1_extremes():
    """The tracer, IVT and total VIMF templates (0.2.9) hold the measured C1 extremes with a 1.5x margin; below the floor or
    above the ceiling cfdb stores a value as missing. PWAT_TR goes slightly negative (-0.19 kg m-2), so its floor
    must be below 0."""
    for name, (vmin, vmax) in WVT_EXTREMES.items():
        lo, hi = storable_range(name)
        assert lo <= min(0.0, 1.5 * vmin) and hi >= 1.5 * vmax, (name, lo, hi)


def test_wvt_template_encodings():
    """Pinned: an encoding is fixed for the life of a dataset once its first variable is created."""
    want = {
        'precip_tr': ('uint32', 4, -1, (-0.9999, 429495.7295)),
        'pwat_tr': ('uint16', 2, -1, (-0.99, 654.35)),
        'vimf_tr_u': ('uint32', 1, -10000.1, (-10000.0, 429486729.4)),
        'vimf_tr_v': ('uint32', 1, -10000.1, (-10000.0, 429486729.4)),
        'ivt': ('uint32', 1, -1, (-0.9, 429496728.5)),
        'vimf_u': ('uint32', 1, -10000.1, (-10000.0, 429486729.4)),
        'vimf_v': ('uint32', 1, -10000.1, (-10000.0, 429486729.4)),
    }
    for name, (enc, precision, offset, (lo, hi)) in want.items():
        d = data_var_defs[name].dtype
        assert (d.name, d.dtype_encoded, d.precision, d.offset, d.fillvalue) == ('float32', enc, precision, offset, 0)
        got = storable_range(name)
        assert (round(got[0], precision), round(got[1], precision)) == (lo, hi), (name, got)


def test_wvt_template_units():
    units = {'precip_tr': 'mm', 'pwat_tr': 'kg m-2', 'vimf_tr_u': 'kg m-1 s-1', 'vimf_tr_v': 'kg m-1 s-1',
             'ivt': 'kg m-1 s-1'}
    for name, u in units.items():
        assert data_var_defs[name].attrs['units'] == u, name


def test_precip_tr_resolves_small_shares():
    """precip_tr holds one region's share of a cell's rain, so its quantum must be well below the total's 0.01 mm
    (a 0.01 mm quantum lost 8.5% of nz_land's tagged rain on 2023-07-01), and need not go below the ~1e-5 mm the
    source increments resolve (float32 spacing of a 100 mm running total is 7.6e-6 mm)."""
    q = 1 / 10 ** data_var_defs['precip_tr'].dtype.precision
    assert q <= 1e-4 < 1 / 10 ** data_var_defs['precipitation'].dtype.precision
    assert q >= 1e-5


def test_tagged_fields_carry_no_standard_name():
    """A tagged field is one tracer region's share, not the CF quantity its total is (no CF name exists for it)."""
    for name in ('precip_tr', 'pwat_tr', 'vimf_tr_u', 'vimf_tr_v'):
        assert 'standard_name' not in data_var_defs[name].attrs, name


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
        'ivt',
        'precip_tr',
        'pwat_tr',
        'vimf_tr_u',
        'vimf_tr_v',
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

"""Variable definitions for cfdb."""

from cfdb_vars.coord_vars import coord_var_defs
from cfdb_vars.data_vars import data_var_defs
from cfdb_vars.time_dtype_params import time_dtype_params as time_dtype_params

__version__ = '0.1.0'

var_defs = {**coord_var_defs, **data_var_defs}

short_name_map = {
    'lon': 'longitude',
    'lat': 'latitude',
    'height': 'height',
    'altitude': 'altitude',
    'time': 'time',
    'x': 'x',
    'y': 'y',
    'point': 'point',
    'line': 'line',
    'polygon': 'polygon',
    'modified_date': 'modified_date',
    'band': 'band',
    'censor_code': 'censor_code',
    'precip': 'precipitation',
    'air_temp': 'air_temperature',
    'wind_speed': 'wind_speed',
    'wind_direction': 'wind_direction',
    'u_wind': 'u_wind',
    'v_wind': 'v_wind',
    'relative_humidity': 'relative_humidity',
    'dew_temp': 'dew_point_temperature',
    'soil_temp': 'soil_temperature',
    'lwe_soil_moisture': 'lwe_soil_moisture',
    'surface_pressure': 'surface_pressure',
    'specific_humidity': 'specific_humidity',
    'mixing_ratio': 'mixing_ratio',
    'shortwave_radiation': 'shortwave_radiation',
    'longwave_radiation': 'longwave_radiation',
    'snow_depth': 'snow_depth',
    'mslp': 'mslp',
    'vorticity': 'vorticity',
    'vertical_velocity': 'vertical_velocity',
    'sensible_heat_flux': 'sensible_heat_flux',
    'moisture_flux': 'moisture_flux',
    'albedo': 'albedo',
    'emissivity': 'emissivity',
    'terrain_height': 'terrain_height',
    'potential_temperature': 'potential_temperature',
    'equivalent_potential_temperature': 'equivalent_potential_temperature',
    'land_use_modis': 'land_use_modis',
}

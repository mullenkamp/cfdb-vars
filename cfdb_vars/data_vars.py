"""Data variable definitions for cfdb."""

from cfdb_models.data_models import DataType, DataVarDef

data_var_defs = {
    'modified_date': DataVarDef(
        dtype=DataType(name='datetime64[us]', dtype_encoded='int64', offset=1756684800000000),
        attrs={
            'long_name': 'last modified date',
        },
    ),
    'band': DataVarDef(
        dtype=DataType(name='uint8'),
        attrs={
            'long_name': 'band number',
        },
    ),
    'censor_code': DataVarDef(
        dtype=DataType(name='uint8'),
        attrs={
            'long_name': 'data censor code',
            'standard_name': 'status_flag',
            'flag_values': '0 1 2 3 4 5',
            'flag_meanings': 'greater_than less_than not_censored non-detect present_but_not_quantified unknown',
        },
    ),
    'precipitation': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'precipitation',
            'units': 'mm',
            'standard_name': 'precipitation_amount',
            'odm2_variable_name': 'precipitation',
        },
    ),
    'air_temperature': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-61, fillvalue=0),
        attrs={
            'long_name': 'air temperature',
            'units': 'K',
            'standard_name': 'air_temperature',
        },
    ),
    'wind_speed': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'wind speed',
            'units': 'm/s',
            'standard_name': 'wind_speed',
            'odm2_variable_name': 'windSpeed',
        },
    ),
    'wind_direction': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'wind direction',
            'units': 'deg',
            'standard_name': 'wind_to_direction',
            'odm2_variable_name': 'windDirection',
        },
    ),
    'u_wind': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-101, fillvalue=0),
        attrs={
            'long_name': 'eastward wind component',
            'units': 'm/s',
            'standard_name': 'eastward_wind',
        },
    ),
    'v_wind': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-101, fillvalue=0),
        attrs={
            'long_name': 'northward wind component',
            'units': 'm/s',
            'standard_name': 'northward_wind',
        },
    ),
    'relative_humidity': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'relative humidity',
            'units': 'm^3/m^3',
            'standard_name': 'relative_humidity',
            'odm2_variable_name': 'relativeHumidity',
        },
    ),
    'dew_point_temperature': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-61, fillvalue=0),
        attrs={
            'long_name': 'dew point temperature',
            'units': 'K',
            'standard_name': 'dew_point_temperature',
            'odm2_variable_name': 'temperatureDewPoint',
        },
    ),
    'soil_temperature': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-61, fillvalue=0),
        attrs={
            'long_name': 'soil temperature',
            'units': 'K',
            'standard_name': 'soil_temperature',
        },
    ),
    'lwe_soil_moisture': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'liquid water equivalent of soil moisture',
            'units': 'mm',
            'standard_name': 'lwe_thickness_of_soil_moisture_content',
        },
    ),
    'surface_pressure': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint32', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'surface pressure',
            'units': 'Pa',
            'standard_name': 'surface_air_pressure',
        },
    ),
    'specific_humidity': DataVarDef(
        dtype=DataType(name='float32', precision=6, dtype_encoded='uint16', offset=-0.000001, fillvalue=0),
        attrs={
            'long_name': 'specific humidity',
            'units': 'kg kg-1',
            'standard_name': 'specific_humidity',
        },
    ),
    'mixing_ratio': DataVarDef(
        dtype=DataType(name='float32', precision=6, dtype_encoded='uint16', offset=-0.000001, fillvalue=0),
        attrs={
            'long_name': 'water vapor mixing ratio',
            'units': 'kg kg-1',
            'standard_name': 'humidity_mixing_ratio',
        },
    ),
    'shortwave_radiation': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'downward shortwave radiation at surface',
            'units': 'W m-2',
            'standard_name': 'surface_downwelling_shortwave_flux_in_air',
            'odm2_variable_name': 'radiationIncomingShortwave',
        },
    ),
    'longwave_radiation': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'downward longwave radiation at surface',
            'units': 'W m-2',
            'standard_name': 'surface_downwelling_longwave_flux_in_air',
            'odm2_variable_name': 'radiationIncomingLongwave',
        },
    ),
    'snow_depth': DataVarDef(
        dtype=DataType(name='float32', precision=3, dtype_encoded='uint16', offset=-0.001, fillvalue=0),
        attrs={
            'long_name': 'physical snow depth',
            'units': 'm',
            'standard_name': 'surface_snow_thickness',
            'odm2_variable_name': 'snowDepth',
        },
    ),
    'mslp': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint32', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'mean sea level pressure',
            'units': 'Pa',
            'standard_name': 'air_pressure_at_mean_sea_level',
        },
    ),
    'vorticity': DataVarDef(
        dtype=DataType(name='float32', precision=5, dtype_encoded='uint16', offset=-0.300001, fillvalue=0),
        attrs={
            'long_name': 'relative vorticity',
            'units': 's-1',
            'standard_name': 'atmosphere_relative_vorticity',
        },
    ),
    'vertical_velocity': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-50.01, fillvalue=0),
        attrs={
            'long_name': 'vertical velocity',
            'units': 'm s-1',
            'standard_name': 'upward_air_velocity',
        },
    ),
    'sensible_heat_flux': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint16', offset=-300.1, fillvalue=0),
        attrs={
            'long_name': 'upward sensible heat flux',
            'units': 'W m-2',
            'standard_name': 'surface_upward_sensible_heat_flux',
            'odm2_variable_name': 'sensibleHeatFlux',
        },
    ),
    'moisture_flux': DataVarDef(
        dtype=DataType(name='float32', precision=6, dtype_encoded='uint16', offset=-0.010001, fillvalue=0),
        attrs={
            'long_name': 'upward moisture flux',
            'units': 'kg m-2 s-1',
            'standard_name': 'water_evapotranspiration_flux',
        },
    ),
    'albedo': DataVarDef(
        dtype=DataType(name='float32', precision=3, dtype_encoded='uint16', offset=-0.001, fillvalue=0),
        attrs={
            'long_name': 'surface albedo',
            'units': '1',
            'standard_name': 'surface_albedo',
            'odm2_variable_name': 'albedo',
        },
    ),
    'emissivity': DataVarDef(
        dtype=DataType(name='float32', precision=3, dtype_encoded='uint16', offset=-0.001, fillvalue=0),
        attrs={
            'long_name': 'surface emissivity',
            'units': '1',
            'standard_name': 'surface_longwave_emissivity',
        },
    ),
    'terrain_height': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'terrain height above sea level',
            'units': 'm',
            'standard_name': 'surface_altitude',
        },
    ),
    'potential_temperature': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-61, fillvalue=0),
        attrs={
            'long_name': 'air potential temperature',
            'units': 'K',
            'standard_name': 'air_potential_temperature',
        },
    ),
    'equivalent_potential_temperature': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-61, fillvalue=0),
        attrs={
            'long_name': 'equivalent potential temperature',
            'units': 'K',
            'standard_name': 'equivalent_potential_temperature',
        },
    ),
    'geopotential_height': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint32', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'geopotential height',
            'units': 'm',
            'standard_name': 'geopotential_height',
        },
    ),
    'land_sea_mask': DataVarDef(
        dtype=DataType(name='uint8'),
        attrs={
            'long_name': 'land sea mask',
            'units': '1',
            'standard_name': 'land_binary_mask',
        },
    ),
    'sea_ice': DataVarDef(
        dtype=DataType(name='float32', precision=3, dtype_encoded='uint16', offset=-0.001, fillvalue=0),
        attrs={
            'long_name': 'sea ice area fraction',
            'units': '1',
            'standard_name': 'sea_ice_area_fraction',
        },
    ),
    'sea_surface_temp': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-61, fillvalue=0),
        attrs={
            'long_name': 'sea surface temperature',
            'units': 'K',
            'standard_name': 'sea_surface_temperature',
        },
    ),
    'snow_water_equiv': DataVarDef(
        dtype=DataType(name='float32', precision=1, dtype_encoded='uint16', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'snow water equivalent',
            'units': 'kg m-2',
            'standard_name': 'lwe_thickness_of_surface_snow_amount',
        },
    ),
    'soil_moisture': DataVarDef(
        dtype=DataType(name='float32', precision=3, dtype_encoded='uint16', offset=-0.001, fillvalue=0),
        attrs={
            'long_name': 'volumetric soil moisture',
            'units': 'm3 m-3',
            'standard_name': 'volume_fraction_of_condensed_water_in_soil',
        },
    ),
    'soil_layer_temp': DataVarDef(
        dtype=DataType(name='float32', precision=2, dtype_encoded='uint16', offset=-61, fillvalue=0),
        attrs={
            'long_name': 'soil layer temperature',
            'units': 'K',
            'standard_name': 'soil_temperature',
        },
    ),
    'land_use_modis': DataVarDef(
        dtype=DataType(name='uint8'),
        attrs={
            'long_name': 'land use category for modis',
            'flag_values': '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21',
            'flag_meanings': (
                'evergreen_needleleaf_forests evergreen_broadleaf_forests deciduous_needleleaf_forests'
                ' deciduous_broadleaf_forests mixed_forests closed_shrublands open_shrublands woody_savannas'
                ' savannas grasslands permanent_wetlands croplands urban_and_built_up'
                ' cropland_natural_vegetation_mosaics permanent_snow_and_ice barren water_bodies wooded_tundra'
                ' mixed_tundra barren_tundra lakes'
            ),
        },
    ),
}

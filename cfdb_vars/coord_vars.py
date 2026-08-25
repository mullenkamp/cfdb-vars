"""Coordinate variable definitions for cfdb."""

from cfdb_models.data_models import CoordVarDef, DataType

coord_var_defs = {
    'longitude': CoordVarDef(
        dtype=DataType(name='float64', precision=6, dtype_encoded='uint32', offset=-180.000001, fillvalue=0),
        attrs={
            'long_name': 'longitude',
            'units': 'degrees_east',
            'standard_name': 'longitude',
            'axis': 'X',
            'odm2_variable_name': 'longitude',
        },
    ),
    'latitude': CoordVarDef(
        dtype=DataType(name='float64', precision=6, dtype_encoded='uint32', offset=-90.000001, fillvalue=0),
        attrs={
            'long_name': 'latitude',
            'units': 'degrees_north',
            'standard_name': 'latitude',
            'axis': 'Y',
            'odm2_variable_name': 'latitude',
        },
    ),
    'height': CoordVarDef(
        dtype=DataType(name='float64', precision=3, dtype_encoded='uint32', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'height',
            'units': 'm',
            'standard_name': 'height',
            'positive': 'up',
            'axis': 'Z',
            'odm2_variable_name': 'height',
        },
    ),
    'altitude': CoordVarDef(
        dtype=DataType(name='float64', precision=3, dtype_encoded='uint32', offset=-11000.001, fillvalue=0),
        attrs={
            'long_name': 'altitude',
            'units': 'm',
            'standard_name': 'altitude',
            'positive': 'up',
            'axis': 'Z',
            'odm2_variable_name': 'altitude',
        },
    ),
    'time': CoordVarDef(
        dtype=DataType(name='datetime64[m]', dtype_encoded='int32', offset=-36816481),
        attrs={
            'long_name': 'time',
            'standard_name': 'time',
            'axis': 'T',
        },
    ),
    # --- forecast axes -------------------------------------------------------------------
    # These two are the (init, lead) pair used by the ts_forecast / grid_forecast dataset types.
    #
    # WARNING -- the axis attrs below are load-bearing, not decoration. cfdb derives a
    # coordinate's internal Axis from the CF 'axis' attr here (utils.get_var_params), and it
    # REFUSES two coordinates sharing an axis. So forecast_reference_time takes 'T' and
    # forecast_period deliberately has NO axis attr: CF defines only X/Y/Z/T, and a lead-time
    # dimension is none of them.
    'forecast_reference_time': CoordVarDef(
        dtype=DataType(name='datetime64[m]', dtype_encoded='int32', offset=-36816481),
        attrs={
            'long_name': 'forecast reference time',
            'standard_name': 'forecast_reference_time',
            'axis': 'T',
        },
    ),
    # WARNING -- 'units' is REQUIRED, load-bearing, and DELIBERATELY NOT DEFAULTED HERE.
    #
    # cfdb has no timedelta dtype, so lead is a bare integer; adding a bare integer to a
    # datetime64 evaluates in the DATETIME's unit, so `last(forecast_reference_time) +
    # max(forecast_period)` silently adds MINUTES against the datetime64[m] above. Every
    # consumer doing init+lead arithmetic must read this attr and build an explicit
    # np.timedelta64.
    #
    # An earlier cut defaulted it to 'h'. Both arms of a code review independently called that
    # a trap, and they were right: a producer of 15-minute leads who simply forgot would have
    # been silently labelled hourly -- a valid-time range 4x too long -- AND the default made
    # the downstream "units must be declared" check unreachable, because the attr was never
    # absent. Omitting it turns a silent error into a loud refusal at validation time.
    #
    # Set it explicitly: ds['forecast_period'].attrs['units'] = 'h'  (or 'min', 's', 'days').
    'forecast_period': CoordVarDef(
        dtype=DataType(name='int32'),
        attrs={
            'long_name': 'forecast period',
            'standard_name': 'forecast_period',
        },
    ),
    'x': CoordVarDef(
        dtype=DataType(name='float32', precision=1),
        attrs={
            'long_name': 'x coordinate of projection',
            'units': 'metres',
            'standard_name': 'projection_x_coordinate',
            'axis': 'X',
        },
    ),
    'y': CoordVarDef(
        dtype=DataType(name='float32', precision=1),
        attrs={
            'long_name': 'y coordinate of projection',
            'units': 'metres',
            'standard_name': 'projection_y_coordinate',
            'axis': 'Y',
        },
    ),
    'depth': CoordVarDef(
        dtype=DataType(name='float64', precision=3, dtype_encoded='uint32', offset=-0.001, fillvalue=0),
        attrs={
            'long_name': 'depth below surface',
            'units': 'm',
            'standard_name': 'depth',
            'positive': 'down',
            'axis': 'Z',
        },
    ),
    'pressure': CoordVarDef(
        dtype=DataType(name='float64', precision=1, dtype_encoded='uint32', offset=-1, fillvalue=0),
        attrs={
            'long_name': 'pressure',
            'units': 'Pa',
            'standard_name': 'air_pressure',
            'axis': 'Z',
        },
    ),
    'point': CoordVarDef(
        dtype=DataType(name='point', precision=5),
        attrs={
            'long_name': 'location geometry as points',
            'axis': 'XY',
        },
    ),
    'line': CoordVarDef(
        dtype=DataType(name='line', precision=5),
        attrs={
            'long_name': 'location geometry as lines',
            'axis': 'XY',
        },
    ),
    'polygon': CoordVarDef(
        dtype=DataType(name='polygon', precision=5),
        attrs={
            'long_name': 'location geometry as polygons',
            'axis': 'XY',
        },
    ),
}

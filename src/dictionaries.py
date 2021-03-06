# -*- coding: utf-8 -*-
"""
Dictionaries used for post-processing.
"""

# Conversion factors between time units and seconds
factors_time = {
    'sec': 1.,
    'min': 60., # WARNING: minutes not yet considered in find_times
    'hr':  3600.,
    'd':   3600. * 24.,
    'yr':  3600. * 24. * 365,
}


fp_uncertainty = {
    '0.1sec':       0.079,
    '1.0sec':       0.079,
    '10.0sec':      0.072,
    '100.0sec':     0.072,
    '300.0sec':     0.06,
    '600.0sec':     0.06,
    '1800.0sec':    0.04,
    '1.0hr':        0.04,
    '2.0hr':        0.04,
    '5.0hr':        0.03,
    '10.0hr':       0.03,
    '1.0d':         0.03,
    '2.0d':         0.025,
    '4.0d':         0.025,
    '8.0d':         0.025,
    '15.0d':        0.025,
    '30.0d':        0.025,
    '90.0d':        0.025,
    '180.0d':       0.025,
    '270.0d':       0.025,
    '1.0yr':        0.025,
    '1.25yr':       0.025,
    '1.5yr':        0.025,
    '2.0yr':        0.025,
    '3.0yr':        0.025,
    '5.0yr':        0.025,
    '10.0yr':       0.025,
    '50.0yr':       0.025,
    '100.0yr':      0.025,
    '10000.0yr':    0.025
}


act_u9_np9_uncertainty = {
    '0.1sec':      0.25,
    '1.0sec':      0.25,
    '10.0sec':     0.25,
    '100.0sec':    0.25,
    '300.0sec':    0.25,
    '600.0sec':    0.25,
    '1800.0sec':   0.25,
    '1.0hr':       0.25,
    '2.0hr':       0.25,
    '5.0hr':       0.25,
    '10.0hr':      0.25,
    '1.0d':        0.25,
    '2.0d':        0.25,
    '4.0d':        0.25,
    '8.0d':        0.25,
    '15.0d':       0.25,
    '30.0d':       0.25,
    '90.0d':       0.24,
    '180.0d':      0.22,
    '270.0d':      0.20,
    '1.0yr':       0.18,
    '1.25yr':      0.16,
    '1.5yr':       0.14,
    '2.0yr':       0.11,
    '3.0yr':       0.08,
    '5.0yr':       0.07,
    '10.0yr':      0.07,
    '50.0yr':      0.10,
    '100.0yr':     0.11,
    '10000.0yr':   0.11
}


u9_np9_uncertainty = {
    '0.1sec':       0.06,
    '1.0sec':       0.06,
    '10.0sec':      0.06,
    '100.0sec':     0.06,
    '300.0sec':     0.06,
    '600.0sec':     0.06,
    '1800.0sec':    0.06,
    '1.0hr':        0.06,
    '2.0hr':        0.06,
    '5.0hr':        0.06,
    '10.0hr':       0.06,
    '1.0d':         0.06,
    '2.0d':         0.06,
    '4.0d':         0.06,
    '8.0d':         0.06,
    '15.0d':        0.06,
    '30.0d':        0.06,
    '90.0d':        0.00,
    '10000.0yr':    0.00
}


fuel_uncertainty = {
    'UO2': {
        '0.1sec':      0.075,
        '1.0sec':      0.074,
        '10.0sec':     0.067,
        '100.0sec':    0.064,
        '300.0sec':    0.053,
        '600.0sec':    0.052,
        '1800.0sec':   0.035,
        '1.0hr':       0.035,
        '2.0hr':       0.035,
        '5.0hr':       0.027,
        '10.0hr':      0.027,
        '1.0d':        0.027,
        '2.0d':        0.024,
        '4.0d':        0.024,
        '8.0d':        0.025,
        '15.0d':       0.026,
        '30.0d':       0.026,
        '90.0d':       0.028,
        '180.0d':      0.028,
        '270.0d':      0.027,
        '1.0yr':       0.027,
        '1.25yr':      0.026,
        '1.5yr':       0.025,
        '2.0yr':       0.025,
        '3.0yr':       0.024,
        '5.0yr':       0.024,
        '10.0yr':      0.025,
        '50.0yr':      0.047,
        '100.0yr':     0.076,
        '10000.0yr':   0.076
    },
    'MOX': {
        '0.1sec':      0.075,
        '1.0sec':      0.074,
        '10.0sec':     0.067,
        '100.0sec':    0.064,
        '300.0sec':    0.053,
        '600.0sec':    0.052,
        '1800.0sec':   0.035,
        '1.0hr':       0.035,
        '2.0hr':       0.035,
        '5.0hr':       0.027,
        '10.0hr':      0.027,
        '1.0d':        0.027,
        '2.0d':        0.024,
        '4.0d':        0.024,
        '8.0d':        0.025,
        '15.0d':       0.026,
        '30.0d':       0.026,
        '90.0d':       0.028,
        '180.0d':      0.028,
        '270.0d':      0.027,
        '1.0yr':       0.027,
        '1.25yr':      0.026,
        '1.5yr':       0.025,
        '2.0yr':       0.025,
        '3.0yr':       0.024,
        '5.0yr':       0.024,
        '10.0yr':      0.025,
        '50.0yr':      0.047,
        '100.0yr':     0.076,
        '10000.0yr':   0.076
    }
}

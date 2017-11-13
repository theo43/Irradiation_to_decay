# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: Regular expressions
"""

# Regular expressions allowing getting time steps and results in blocks
#   1. For time steps research
regex_time = r"^\s+(charge\s+discharge|initial)\s+\d+\.\d?\s?[sechrdyr]"

#   2. For category ('elements' or 'nuclides') research
regex_category = {
    # For 'Elements' category. Gets the "totals"
    'Elements': r"^\s+([a-z]{,2}|totals)\s+\d\.\d{2}E[+-]\d{2}",
    # For 'Isotopes' category. Does not get "total"
    'Isotopes': r"^\s+[a-z]{1,2}\s{0,2}\d{1,3}[m]?\s+\d\.\d{2}E[+-]\d{2}"
}

# Regular expression to detect category and unit
regex_categ_unit = r"concentrations, grams|radioactivity, curies|thermal"
regex_categ_unit += r" power, watts|gamma power, watts"

# Regular expression matching groups only
regex_after_Decay = r"actinides|fission products|light elements"

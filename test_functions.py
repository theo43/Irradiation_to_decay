#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Nov. 2017
POS: global tests of the tool - decay power curve and source terms generation
"""

import pandas as pd
from functions import (create_df_decay_power,
                       gather_df_decay_power,
                       create_df_inventories,
                       gather_df_inventories,
                       convert_str_sec)
from dictionaries import (factors_time, act_u9_np9_uncertainty,
                          u9_np9_uncertainty, fp_uncertainty, fuel_uncertainty)
from regular_expressions import (regex_time, regex_category, regex_categ_unit,
                                 regex_after_Decay)

def test_decay_power_generation():
    """Test for decay power curve generation"""

    # Import the test DataFrame
    df_test = pd.read_excel('input_tests/Decay_power_curve.xlsx',
                            sheetname='decay_power_curve',
                            index_col = 0)

    # Create the DataFrame to be compared to df_test
    list_path = ['input_tests/file1.out',
                 'input_tests/file2.out',
                 'input_tests/file3.out']
    list_nbfa = [21, 68, 68]
    list_massfa = [0.465] * 3

    list_df = []
    for path in list_path:
        list_df.append(create_df_decay_power(path,
                                             factors_time,
                                             regex_time,
                                             regex_category,
                                             regex_categ_unit,
                                             regex_after_Decay))

    decay_power = gather_df_decay_power(list_df,
                                        list_massfa,
                                        list_nbfa,
                                        3055.,
                                        False,
                                        act_u9_np9_uncertainty,
                                        u9_np9_uncertainty,
                                        fp_uncertainty,
                                        fuel_uncertainty,
                                        factors_time)
    
    assert not (False in decay_power == df_test)


def test_source_terms_generation():
    """Test for source terms generation"""

    # Import the test DataFrames
    PATH_DF_ELEMENTS = 'input_tests/Source_terms_elements.xlsx'
    PATH_DF_ISOTOPES = 'input_tests/Source_terms_isotopes.xlsx'

    df_test_elem = pd.read_excel(PATH_DF_ELEMENTS,
                                 sheetname=['grams', 'becquerels',
                                            'watts_total', 'watts_gamma'],
                                 index_col=[0, 1])
    test_elem_g = df_test_elem['grams']
    test_elem_bq = df_test_elem['becquerels']
    test_elem_wt = df_test_elem['watts_total']
    test_elem_wg = df_test_elem['watts_gamma']
    index_elem = test_elem_g.index

    df_test_isot = pd.read_excel(PATH_DF_ISOTOPES,
                                 sheetname=['grams', 'becquerels',
                                            'watts_total', 'watts_gamma'],
                                 index_col=[0, 1])
    
    test_isot_g = df_test_isot['grams']
    test_isot_bq = df_test_isot['becquerels']
    test_isot_wt = df_test_isot['watts_total']
    test_isot_wg = df_test_isot['watts_gamma']
    index_isot = test_isot_g.index

    # Create the new DataFrame to be compared to the test_*
    list_path = ['input_tests/file1.out',
                 'input_tests/file2.out',
                 'input_tests/file3.out']
    list_nbfa = [21, 68, 68]
    list_massfa = [0.465] * 3
    list_units = ['g', 'bq', 'wt', 'wg']
    list_categories = ['Elements', 'Isotopes']

    list_df = []
    for path in list_path:
        list_df.append(create_df_inventories(path,
                                             list_units,
                                             list_categories,
                                             factors_time,
                                             regex_time,
                                             regex_category,
                                             regex_categ_unit,
                                             regex_after_Decay))
    source_terms = gather_df_inventories(list_categories,
                                         list_units,
                                         list_df,
                                         list_massfa,
                                         list_nbfa)
    timesteps = source_terms['Elements']['g'].columns
    timesteps = sorted(timesteps,
                       key=lambda x: convert_str_sec(x, factors_time))    

    elem_g = source_terms['Elements']['g'].reset_index()
    elem_g = elem_g.set_index(['Group', 'Element']).reindex(index=index_elem,
                                                            columns=timesteps)
    elem_bq = source_terms['Elements']['bq'].reset_index()
    elem_bq = elem_bq.set_index(['Group', 'Element']).reindex(index=index_elem,
                                                            columns=timesteps)
    elem_wt = source_terms['Elements']['wt'].reset_index()
    elem_wt = elem_wt.set_index(['Group', 'Element']).reindex(index=index_elem,
                                                            columns=timesteps)
    elem_wg = source_terms['Elements']['wg'].reset_index()
    elem_wg = elem_wg.set_index(['Group', 'Element']).reindex(index=index_elem,
                                                            columns=timesteps)
    isot_g = source_terms['Isotopes']['g'].reset_index()
    isot_g = isot_g.set_index(['Group', 'Isotope']).reindex(index=index_isot,
                                                            columns=timesteps)
    isot_bq = source_terms['Isotopes']['bq'].reset_index()
    isot_bq = isot_bq.set_index(['Group', 'Isotope']).reindex(index=index_isot,
                                                            columns=timesteps)
    isot_wt = source_terms['Isotopes']['wt'].reset_index()
    isot_wt = isot_wt.set_index(['Group', 'Isotope']).reindex(index=index_isot,
                                                            columns=timesteps)
    isot_wg = source_terms['Isotopes']['wg'].reset_index()
    isot_wg = isot_wg.set_index(['Group', 'Isotope']).reindex(index=index_isot,
                                                            columns=timesteps)
    
    assert not (False in test_elem_g == elem_g)
    assert not (False in test_elem_bq == elem_bq)
    assert not (False in test_elem_wt == elem_wt)
    assert not (False in test_elem_wg == elem_wg)
    assert not (False in test_isot_g == isot_g)
    assert not (False in test_isot_bq == isot_bq)
    assert not (False in test_isot_wt == isot_wt)
    assert not (False in test_isot_wg == isot_wg)

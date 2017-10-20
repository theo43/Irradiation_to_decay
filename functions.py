#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: Functions
"""

def find_group(line):
    """Post-treat the name of the group of nuclides or elements ("actinides",
       "fission products" or "light elements")

       Argument:
           line (string): line of a .out file to post-treat

       Returns:
           group (string): group of the isotope or element

       Example:
           >>> find_group("  Decay from 11 h to 20 h    actinides   page  533")
           'Actinides'
    """
    from re import search
    group='NA'
    if search("fission products", line):
        group = "Fission products"
    if search("actinides", line):
        group = "Actinides"
    if search("light elements", line):
        group = "Light elements"

    return group


def find_category_unit(line):
    """Post-treat the category of results: "nuclides" or "elements" and the
       unit of the results:
           - "g" for mass in grams;
           - "Bq" for radioactivity in Bq (1 Cu = 3.7x10^10 Bq);
               (Curies results given in .out files are converted in Bq)
           - "W" for total thermal power in watts;
           - "W_gamma" for gamma contribution in total power, in watts.

       Argument:
           line (string): line of a .out file to post-treat

       Returns:
           tup (tuple): contains the category (tup[0]) and the unit (tup[1])

       Example:
           >>> find_category_unit("      element thermal power, watts  ")
           ('Elements', 'W')

    """
    from re import search
    if search("concentrations, grams", line):
        unit = "g"
    if search("radioactivity, curies", line):
        unit = "Bq"
    if search("thermal power, watts", line):
        unit = "W"
    if search("gamma power, watts", line):
        unit = "W_gamma"
    if search(" element ", line):
        category = "Elements"
    if search(" nuclide ", line):
        category = "Isotopes"
    tup = (category, unit)

    return tup


def find_times(line):
    """Post-treat the time steps of the block of data being read. Time steps
       are given with the following form: "float"+"unit". If the time step
       value is given in:
            - Seconds: no space between the float and "sec";
            - Minutes: to be completed
            - Hours: one space between the float and "hr";
            - Days: one space between the float and "d";
            - Months: to be completed
            - Years: one space between the float and "yr";

       Argument:
           line (string): line of a .out file to post-treat

       Returns:
           time_steps (list): split of the line containing the time steps

       Example:
           >>> find_times("             initial   11.0 hr   12.0 hr ")
           ['initial', '11.0 hr', '12.0 hr']

    """
    from re import findall
    time_steps = findall("[a-z]+|\d+\.\d{,2}\s?[secdhryr]{1,3}", line)
    return time_steps


def find_results(line):
    """Post-treat the results in [unit] of a block of data being read

       Argument:
           line (string): line of a .out file to post-treat

       Returns:
           - results (list): split of the line containing the results. The
             first element of the list is the isotope or element name (string),
             the rest is the resulting contribution (float)

       Example:
           >>> find_results("    am239   2.90E-18  4.44E-09  4.44E-09  ")
           ['am239', 2.9e-18, 4.44e-09, 4.44e-09]

    """
    from re import findall
    results = findall("[a-z]{1,6}\s{,2}\d{,3}m?|\d\.\d{2}E[+-]\d{2}", line)
    for i, r in enumerate(results[1:]):
        results[i+1] = float(r)

    return results


def create_df_decay_power(file_path,      factors_time,     regex_time,
                          regex_category, regex_categ_unit, regex_after_Decay):
    """Read a single .out file and create a pandas DataFrame containing the
       power results (in Watts total) for every detected time steps, for
       following contribution:
           - Total decay power (best-estimate)
           - Actinides (without 239U and 239Np)
           - 239U and 239 Np
           - Fission products

       Arguments:
           - file_path (string): absolute location of the file
           - factors_time (dict): correspondence in seconds for different time
             units
           - regex_* (string): regular expressions

       Returns:
           df (pandas.DataFrame)

    """
    import re
    import pandas as pd

    # Regex "nuclides or elements": initially 'None', switches to:
    #   regex_category['elements'] if category == elements;
    #   regex_category['nuclides'] if category == nuclides.
    regex_noe = None

    # Variable switching to 1 when a block of 'Decay' results is read.
    readblock = 0

    # Create the DataFrame containing the results
    df = pd.DataFrame()
    df.columns.name = 'Time steps'
    df.index.name = 'Contributions'

    # Open the .out file in read mode and store the lines in a list
    with open(file_path, 'r') as fi:
        read_file = fi.readlines()

    for i, line in enumerate(read_file):

        if re.search("^\s+Decay ", line) and\
        (re.search(regex_after_Decay, line)):
            readblock = 1
            # Search the group of nuclides or elements
            # Ex: 'fission products', 'actinides' or 'light elements'
            group = find_group(line)

        if readblock == 1 and re.search(regex_categ_unit, line):
            # Search the category ('elements' or 'nuclides')
            category, unit = find_category_unit(line)
            regex_noe = regex_category[category]

        if readblock == 1 and re.search(regex_time, line):
            # Read the block of data only if " Decay " has been read
            time_steps = find_times(line)
            for i, t in enumerate(time_steps):
                time_steps[i] = t.replace(" ", "")

        if readblock == 1 and regex_noe != None:

            if re.search(regex_noe, line) and unit == 'W':
                # Search the list of results for the current bloc of data
                #  results[0]: name of the nuclide or element
                #  results[i!=0]: result for the corresponding unit and time
                results = find_results(line)

                # 'NOE': Nuclide Or Element name, without space(s) in it
                NOE = results[0].replace(" ", "")
                NOE = NOE.replace("totals", "total")

                cond1 = (NOE == 'u239' or NOE == 'np239')
                cond2 = (group in  ['Actinides', 'Fission products'] and\
                         NOE == 'total')

                if cond1 == True:
                    se = pd.Series(results[1:],
                                   index=time_steps,
                                   name=NOE.title())
                    df = df.append(se)

                if cond2 == True:
                    se = pd.Series(results[1:],
                                   index=time_steps,
                                   name=group)
                    df = df.append(se)

        if re.search("^\x0c", line) and readblock == 1:
            # Detect the special font at the end of the bloc of data
            # caractherizing the bloc's end: stops data reading
            readblock = 0

    df = df.groupby(df.index).sum()
    del df['initial']
    del df['charge']
    columns = sorted(df.columns,key=lambda x: convert_str_sec(x, factors_time))
    df = df.reindex(columns=columns)
    df = df.T
    df['Total (BE)'] = df['Actinides']+df['Fission products']

    return df


def gather_df_decay_power(list_batch_df,            FAmass_per_file,
                          nFA_per_file,             core_power,
                          mox,                      act_u9_np9_uncertainty,
                          u9_np9_uncertainty,       fp_uncertainty,
                          fuel_uncertainty,         factors_time):
    """Gather the DataFrames listed in list_batch_df, taking into account the
       number of FA per batch and the FA mass in each batch.
       Calculate the resulting Best-Estimate power (%FP), sigma value (%), and
       the power value with 1.645, 2.0, 3.0 sigma (%FP).

       Arguments:
           - list_batch_df (list): pandas DataFrames containing decay power
             data
           - FAmass_per_file (list): corresponding FA masses per DataFrame
           - nFA_per_file (list): corresponding numbers of FA per DataFrame
           - core_power (float): power used to normalize the decay power curve
           - mox (bool): if the core contains mox or not
           - *_uncertainty (dict): uncertainties corresponding to decay times
           - factors_time (dict): correspondence in seconds for different time
             units

        Returns:
           df (pandas.DataFrame)

    """
    from pandas import DataFrame
    from numpy import nan, sqrt

    df = DataFrame()

    for i, d in enumerate(list_batch_df):
        df = df.add(d * FAmass_per_file[i] * nFA_per_file[i],
                    fill_value=0)

    df['Act-(U9+Np9)']  = df['Actinides'] - df['U239'] - df['Np239']
    df['%Act-(U9+Np9)'] = df['Act-(U9+Np9)']       / df['Total (BE)']
    df['%(U9+Np9)']     = (df['U239']+df['Np239']) / df['Total (BE)']
    df['%FP']           = df['Fission products']   / df['Total (BE)']
    df['Best-estimate'] = df['Total (BE)']         / (core_power*1000000)

    df['act_u9_np9_unc'] = nan
    df['u9_np9_unc']     = nan
    df['fp_unc']         = nan
    df['sig_uo2']        = nan

    if mox == 1:
        df['sig_mox'] = nan

    for i in df.index:
        df['act_u9_np9_unc'][i] = find_unc(i, act_u9_np9_uncertainty,
                                           factors_time)
        df['u9_np9_unc'][i] = find_unc(i, u9_np9_uncertainty, factors_time)
        df['fp_unc'][i] = find_unc(i, fp_uncertainty, factors_time)
        df['sig_uo2'][i] = find_unc(i, fuel_uncertainty['UO2'], factors_time)

        if mox == 1:
            df['sig_mox'][i] = find_unc(i, fuel_uncertainty['MOX'],
                                        factors_time)

    df['sigma_calc'] = sqrt(df['%Act-(U9+Np9)']**2 * df['act_u9_np9_unc']**2
                       + df['%(U9+Np9)']**2        * df['u9_np9_unc']**2
                       + df['%FP']**2              * df['fp_unc']**2 )\
                       / (df['%Act-(U9+Np9)']+df['%(U9+Np9)']+df['%FP'])

    df['Sigma value [%]'] = nan

    if mox == 1:
        for i in df.index:
            df['Sigma value [%]'][i] = max(df['sig_uo2'][i],
                                           df['sig_mox'][i],
                                           df['sigma_calc'][i])
        del df['sig_mox']
        del df['sig_uo2']
    else:
        for i in df.index:
            df['Sigma value [%]'][i] = max(df['sig_uo2'][i],
                                           df['sigma_calc'][i])
        del df['sig_uo2']

    df['1.645 sigma'] = df['Best-estimate'] * (1 + 1.645*df['Sigma value [%]'])
    df['2 sigma']     = df['Best-estimate'] * (1 + 2.000*df['Sigma value [%]'])
    df['3 sigma']     = df['Best-estimate'] * (1 + 3.000*df['Sigma value [%]'])

    list_time_sec = []
    for t_str in df.index:
        list_time_sec.append(convert_str_sec(t_str, factors_time))
    df['Time steps [s]'] = list_time_sec

    columns_final = ['Time steps [s]'   ,  'Best-estimate',
                     'Sigma value [%]'  ,  '1.645 sigma'  ,
                     '2 sigma'          ,  '3 sigma'       ]

    df = df.reindex(columns=columns_final)

    df['Best-estimate']   = df['Best-estimate']   * 100
    df['Sigma value [%]'] = df['Sigma value [%]'] * 100
    df['1.645 sigma']     = df['1.645 sigma']     * 100
    df['2 sigma']         = df['2 sigma']         * 100
    df['3 sigma']         = df['3 sigma']         * 100

    return df


def create_df_inventories(file_path,        list_units,
                          list_categories,  factors_time,
                          regex_time,       regex_category,
                          regex_categ_unit, regex_after_Decay):
    """Read a single .out file and create a dictionary containing the stored
       data with pandas DataFrames. The dictionary keys represent:
           - 1st key: category ('Elements' or 'Isotopes')
           - 2nd key: unit ('g' for mass, 'Bq' for activity, 'W' for total
             power, 'W_gamma' for gamma power)
       The value of a second key is a pandas DataFrame containing the results
       for every detected time steps and for every detected elements or
       isotopes

       Arguments:
           - file_path (string): absolute location of the file
           - list_units (list): units chosen by the user
           - list_categories (list): categories ('elements' or 'isotopes')
             chosen by the user
           - factors_time (dict): correspondence in seconds for different time
             units
           - regex_* (string): regular expressions

       Returns:
           inv (dict)

    """
    import re
    import pandas as pd
    inv = {}

    if 'Elements' in list_categories:
        inv['Elements'] = {}
    if 'Isotopes' in list_categories:
        inv['Isotopes'] = {}

    ### Regex "nuclides or elements": initially 'None', switches to:
    ### >>>> regex_category['elements'] if category == elements
    ### >>>> regex_category['nuclides'] if category == nuclides
    regex_noe = None

    ### Variable switching to 1 when a block of 'Decay' results is read
    readblock = 0

    ### Open the .out file in read mode and store the lines in a list
    with open(file_path, 'r') as fi:
        read_file = fi.readlines()

    for i, line in enumerate(read_file):

        if (re.search("^\s+Decay ", line)) and\
        (re.search(regex_after_Decay, line)):
            readblock = 1
            ### Search the group of nuclides or elements
            ### Ex: 'fission products', 'actinides' or 'light elements'
            group = find_group(line)
            bloc_res = []

        if readblock == 1 and re.search(regex_categ_unit, line):
            ### Search the category ('elements' or 'nuclides')
            category, unit = find_category_unit(line)
            regex_noe = regex_category[category]

        if readblock == 1 and re.search(regex_time, line):
            ### Read the block of data only if " Decay " has been read
            time_steps = find_times(line)
            for i, t in enumerate(time_steps):
                time_steps[i] = t.replace(" ", "")
            columns_df = ['Group', re.sub("s$", "", category)]
            columns_df.extend(time_steps)

        if readblock == 1 and regex_noe != None:

            if re.search(regex_noe, line) and (unit in list_units) and\
            (category in list_categories) :
                ### Search the list of results for the current bloc of data
                # results[0]: name of the nuclide or element
                # results[i!=0]: result for the corresponding unit and time
                results = find_results(line)
                results[0] = re.sub("\s+", "", results[0]).title()
                if results[0] == "Totals":
                    results[0] = "Total"
                row_res = [group]
                row_res.extend(results)
                bloc_res.append(row_res)

        if (re.search("^\x0c", line)) and (readblock == 1):
            ### Detect the special font at the end of the bloc of data
            # caractherizing the bloc's end: stops data reading
            readblock = 0

            ### End of the bloc of data: an elementary DataFrame based on
            # "bloc_res" matrix (content) and "columns_df" for indices
            if (unit in list_units) and (category in list_categories):
                if unit not in inv[category].keys():
                    inv[category][unit] = []
                df = pd.DataFrame(bloc_res, columns=columns_df)
                inv[category][unit].append(df)

    for k1 in inv.keys():
        for k2 in inv[k1].keys():

            ### inv[k1][k2] is a dataframes list. Concatenate them into one df
            inv[k1][k2] = pd.concat(inv[k1][k2])
            if "Isotope" in inv[k1][k2].columns:
                inv[k1][k2] = inv[k1][k2].groupby(['Group', 'Isotope']).sum()
            if "Element" in inv[k1][k2].columns:
                inv[k1][k2] = inv[k1][k2].groupby(['Group', 'Element']).sum()

            del inv[k1][k2]['initial']
            del inv[k1][k2]['charge']

    return inv


def gather_df_inventories(list_categories, list_units,
                          list_batch_df, FAmass_per_file,
                          nFA_per_file):
    """Gather the pandas DataFrames created by create_df_inventories with the
       corresponding FA mass and number of FA per batch. Create a dictionary
       whose:
           - 1st key is the chosen category(ies): 'Elements' or 'Isotopes'
           - 2nd key is the chosen unit(s)

       Arguments:
           - list_category (list): categories chosen by the user
           - list_units (list): units chosen by the user
           - list_batch_df (list): list of dictionaries returned by
             create_df_inventories
           - FAmass_per_file (list): FA masses chosen by the user per batch
           - nFA_per_file (list): number of FA chosen by the user per batch

       Returns:
           dinv (dict)

    """
    dinv = {}
    for c in list_categories:
        dinv[c] = {}
        for u in list_units:
            dinv[c][u] = list_batch_df[0][c][u]
            dinv[c][u] = dinv[c][u] * FAmass_per_file[0]*\
                         nFA_per_file[0]
            for i, d in enumerate(list_batch_df[1:]):
                df_to_add = d[c][u] * FAmass_per_file[i+1] *\
                            nFA_per_file[i+1]
                dinv[c][u] = dinv[c][u].add(df_to_add, fill_value=0)

    return dinv


def convert_str_sec(word, factors_time):
    """Convert a time step given in a string into a number of seconds.

    Arguments:
        - word (string): time step to convert
        - factors_time (dict): correspondence in seconds for different time
          units

    Returns:
        sec (float): corresponding time in seconds

    Example:
        >>> convert_str_sec("2.0hr", factors_time)
        7200.0

    """

    from re import findall
    if word == 'discharge':
        sec = 0.0
    else:
        sec = float(findall("\d+\.\d+", word)[0]) *\
              factors_time[findall("[a-z]+", word)[0]]

    return sec


def test_df_consistency(list_df):
    """Return True is all the DataFrames in list_df have the same indexes and
    columns.
    NOT USED YET BUT SHOULD.

    """
    df0 = list_df[0]
    ind0 = df0.index
    col0 = df0.columns
    for i, df in enumerate(list_df[1:]):
        ind = df.index
        col = df.columns
        if False in ind0 == ind:
            return False
            continue
        if False in col0 == col:
            return False
            continue
        return True


def find_unc(time_str, dictionary, factors_time):
    """Find the uncertainty value to be used, depending on the time step. If
       time_str (converted from string to float in sec with convert_str_sec)
       does not match any keys in dictionary, the maximum value between the two
       closest keys values is returned

       Arguments:
           - time_str (string): time step of the form "float"+"time_unit"
           - dictionary (dict): uncertainty values corresponding to different
             decay time steps
           - factors_time (dict): correspondence in seconds for different time
             units

       Returns:
           Uncertainty value to be used (float)

       Example:
           >>> find_unc('1.5d', fp_uncertainty, factors_time)
           0.03

    """

    time_sec = convert_str_sec(time_str, factors_time)
    L = sorted(dictionary.keys(), key=lambda x: convert_str_sec(x,
                                                                factors_time))
    for i, key in enumerate(L):
        if (time_sec == convert_str_sec(L[i], factors_time)) or\
           (time_sec < convert_str_sec(L[i], factors_time)):
            uncertainty = dictionary[L[i]]
            break
        if (time_sec > convert_str_sec(L[i], factors_time)) and\
           (time_sec < convert_str_sec(L[i+1], factors_time)):
            uncertainty = max(dictionary[L[i]], dictionary[L[i+1]])
            break
        else:
            continue

    return uncertainty


def get_dict_group_noe(df):
    """Analyze a pandas Dataframe having a two levels index:
           - 1st level: group of isotope or element ("Actinides", "Fission
             products", ..)
           - 2nd level: names of the isotopes or elements

       Argument:
           df (pandas.DataFrame): the two levels indexed DataFrame

       Returns:
           d (dict): dictionary whose keys are the contained group, and values
           are the sorted list of isotopes or elements contained in this group

    """
    d = {}
    L0 = df.index.get_level_values(0)
    L1 = df.index.get_level_values(1)

    for i, e0 in enumerate(L0):
        if e0 not in d.keys():
            d[e0] = []
            d[e0].append(L1[i])
        else:
            d[e0].append(L1[i])

    # Sort the list of elements or isotopes
    for k in d.keys():
        d[k] = sorted(d[k])

    return d


def get_state_IntVar(dictionary, factors_time):
    """Get the state of IntVar instances stored in a dictionary

       Arguments:
           - dictionary (dict): keys are string instances whose values are 0
             or 1
           - factors_time (dict): correspondence in seconds for different time
             units

       Returns:
           The list of the dictionary's keys whose values equal to 1

    """

    list_IntVar1 = []
    for k in sorted(dictionary.keys(),
                    key=lambda x: convert_str_sec(x, factors_time)):
        if dictionary[k].get() == 1:
            list_IntVar1.append(k)
    return list_IntVar1


def check_input_output(in_loc, out_loc):
    """Check if ../Input and ../Output folders exist, and get all the available
       .out files in ../Input folder
       
       Arguments:
           - in_loc (string): absolute location of ../Input folder
           - out_loc (string): absolute location of ../Output folder
       
       Returns:
           list_in_files (list): absolute location of available .out files in
           ../Input folder
           
    """
    import os.path
    from os import mkdir
    import glob
    import sys

    # Check if 'Input' folder exists
    if os.path.isdir(in_loc):
        list_in_files = [f for f in glob.glob(os.path.join(in_loc, '*.out'))]

        # If empty, restart needed
        if list_in_files == []:
            msg = ("\nWarning, the following folder:\n{}\ndoes not contain any"
                   " \".out\" file. The files you want to post-treat need to "
                   "be placed in it. Please restart.".format(in_loc))
            print(msg)
            sys.exit(0)

    if not os.path.exists(in_loc):
        msg = ("\nWarning, the following folder doesn't exist:\n{}\nIt is now "
               "created and empty. The files you want to post-treat need to "
               "be placed in it. Please restart.".format(in_loc))
        os.mkdir(in_loc)
        print(msg)
        sys.exit(0)

    # Also check if 'Output' folder exists. If not, create it
    if not os.path.exists(out_loc):
        os.mkdir(out_loc)
        msg = ("\nThe following folder doesn't exist:\n{}\nCreation of this "
               "folder, where your resulting files will be located."\
               .format(out_loc))
        print(msg)
    
    return list_in_files

"""def plot_inventory(di, category, unit, group, list_noe):
    Plot evolution of isotope or nuclide over decay time.

    import re
    import matplotlib.pyplot as plt
    from functions_dict import convert_str_sec, factors_time
    # "di" comes from create_df_inventories, needs a bit of preparation
    d = di[category][unit]

    # Reset index
    d = d.reset_index()

    # Drop "Totals" in "Elements" category
    if category == 'Elements':
        d = d[d['Element'] != 'Totals']

    # Target the "group" group
    d = d[d['Group'] == group]

    # Delete the "Group name" feature
    del d['Group']

    # Set index on noe name
    d = d.set_index(re.sub('s$', ' ', category)+'name')
    d.columns.name = 'Time'

    # Transpose the dataframe
    d = d.T.reset_index()
    d['Time [s]'] = d['Time'].apply(lambda t: convert_str_sec(t, factors_time))
    del d['Time']
    d = d.set_index('Time [s]').sort_index()

    # Finally plot
    t = 'Title'
    d[list_noe].plot(logx=1, logy=0, title=t, grid=1, subplots=1)
    plt.show()"""

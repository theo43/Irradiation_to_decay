# -*- coding: utf-8 -*-
"""
@author: theo43
date: Sept. 2017
POS: functions
"""

def find_group(line):
    """Post-process the name of the group of nuclides or elements ("actinides",
       "fission products" or "light elements")

       Argument:
           line (string): line of a .out file to post-process

       Returns:
           group (string): group of the isotope or element

       Example:
           >>> find_group("  Decay from 11 h to 20 h    actinides   page  533")
           'Actinides'
    """
    from re import search
    group ='NA'
    if search("fission products", line):
        group = "Fission products"
    if search("actinides", line):
        group = "Actinides"
    if search("light elements", line):
        group = "Light elements"

    return group


def find_category_unit(line):
    """Post-process the category of results: "nuclides" or "elements" and the
       unit of the results:
           - "g" for mass in grams
           - "bq" for radioactivity in Bq (1 Cu = 3.7x10^10 Bq)
               (Curies results given in .out files are converted in Bq)
           - "wt" for total thermal power in watts
           - "wg" for gamma contribution in total power, in watts

       Argument:
           line (string): line of a .out file to post-process

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
        unit = "bq"
    if search("thermal power, watts", line):
        unit = "wt"
    if search("gamma power, watts", line):
        unit = "wg"
    if search(" element ", line):
        category = "Elements"
    if search(" nuclide ", line):
        category = "Isotopes"
    tup = (category, unit)

    return tup


def find_times(line):
    """Post-process the time steps of the block of data being read. Time steps
       are given with the following form: "float"+"unit". If the time step
       value is given in:
            - Seconds: no space between the float and "sec"
            - Minutes: to be completed
            - Hours: one space between the float and "hr"
            - Days: one space between the float and "d"
            - Months: to be completed
            - Years: one space between the float and "yr"

       Argument:
           line (string): line of a .out file to post-process

       Returns:
           time_steps (list): split of the line containing the time steps

       Example:
           >>> find_times("             initial   11.0 hr   12.0 hr ")
           ['initial', '11.0 hr', '12.0 hr']

    """
    from re import findall
    time_steps = findall(r"[a-z]+|\d+\.\d{,2}\s?[secdhryr]{1,3}", line)
    return time_steps


def find_results(line):
    """Post-process the results in [unit] of a block of data being read

       Argument:
           line (string): line of a .out file to post-process

       Returns:
           - results (list): split of the line containing the results. The
             first element of the list is the isotope or element name (string),
             the rest is the resulting contribution (float)

       Example:
           >>> find_results("    am239   2.90E-18  4.44E-09  4.44E-09  ")
           ['am239', 2.9e-18, 4.44e-09, 4.44e-09]

    """
    from re import findall
    results = findall(r"[a-z]{1,6}\s{,2}\d{,3}m?|\d\.\d{2}E[+-]\d{2}", line)
    for i, r in enumerate(results[1:]):
        results[i+1] = float(r)

    return results


def create_df_decay_power(file_path,
                          factors_time,
                          regex_time,
                          regex_category,
                          regex_categ_unit,
                          regex_after_Decay):
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

    from re import search
    from pandas import DataFrame, Series

    # Regex "nuclides or elements": initially 'None', switches to:
    #   regex_category['elements'] if category == elements;
    #   regex_category['nuclides'] if category == nuclides.
    regex_noe = None

    # Variable switching to 1 when a block of 'Decay' results is read.
    readblock = 0

    # Create the DataFrame containing the results
    df = DataFrame()
    df.columns.name = 'Time steps'
    df.index.name = 'Contributions'

    # Open the .out file in read mode and store the lines in a list
    with open(file_path, 'r') as fi:
        read_file = fi.readlines()

    for i, line in enumerate(read_file):

        if search(r"^\s+Decay ", line) and\
        (search(regex_after_Decay, line)):
            readblock = 1
            # Search the group of nuclides or elements
            # Ex: 'fission products', 'actinides' or 'light elements'
            group = find_group(line)

        if readblock == 1 and search(regex_categ_unit, line):
            # Search the category ('elements' or 'nuclides')
            category, unit = find_category_unit(line)
            regex_noe = regex_category[category]

        if readblock == 1 and search(regex_time, line):
            # Read the block of data only if " Decay " has been read
            time_steps = find_times(line)
            for i, t in enumerate(time_steps):
                time_steps[i] = t.replace(" ", "")

        if readblock == 1 and regex_noe != None:

            if search(regex_noe, line) and unit == 'wt':
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
                    se = Series(results[1:],
                                index=time_steps,
                                name=NOE.title())
                    df = df.append(se)

                if cond2 == True:
                    se = Series(results[1:],
                                index=time_steps,
                                name=group)
                    df = df.append(se)

        if search("^\x0c", line) and readblock == 1:
            # Detect the special font at the end of the bloc of data
            # caractherizing the bloc's end: stops data reading
            readblock = 0

    df = df.groupby(df.index).sum()
    del df['initial']
    del df['charge']
    columns = sorted(df.columns,
                     key=lambda x: convert_str_sec(x, factors_time))
    df = df.reindex(columns=columns)
    df = df.T
    df['Total (BE)'] = df['Actinides']+df['Fission products']

    return df


def gather_df_decay_power(list_batch_df, FAmass_per_file,
                          nFA_per_file, core_power,
                          mox, act_u9_np9_uncertainty,
                          u9_np9_uncertainty, fp_uncertainty,
                          fuel_uncertainty, factors_time):
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
    df['u9_np9_unc'] = nan
    df['fp_unc'] = nan
    df['sig_uo2'] = nan

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

    columns_final = ['Time steps [s]',
                     'Best-estimate',
                     'Sigma value [%]',
                     '1.645 sigma',
                     '2 sigma',
                     '3 sigma']

    df = df.reindex(columns=columns_final)

    df['Best-estimate']   = df['Best-estimate']   * 100
    df['Sigma value [%]'] = df['Sigma value [%]'] * 100
    df['1.645 sigma']     = df['1.645 sigma']     * 100
    df['2 sigma']         = df['2 sigma']         * 100
    df['3 sigma']         = df['3 sigma']         * 100

    return df




def create_df_inventories(file_path,
                          list_units,
                          list_categories,
                          factors_time,
                          regex_time,
                          regex_category,
                          regex_categ_unit,
                          regex_after_Decay):
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
    from re import search, sub
    import pandas as pd
    inv = {}

    if 'Elements' in list_categories:
        inv['Elements'] = {}
    if 'Isotopes' in list_categories:
        inv['Isotopes'] = {}

    # Regex "nuclides or elements": initially 'None', switches to:
    # >>>> regex_category['elements'] if category == elements
    # >>>> regex_category['nuclides'] if category == nuclides
    regex_noe = None

    # Variable switching to 1 when a block of 'Decay' results is read
    readblock = 0

    # Open the .out file in read mode and store the lines in a list
    with open(file_path, 'r') as fi:
        read_file = fi.readlines()

    for i, line in enumerate(read_file):

        if (search(r"^\s+Decay ", line)) and\
        (search(regex_after_Decay, line)):
            readblock = 1
            # Search the group of nuclides or elements
            # Ex: 'fission products', 'actinides' or 'light elements'
            group = find_group(line)
            bloc_res = []

        if readblock and search(regex_categ_unit, line):
            # Search the category ('elements' or 'nuclides')
            category, unit = find_category_unit(line)
            regex_noe = regex_category[category]

        if readblock and search(regex_time, line):
            # Read the block of data only if " Decay " has been read
            time_steps = find_times(line)
            for i, t in enumerate(time_steps):
                time_steps[i] = t.replace(" ", "")
            columns_df = ['Group', sub("s$", "", category)]
            columns_df.extend(time_steps)

        if readblock and regex_noe != None:

            if search(regex_noe, line) and (unit in list_units) and\
            (category in list_categories):
                # Search the list of results for the current bloc of data
                # results[0]: name of the nuclide or element
                # results[i!=0]: result for the corresponding unit and time
                results = find_results(line)
                results[0] = sub(r"\s+", "", results[0]).title()
                if results[0] == "Totals":
                    results[0] = "Total"

                # Information: radioactivity results in .out files are provided
                # in curies, not becquerels. The conversion is not done here
                # as it is much more efficient to convert directly an entire
                # pandas DataFrame: see gather_df_inventories function

                # Build the bloc results
                row_res = [group]
                row_res.extend(results)
                bloc_res.append(row_res)

        if (search("^\x0c", line)) and readblock:
            # Detect the special font at the end of the bloc of data
            # caractherizing the bloc's end: stops data reading
            readblock = 0

            # End of the bloc of data: an elementary DataFrame based on
            # "bloc_res" matrix (content) and "columns_df" for indices
            if (unit in list_units) and (category in list_categories):
                if unit not in inv[category].keys():
                    inv[category][unit] = []
                df = pd.DataFrame(bloc_res, columns=columns_df)
                inv[category][unit].append(df)

    for c in inv.keys():
        for u in inv[c].keys():
            # inv[k1][k2] is a dataframes list. Concatenate them into one df
            inv[c][u] = pd.concat(inv[c][u])
            if "Isotope" in inv[c][u].columns:
                inv[c][u] = inv[c][u].groupby(['Group', 'Isotope']).sum()
            if "Element" in inv[c][u].columns:
                inv[c][u] = inv[c][u].groupby(['Group', 'Element']).sum()

            del inv[c][u]['initial']
            del inv[c][u]['charge']

    return inv


def gather_df_inventories(list_categories,
                          list_units,
                          list_batch_df,
                          FAmass_per_file,
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
            # Convert curies to becquerels
            # Radioactivity results in .out files are initially in Cu
            # 1 cu = 3.7E10 bq
            if u == 'bq':
                dinv[c][u] = dinv[c][u] * 3.7E10

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
        sec = float(findall(r"\d+\.\d+", word)[0]) *\
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


def get_dict_group_ioe(df):
    """Analyze a pandas Dataframe having a two levels index:
           - 1st level: group of isotope or element ("Actinides", "Fission
             products", ..)
           - 2nd level: names of the isotopes or elements

       Argument:
           df (pandas.DataFrame): the two levels indexed DataFrame

       Returns:
           di (dict): dictionary whose keys are the contained group, and values
           are the sorted list of isotopes or elements contained in this group

    """
    di = {}
    L0 = df.index.get_level_values(0)
    L1 = df.index.get_level_values(1)

    for i, e0 in enumerate(L0):
        if e0 not in di.keys():
            di[e0] = []
            di[e0].append(L1[i])
        else:
            di[e0].append(L1[i])

    # Sort the list of elements or isotopes
    for k in di.keys():
        di[k] = sorted(di[k])

    return di


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
    from os import mkdir, path
    import glob
    import sys

    # Check if 'Input' folder exists
    if path.isdir(in_loc):
        list_in_files = [f for f in glob.glob(path.join(in_loc, '*.out'))]

        # If empty, restart needed
        if list_in_files == []:
            msg = ("\nWarning, the following folder:\n{}\ndoes not contain any"
                   " \".out\" file. The files you want to post-process need to "
                   "be placed in it. Please restart.".format(in_loc))
            print(msg)
            sys.exit(0)

    if not path.exists(in_loc):
        msg = ("\nWarning, the following folder doesn't exist:\n{}\nIt is now "
               "created and empty. The files you want to post-process need to "
               "be placed in it. Please restart.".format(in_loc))
        mkdir(in_loc)
        print(msg)
        sys.exit(0)

    # Also check if 'Output' folder exists. If not, create it
    if not path.exists(out_loc):
        mkdir(out_loc)
        msg = ("\nThe following folder doesn't exist:\n{}\nCreation of this "
               "folder, where your resulting files will be located."\
               .format(out_loc))
        print(msg)

    return list_in_files


def create_df_info(**kwargs):
    """Build a list containing the information chosen by the user to be
       inserted in a Dataframe

       Arguments:
           **kwargs (dict):

       Returns:
           df_info (pandas.DataFrame)

    """

    from os import path
    from pandas import DataFrame

    info = []
    info.append([path.basename(f) for f in kwargs["chosen_files"]])
    info.append(kwargs["FAmass_per_file"])
    info.append(kwargs["nFA_per_file"])
    info.append(kwargs["chosen_files"])

    df_info = DataFrame(info,
                        index=['File name',
                               'FA mass (tons)',
                               'Number of FA',
                               'File location'])
    df_info = df_info.T.groupby(['File name']).sum()

    return df_info


def write_results(output_location,
                  results_type,
                  suffix,
                  dict_results,
                  df_user_data,
                  **kwargs):
    """Check if the sub-folder corresponding to the required results type
       exists, and create it if it does not. Create the results file

       Arguments:
           - output_location (str):
           - results_type (str): name of the sub-folder for results
             ("Decay_power_curve" or "Source_terms")
           - suffix (str): suffix of the results file name
             asked by the user appended to results file name
           - dict_results (dict): contains the pandas DataFrames to be printed
             in the result file:
                 - 1st key: results_type
                 - 2nd key: categories (only for source terms)
                 - 3rd key: units (only for source terms)
             For decay power curve generation: dict_results is directly a
             pandas.DataFrame
           - df_user_data (pandas.DataFrame): data provided by the user in
             UserData
           - **kwargs (dict): only for source terms results
                 - index_group_ioe (list): tuples containing (group, isotope or
                   element) names for source terms result file indexing
                 - time_steps (list): time steps names for columns indexing
                 - category (str): category for source terms results
                 - factors_time (dict): amount of seconds in different units of
                   time

       Returns:
           list_title_msg (list): tuple(s) of title (str), msg (str) to be
           displayed in a messagebox

    """

    from pandas import ExcelWriter
    from os import path, mkdir

    list_title_msg = []

    # Check if the folder inside the one containing the .out files exists
    folder = path.join(output_location, "POS_results")
    if not path.exists(folder):
        title = "Info: folder creation"
        msg = "Folder {} does not exist, it is created".format(folder)
        list_title_msg.append((title, msg))
        mkdir(folder)

    # Check if the sub-folder already exists in "POS" folder
    folder = path.join(folder, results_type)
    if (not path.exists(folder)) or\
       (path.exists(folder) and (not path.isdir(folder))):
        title = "Info: folder creation"
        msg = "Folder {} does not exist, it is created".format(folder)
        list_title_msg.append((title, msg))
        mkdir(folder)

    # Write the output file in Excel format
    if results_type == "Source_terms":  # Source terms file creation

        # Unit names for result file sheet names
        dict_unit = {
            'wt': 'watts_total',
            'wg': 'watts_gamma',
            'g': 'grams',
            'bq': 'becquerels'
        }

        index_group_ioe = kwargs['index_group_ioe']
        time_steps = kwargs['time_steps']
        factors_time = kwargs['factors_time']
        time_steps = sorted(time_steps,
                            key=lambda x: convert_str_sec(x, factors_time))
        category = kwargs['category']

        file_name = results_type + "_" + category.lower()
        file_name += "_" + suffix + ".xlsx"
        file_name = path.join(folder, file_name)
        writer = ExcelWriter(file_name)
        df_user_data.to_excel(writer, "user_data")

        for unit in sorted(dict_results[category].keys()):
            df = dict_results[category][unit]
            df = df.reindex(index=index_group_ioe, columns=time_steps)
            name = dict_unit[unit]
            df.to_excel(writer, name)

    else:  # Decay power curve file creation
        file_name = results_type + "_" + suffix + ".xlsx"
        file_name = path.join(folder, file_name)
        writer = ExcelWriter(file_name)
        df_user_data.to_excel(writer, "user_data")
        dict_results.to_excel(writer, results_type.lower())

    writer.save()

    title = "Info: results file creation"
    msg = "Creation of:\n{}".format(file_name)
    list_title_msg.append((title, msg))

    return list_title_msg

# -*- coding: iso-8859-1 -*-
# -*- encoding: iso8859-1 -*-
# Author: theo43@github

##############################################################################
### REGULAR EXPRESSIONS    
##############################################################################

### Regular expressions allowing getting time steps and results in blocks
# 1. For time steps research
regex_time = "^\s+(charge\s+discharge|initial)\s+\d+\.\d?\s?[sechrdyr]"
# 2. For category ('elements' or 'nuclides') research
regex_category = {
    # For 'Elements' category. Gets the "totals"
    'Elements': "^\s+([a-z]{,2}|totals)\s+\d\.\d{2}E[+-]\d{2}",
    # For 'Isotopes' category. Does not get "total"
    'Isotopes': "^\s+[a-z]{1,2}\s{0,2}\d{1,3}[m]?\s+\d\.\d{2}E[+-]\d{2}"
}
### Regular expression to detect category and unit
reg_categ_unit = "concentrations, grams|radioactivity, curies|thermal"
reg_categ_unit += " power, watts|gamma power, watts"
### Regular expression matching groups only
reg_after_Decay = "actinides|fission products|light elements"

##############################################################################
### DICTIONARIES    
##############################################################################

### Dictionnary containing the conversion factor between different
# time units and seconds.
factors_time = {
    'sec': 1.,
    'min': 60., # WARNING: minutes not yet considered in find_times
    'hr': 3600.,
    'd': 24. * 3600.,
    'yr': 365 * 24. * 3600.
}

fp_uncertainty = {
    '0.1sec':          0.079,
    '1.0sec':          0.079,
    '10.0sec':         0.072,
    '100.0sec':        0.072,
    '300.0sec':        0.06,
    '600.0sec':        0.06,
    '1800.0sec':       0.04,
    '1.0hr':           0.04,
    '2.0hr':           0.04,
    '5.0hr':           0.03,
    '10.0hr':          0.03,
    '1.0d':            0.03,
    '2.0d':            0.025,
    '4.0d':            0.025,
    '8.0d':            0.025,
    '15.0d':           0.025,
    '30.0d':           0.025,
    '90.0d':           0.025,
    '180.0d':          0.025,
    '270.0d':          0.025,
    '1.0yr':           0.025,
    '1.25yr':          0.025,
    '1.5yr':           0.025,
    '2.0yr':           0.025,
    '3.0yr':           0.025,
    '5.0yr':           0.025,
    '10.0yr':          0.025,
    '50.0yr':          0.025,
    '100.0yr':         0.025,
    '10000.0yr':       0.025
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
    '0.1sec':          0.06,
    '1.0sec':          0.06,
    '10.0sec':         0.06,
    '100.0sec':        0.06,
    '300.0sec':        0.06,
    '600.0sec':        0.06,
    '1800.0sec':       0.06,
    '1.0hr':           0.06,
    '2.0hr':           0.06,
    '5.0hr':           0.06,
    '10.0hr':          0.06,
    '1.0d':            0.06,
    '2.0d':            0.06,
    '4.0d':            0.06,
    '8.0d':            0.06,
    '15.0d':           0.06,
    '30.0d':           0.06,
    '90.0d':           0.00,
    '10000.0yr':       0.00
}

fuel_uncertainty = {
    'UO2': {
        '0.1sec':        0.075,
        '1.0sec':        0.074,
        '10.0sec':       0.067,
        '100.0sec':      0.064,
        '300.0sec':      0.053,
        '600.0sec':      0.052,
        '1800.0sec':     0.035,
        '1.0hr':         0.035,
        '2.0hr':         0.035,
        '5.0hr':         0.027,
        '10.0hr':        0.027,
        '1.0d':          0.027,
        '2.0d':          0.024,
        '4.0d':          0.024,
        '8.0d':          0.025,
        '15.0d':         0.026,
        '30.0d':         0.026,
        '90.0d':         0.028,
        '180.0d':        0.028,
        '270.0d':        0.027,
        '1.0yr':         0.027,
        '1.25yr':        0.026,
        '1.5yr':         0.025,
        '2.0yr':         0.025,
        '3.0yr':         0.024,
        '5.0yr':         0.024,
        '10.0yr':        0.025,
        '50.0yr':        0.047,
        '100.0yr':       0.076,
        '10000.0yr':     0.076
    },
    'MOX': {
        '0.1sec':        0.075,
        '1.0sec':        0.074,
        '10.0sec':       0.067,
        '100.0sec':      0.064,
        '300.0sec':      0.053,
        '600.0sec':      0.052,
        '1800.0sec':     0.035,
        '1.0hr':         0.035,
        '2.0hr':         0.035,
        '5.0hr':         0.027,
        '10.0hr':        0.027,
        '1.0d':          0.027,
        '2.0d':          0.024,
        '4.0d':          0.024,
        '8.0d':          0.025,
        '15.0d':         0.026,
        '30.0d':         0.026,
        '90.0d':         0.028,
        '180.0d':        0.028,
        '270.0d':        0.027,
        '1.0yr':         0.027,
        '1.25yr':        0.026,
        '1.5yr':         0.025,
        '2.0yr':         0.025,
        '3.0yr':         0.024,
        '5.0yr':         0.024,
        '10.0yr':        0.025,
        '50.0yr':        0.047,
        '100.0yr':       0.076,
        '10000.0yr':     0.076
    }
}

### Correspondance between units and units for printing (source terms printing)                   
dict_unit = {
    'W': 'watts',
    'W_gamma': 'watts_gamma',
    'g': 'grams',
    'Bq': 'becquerels'
}

##############################################################################
### FUNCTIONS    
##############################################################################

def find_group(line):
    """
    Return the name of the group of nuclides or elements:
    'actinides', 'fission products' or 'light elements'.
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

##############################################################################

def find_category_unit(line):
    """ 
    Return the category of results: 'nuclides' or 'elements' as
    first argument.
    The second argument returned is the unit of the results:
            * 'g' for mass in grams;
            * 'Bq' for radioactivity in Bq (1 Cu = 3.7x10^10 Bq);
               >>> outputfile2dictionary automatically converts Cu to Bq <<<
            * 'W' for total thermal power in watts;
            * 'W_gamma' for gamma contribution in total power, in watts.
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
    return category, unit

##############################################################################

def find_times(line):
    """ 
    Return the time steps of the block of data being read.
    In OrigenS.out files, if the time step value is given in:
            * Seconds: no space between the float number and 'sec';
            * Minutes: ?? to be completed
            * Hours: one space between the float number and 'hr';
            * Days: one space between the float number and 'd';
            * Months: ?? to be completed
            * Years: one space between the float number and 'yr';
    """
    from re import findall
    time_steps = findall("[a-z]+|\d+\.\d{,2}\s?[secdhryr]{1,3}", line)
    return time_steps

##############################################################################

def find_results(line):
    """ 
    Return the results in [unit] of a block of data being read.
    """
    from re import findall
    results = findall("[a-z]{1,6}\s{,2}\d{,3}m?|\d\.\d{2}E[+-]\d{2}", line)
    for i, r in enumerate(results[1:]):
        results[i+1] = float(r)
    return results

##############################################################################

def create_df_inventories(file_path, list_units, list_categories,
                          factors_time, regex_time, regex_category,
                          reg_categ_unit, reg_after_Decay):
    """
    Read an Origen-S.out file, return a dictionary containing the stored data
    in the following order:
    * 1st key: category ('Elements' or 'Isotopes');
    * 2nd key: unit ('g' for mass, 'Bq' for activity, 'W' for total power,
                    'W_gamma' for gamma power);
    The 2nd key values are a DataFrame containing the results for time steps,
    group, isotope or element name.
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

    ### Open the OrigenS.out file in read mode and store the lines in a list
    with open(file_path, 'r') as fi:
        read_file = fi.readlines()

    for i, line in enumerate(read_file):
        
        if (re.search("^\s+Decay ", line)) and\
        (re.search(reg_after_Decay, line)):
            readblock = 1
            ### Search the group of nuclides or elements
            ### Ex: 'fission products', 'actinides' or 'light elements'
            group = find_group(line)
            bloc_res = []
        
        if readblock == 1 and re.search(reg_categ_unit, line):
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

##############################################################################

def create_df_decay_power(file_path, factors_time, regex_time, regex_category,
                          reg_categ_unit, reg_after_Decay):
    """
    Read an Origen-S.out file, return a DataFrame containing the results for
    time steps (columns), and the following contribution (index):
    * Total decay power (best-estimate)  
    * Actinides (without 239U and 239Np)
    * 239U and 239 Np
    * Fission products
    """
    import re
    import pandas as pd

    ### Regex "nuclides or elements": initially 'None', switches to:
    ### >>>> regex_category['elements'] if category == elements;
    ### >>>> regex_category['nuclides'] if category == nuclides.
    regex_noe = None

    ### Variable switching to 1 when a block of 'Decay' results is read.
    readblock = 0
    
    ### Create the DataFrame containing the results
    df = pd.DataFrame()
    df.columns.name = 'Time steps'
    df.index.name = 'Contributions'

    ### Open the OrigenS.out file in read mode and store the lines in a list
    with open(file_path, 'r') as fi:
        read_file = fi.readlines()

    for i, line in enumerate(read_file):

        if re.search("^\s+Decay ", line) and\
        (re.search(reg_after_Decay, line)):
            readblock = 1
            ### Search the group of nuclides or elements
            ### Ex: 'fission products', 'actinides' or 'light elements'
            group = find_group(line)
        
        if readblock == 1 and re.search(reg_categ_unit, line):
            ### Search the category ('elements' or 'nuclides')
            category, unit = find_category_unit(line)
            regex_noe = regex_category[category]

        if readblock == 1 and re.search(regex_time, line):
            ### Read the block of data only if " Decay " has been read
            time_steps = find_times(line)
            for i, t in enumerate(time_steps):
                time_steps[i] = t.replace(" ", "")

        if readblock == 1 and regex_noe != None:

            if re.search(regex_noe, line) and unit == 'W':
                ### Search the list of results for the current bloc of data
                # results[0]: name of the nuclide or element
                # results[i!=0]: result for the corresponding unit and time
                results = find_results(line)

                ### 'NOE': Nuclide Or Element name, without space(s) in it
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
            ### Detect the special font at the end of the bloc of data
            # caractherizing the bloc's end: stops data reading
            readblock = 0

    df = df.groupby(df.index).sum()
    del df['initial']
    del df['charge']
    df = df.reindex(columns=sorted(df.columns,
                                   key=lambda x: convert_str_sec(x,
                                                                factors_time)))
    df = df.T
    df['Total (BE)'] = df['Actinides']+df['Fission products']
    return df

##############################################################################
  
def convert_str_sec(word, factors):
    """
    Convert a time step given in a string into a number of seconds.
    """
    from re import findall
    if word == 'discharge':
        sec = 0.0
    else:
        sec = float(findall("\d+\.\d+", word)[0]) *\
              factors[findall("[a-z]+", word)[0]]
    
    return sec

##############################################################################

def test_df_consistency(list_df):
    """
    Return True is all the DataFrames in list_df have the same indexes and
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

##############################################################################

def gather_df(list_batch_df,            FA_mass,
              n_FA_batch,               list_names,
              core_power,               mox,
              act_u9_np9_uncertainty,   u9_np9_uncertainty,
              fp_uncertainty,           fuel_uncertainty,
              factors):
    """
    Gather the DataFrames listed in list_batch_df, taking into account the
    number of FA per batch, the FA mass.
    Calculate the resulting BE power, sigma value.
    Return a DataFrame containing the time steps chosen by the user (index),
    the BE power, and with 1.645, 2 and 3 sigma (all power value given in %FP.
    """
    from pandas import DataFrame
    from numpy import nan, sqrt
    
    df = DataFrame()
    
    for i, d in enumerate(list_batch_df):
        df = df.add(d*FA_mass[i]*n_FA_batch[i], fill_value=0)
    
    df['Act-(U9+Np9)'] = df['Actinides'] - df['U239'] - df['Np239']
    df['%Act-(U9+Np9)'] = df['Act-(U9+Np9)'] / df['Total (BE)']
    df['%(U9+Np9)'] = (df['U239']+df['Np239']) / df['Total (BE)']
    df['%FP'] = df['Fission products'] / df['Total (BE)']
    df['Best-estimate [%FP]'] = df['Total (BE)'] / (core_power*1000000)
    
    df['act_u9_np9_unc'] = nan
    df['u9_np9_unc'] = nan
    df['fp_unc'] = nan
    df['sig_uo2'] = nan
    if mox == 1:
        df['sig_mox'] = nan
        
    for i in df.index:
        df['act_u9_np9_unc'][i] = find_unc(i, act_u9_np9_uncertainty, factors)
        df['u9_np9_unc'][i] = find_unc(i, u9_np9_uncertainty, factors)
        df['fp_unc'][i] = find_unc(i, fp_uncertainty, factors)
        df['sig_uo2'][i] = find_unc(i, fuel_uncertainty['UO2'], factors)
        if mox == 1:
            df['sig_mox'][i] = find_unc(i, fuel_uncertainty['MOX'], factors)
    
    df['sigma_calc'] = sqrt(df['%Act-(U9+Np9)']**2 * df['act_u9_np9_unc'] **2
                      + df['%(U9+Np9)']**2   * df['u9_np9_unc'] **2
                      + df['%FP']**2         * df['fp_unc'] **2 )\
                    / (df['%Act-(U9+Np9)'] + df['%(U9+Np9)'] + df['%FP'])
    
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
    
    df['1.645 sigma [%FP]'] = df['Best-estimate [%FP]'] *\
                              (1 + 1.645 * df['Sigma value [%]'])
    df['2 sigma [%FP]'] = df['Best-estimate [%FP]'] *\
                          (1 + 2.0 * df['Sigma value [%]'])
    df['3 sigma [%FP]'] = df['Best-estimate [%FP]'] *\
                          (1 + 3.0 * df['Sigma value [%]'])
    
    list_time_sec = []
    for t_str in df.index:
        list_time_sec.append(convert_str_sec(t_str, factors))
    df['Time steps [s]'] = list_time_sec
    
    columns_final = ['Time steps [s]'  ,  'Best-estimate [%FP]',
                     'Sigma value [%]' ,  '1.645 sigma [%FP]',
                     '2 sigma [%FP]'   ,  '3 sigma [%FP]']
    df = df.reindex(columns=columns_final)
    df['Best-estimate [%FP]'] = df['Best-estimate [%FP]']*100
    df['Sigma value [%]'] = df['Sigma value [%]']*100
    df['1.645 sigma [%FP]'] = df['1.645 sigma [%FP]']*100
    df['2 sigma [%FP]'] = df['2 sigma [%FP]']*100
    df['3 sigma [%FP]'] = df['3 sigma [%FP]']*100
    return df   

############################################################################## 

def find_unc(time_str, dictionary, factors):
    """
    Find the uncertainty value to be used, depending on the time step.
    """
    time_sec = convert_str_sec(time_str, factors)
    L = sorted(dictionary.keys(), key=lambda x: convert_str_sec(x, factors))
    for i, key in enumerate(L):
        if (time_sec == convert_str_sec(L[i], factors)) or\
           (time_sec < convert_str_sec(L[i], factors)):
            uncertainty = dictionary[L[i]]
            break
        if (time_sec > convert_str_sec(L[i], factors)) and\
           (time_sec < convert_str_sec(L[i+1], factors)):
            uncertainty = max(dictionary[L[i]], dictionary[L[i+1]])
            break
        else:
            continue
    return uncertainty

##############################################################################

def get_dict_group_noe(df):
    """
    Return a dictionary from a dataframe, whose first key represents the
    groups. The corresponding values are a list of isotopes or elements
    available for this group.
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
    for k in d.keys():
        d[k] = sorted(d[k])
    return d

##############################################################################

def get_state_IntVar(dictionary, factors):
    """
    Get the state IntVar instances stored in a dictionary.
    """
    list_IntVar1 = []
    for k in sorted(dictionary.keys(),
                    key=lambda x: convert_str_sec(x, factors)):
        if dictionary[k].get() == 1:
            list_IntVar1.append(k)
    return list_IntVar1

##############################################################################

def plot_inventory(di, category, unit, group, list_noe):
    """
    Plot evolution of isotope or nuclide over decay time.
    """
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
    plt.show()

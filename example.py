__author__ = 'marcos'
import analysis
import pandas as pd
import numpy as np
import re

models = {'lognormal_delta_fixed': analysis.LogNormalFixedDAnalysis,
          'lognormal_delta_fixed_beta_fixed': analysis.LogNormalFixedDFixedBetaAnalysis,
          'lognormal': analysis.LogNormalAnalysis,
          'lognormal_beta_fixed': analysis.LogNormalFixedBetaAnalysis,
          'gaussian_delta_fixed': analysis.FixedDAnalysis,
          'gaussian_delta_fixed_beta_fixed': analysis.FixedDFixedBetaAnalysis,
          'gaussian': analysis.ConstrainedDAnalysis,
          'gaussian_beta_fixed': analysis.ConstrainedDFixedBetaAnalysis,
          'person': analysis.PopulationAnalysis}

df_15 = pd.read_excel("~/Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2015.xls", "15tbl08")
states = list(df_15.State)
states_index = [k for k in range(len(states)) if type(states[k]) == unicode]
states_correction = list(np.concatenate([[states[states_index[i]]]*(states_index[i+1] - states_index[i]) for i in range(len(states_index) - 1)]))
states_correction += [states[states_index[-1]]]*(len(states)-states_index[-1])
df_15['State'] = states_correction
df_15['City'] = map(lambda x: re.sub("[0-9]*", "", x), df_15.City)

types = ["Larceny-\ntheft", "Burglary", "Robbery", "Violent\ncrime", "Rape\n(legacy\ndefinition)2", 'Rape\n(revised\ndefinition)1', 'Property\ncrime', 'Motor\nvehicle\ntheft', 'Arson3', 'Aggravated\nassault', 'Murder and\nnonnegligent\nmanslaughter']

for typec in types:
    print typec
    df_15_ = df_15[df_15['Population'] > 10]
    df_15_ = df_15_[df_15_[typec] > 1]
    x = np.array(map(float, df_15_['Population']))
    y = np.array(map(float, df_15_[typec]))
    x = x[~pd.isnull(y)]
    y = y[~pd.isnull(y)]
    data_xy = x, y
    for m, model in models.items():
        line = typec.replace("\n", " ") + ","
        r = model(data_xy, required_successes=8)
        line += "%s," % m.description
        line += ",".join(map(str, r.beta)) + ","
        line += "%f," % r.bic
        line += "%f" % r.p_value
        print line

# df_14 = pd.read_excel("/home/marcos/Downloads/table-8.xls", "14tbl08")
# df_14 = df_14[~pd.isnull(df_14['City'])]
# states = list(df_14.State)
# states_index = [k for k in range(len(states)) if type(states[k]) == unicode]
# states_correction = list(np.concatenate([[states[states_index[i]]]*(states_index[i+1] - states_index[i]) for i in range(len(states_index) - 1)]))
# states_correction += [states[states_index[-1]]]*(len(states)-states_index[-1])
# df_14['State'] = states_correction
# df_14['City'] = map(lambda x: re.sub("[0-9]*", "", x), df_14.City)
# df_2LA = df_15.merge(df_14, how="left", on=["State", "City"])
# df_2LA.columns

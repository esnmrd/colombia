#%% [markdown]
# ## Visualization of emission and traffic volume observations
# ### Ehsan Moradi, Ph.D. Candidate

#%% [markdown]
# ### Load required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn import preprocessing
import itertools

plt.rcParams["axes.grid"] = True

#%% [markdown]
# ### General settings
features = ["VolEq", "VolMC", "VolPC", "VolLT", "VolHT"]
dependents = ["AvgBC", "Dust"]
extra = ["DayOfWeek", "TimeWindow", "PeakState"]
neighbourhoods = ["La Concordia", "La Joya", "La Provenza", "La AltoViento"]

#%% [markdown]
# ### Loading observations from Excel into a pandas dataframe
dir = r"/Users/ehsan/Dropbox/Academia/Colombia Project/Data"
file = r"/Neighbourhoods - Traffic Volume and Emissions.xlsx"
path = dir + file
df = pd.read_excel(path, sheet_name=neighbourhoods[2])
df = df.drop(["Date", "DateTime"], axis=1)
df = df.dropna()

#%% [markdown]
# ### Feature scaling
keys = extra + features + dependents
set = set_scaled = df.loc[:, keys]
scaler = preprocessing.MinMaxScaler().fit(set[features + dependents])
set_scaled.loc[:, features + dependents] = scaler.transform(set[features + dependents])

#%% [markdown]
# ### Plotting the traffic volume passing through the intersection vs. different emissions concentration
pairs = []
for feature in features:
    pairs.append([feature] + dependents)
fig = plt.figure(figsize=(25, 5 * len(pairs)))
gs = gridspec.GridSpec(len(pairs), 1, figure=fig, hspace=0.6)
gs.tight_layout(fig)
# fig.suptitle('Ambient Emissions vs. Traffic Volume', fontsize = 16)
for index, g in enumerate(gs):
    ax1 = fig.add_subplot(g)
    ax1.set_title("{0} vs. Emissions".format(pairs[index][0], pairs[index][1]))
    ax1.set_xticks(set_scaled["TimeWindow"][::12].index)
    ax1.set_xticklabels(set_scaled["TimeWindow"][::12].str.slice(0, 5))
    ax2 = ax1.twiny()
    ax2.set_xticks(set_scaled["DayOfWeek"][::50].index)
    ax2.set_xticklabels(set_scaled["DayOfWeek"][::50])
    ax1.xaxis.grid(b=True, which="major", color="k", linestyle=":", alpha=0.25)
    ax1.yaxis.grid(b=True, which="major", color="k", linestyle=":", alpha=0.25)
    ax2.xaxis.grid(b=False)
    set_scaled[list(pairs[index])[0]].plot(ax=ax1, kind="bar")
    set_scaled[list(pairs[index])[1:]].plot(ax=ax1, rot=45)
    ax1.legend(loc="best")

plt.savefig("{}.png".format(neighbourhoods[2]), bbox_inches="tight", dpi=200)
plt.show()

# generate_results_table.py
# Oliver Evans
# 5-12-2016

# Load data from ../restored/hdfs, and find the best tuples for each tuple size based on the specified metric. Create the following 4 latex tables:
#    The best tuples
#    Sensitivity values for those tuples
#    Specificity values for those tuples
#    Values of specified metric for those tuples

# Load my script to read data from hdfs
from read import *

# data('sens_all') lists sensitivity for all tuples
# data('spec_all',5,6,2) shows specificity for the tuple (2,5,6)
# data('perf_tups') lists the best tuples for each size based on 'performance'
# 'Performance' is the total percentage of correctly classified samples
# 'Product' is the product of sensitivity and specificity
# Everything returned from data() is a Pandas DataFrame

# Other imports
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

########################
## DEFINE METRIC HERE ##
########################
metric_name = 'perf'
def metric_func(sens,spec):
    metrics={}
    metrics['alpha'] = sens/(1-spec)
    metrics['prod'] = sens*spec          
    metrics['sum'] = sens+spec
    metrics['perf'] = 2/3*sens+1/3*spec
    return metrics[metric_name]

# Create directory if it doesn't exists
dir_name='../tables/'+metric_name+'/'
os.system('mkdir -p '+dir_name)

#Set font
font={'family':'serif','size':10}
mpl.rc('font',**font)

# Create contour plot of metric
t=np.arange(0,1,0.01)
x,y=np.meshgrid(t,t)
z=metric_func(x,y)
plt.figure(figsize=[3.5,3.5])
contour_plot = plt.contour(x,y,z,levels=np.linspace(0,z.max(),11))
plt.title("Metric contour: '{}'".format(metric_name))
plt.xlabel("sensitivity")
plt.ylabel("specificity")
plt.colorbar(contour_plot)
plt.tight_layout()
plt.savefig(dir_name+'contour.pdf')

# Find the indices of tuples of each size (2-7)
bool_list = [[len(x) == n for x in data('sens_all').index.values] for n in range(2,8)]
ind = [np.where(x) for x in bool_list]

# Create DataFrames for the 4 tables to be produced
tups_table = pd.DataFrame(index=range(2,8),columns=data('sens_all').columns)
sens_table = pd.DataFrame(index=range(2,8),columns=data('sens_all').columns)
spec_table = pd.DataFrame(index=range(2,8),columns=data('sens_all').columns)
metric_table = pd.DataFrame(index=range(2,8),columns=data('sens_all').columns)

# Determine how to split tuple table to prevent it from being too wide
alg_set_len=3
n_algorithms=len(tups_table.columns)
n_alg_sets=int(np.ceil(n_algorithms/alg_set_len))

# Identify best tuples based on metric for each algorithm
for i in range(6):
    sens = data('sens_all').iloc[ind[i]]
    spec = data('spec_all').iloc[ind[i]]
    perf = data('perf_all').iloc[ind[i]]

    # Calculate metric values based on metric_func
    metric = metric_func(sens,spec)
    
    # Find best tuples
    # This particular metric should be maximized.
    # To minimize, use idxmin instead
    best_tuples = metric.idxmax()

    # Get sens & spec of best tuples
    best_sens = sens.loc[best_tuples]
    best_spec = spec.loc[best_tuples]
    
    # Get best values of metric
    best_metric = metric.loc[best_tuples]

    # Save all information from this tuple size to tables
    tups_table.iloc[i,:] = best_tuples.values
    sens_table.iloc[i,:] = np.diag(best_sens.values)
    spec_table.iloc[i,:] = np.diag(best_spec.values)
    metric_table.iloc[i,:] = np.diag(best_metric.values)

# Export tables to LaTeX
with open(dir_name+'tuples.tex','w') as out_file:
    for alg_set_num in range(n_alg_sets):
        alg_set=tups_table.iloc[:,alg_set_num*alg_set_len:(alg_set_num+1)*alg_set_len]
        alg_set.to_latex(out_file,na_rep='',float_format='{:.2f}'.format)
        out_file.write("\\vspace{1em}\n\n")

with open(dir_name+'sens.tex','w') as out_file:
    sens_table.to_latex(out_file,na_rep='',float_format='{:.2f}'.format)

with open(dir_name+'spec.tex','w') as out_file:
    spec_table.to_latex(out_file,na_rep='',float_format='{:.2f}'.format)

with open(dir_name+'metric.tex','w') as out_file:
    metric_table.to_latex(out_file,na_rep='',float_format='{:.2f}'.format)


# Export tables to plain text
with open(dir_name+'tuples.txt','w') as out_file:
    #Print every few (as defined by alg_set_len) algorithms on a new line
    #This is to prevent strange formatting from lines that are too long
    out_file.write("Best Tuples\n")
    for alg_set_num in range(n_alg_sets):
        alg_set=tups_table.iloc[:,alg_set_num*alg_set_len:(alg_set_num+1)*alg_set_len]
        out_file.write(alg_set.to_string())
        out_file.write("\n\n")

with open(dir_name+'sens.txt','w') as out_file:
    out_file.write("Sensitivity values for Best Tuples\n")
    out_file.write(sens_table.to_string())

with open(dir_name+'spec.txt','w') as out_file:
    out_file.write("Specificity values for Best Tuples\n")
    out_file.write(spec_table.to_string())

with open(dir_name+'metric.txt','w') as out_file:
    out_file.write("'{}' values for Best Tuples\n".format(metric_name))
    out_file.write(metric_table.to_string())

# Done!
print("Generated LaTeX tables based on metric '{}'".format(metric_name))


#plot_symptom_results.py

#Make two plots:
#One for the best specificity for each symptom
#One for the best sensitivity for each symptom
#Out of all tuples of all sizes
#Best will be determined by maximum sens*spec
#Then create a list of which tuple was used for each symptom
#Then use latex to create a pdf containing the 2 plots and list

#Imports
from numpy import *
import pandas as pd
from matplotlib.pyplot import *
from subprocess import check_output
from os import system
import re

#Run bash command, return list of lines of output
#Cmd should be a string or list of strings
#Each argument in cmd must be a separate string
#Use os.system for more complex commands (e.g. piping, redirection, etc.)
#When you don't need to see the output
def run(cmd):
    return check_output(cmd).decode().split('\n')[:-1]

#Return index tuple for maximum value in numpy array
def find_max(a):
    return unravel_index(a.argmax(),a.shape)

#Base directory
base_dir="/home/oevans/chiari/"

#Generate key for converting between my symptom names and real symptom names
#Open file
key_file=open(base_dir+"notes/symptom_key.txt")
#Make array of lines
key_lines=key_file.readlines()
#Split each line into two pieces - my name and real name - by first space
key=[line.replace('\n','').split(' ',1) for line in key_lines[3:]]
#Remove preceeding whitespace from real symptom name
for i,entry in enumerate(key):
    if len(entry) == 2:
        entry[1]=entry[1].lstrip()
    else:
        key.pop(i)
#Convert to numpy array
key=array(key)

#List of best tuple/algorithm/value data from each file
best_data=[]

#List of symptom names in order
symptom_name_data=[]

#Best tuples
tuple_data=[]

#Best algorithms
alg_data=[]

#Best values
value_data=[]

#All metric values
metric_data=[]

#Loop through most recent files
files=run(base_dir+"python/latest_symptoms.sh")
"""
files=['symptoms/symptom3-04-12-2016',
       'symptoms/symptom5-04-12-2016',
       'symptoms/symptom6-04-12-2016',
       'symptoms/symptom7-04-12-2016',
       'symptoms/symptom8-04-12-2016']
"""

# Number of files
n_files=len(files)
for file in files:
    #Dictionary of hdf files
    hdfs={}

    #Get symptom name
    my_name=re.sub('symptoms/','',file)
    my_name=re.sub('-.*','',my_name)
    print(my_name)
    #Remove initial whitespaces
    symptom_name=key[key[:,0]==my_name,1][0].lstrip()
    print(symptom_name)

    #Restore files
    system(base_dir+"python/restore_backup.sh {}".format(file))

    #Open all hdf files
    for file_name in run(["ls",base_dir+'restored/hdf']):
        data_name=file_name[:-4] #Remove file extension
        file_path=base_dir+'restored/hdf/'+file_name
        hdfs[data_name] = pd.read_hdf(file_path,data_name)

    #Multiply sens * spec to judge best
    prod=hdfs['sens_all']*hdfs['spec_all']
    sens=hdfs['sens_all']
    spec=hdfs['spec_all']
    perf=hdfs['perf_all']

    #Metrics to judge quality of prediction
    metrics=[prod,sens,spec,perf]
    metric_names=['prod','sens','spec','perf']

    #Best result of all algorithms for each tuple
    best_list=prod.max(axis=1)

    #List of algorithms which gave those results
    alg_list=prod.idxmax(axis=1)

    #Tuple with the best value overall
    best_tuple=best_list.argmax()

    #Best value *BASED ON MULT*
    best_value=best_list.max()

    #Algorithm which gave that result
    #Won't work if all values in dataframe are NaN (predict failed)
    try:
        best_alg=alg_list[best_tuple]
        #Get values of other metrics

        best_metrics=[metric.loc[[best_tuple],best_alg][0] for metric in metrics]

    except(TypeError):
        print("All NaNs")
        best_tuple=''
        best_alg=''
        #Empty list of lists
        best_metrics=[nan for metric in metrics]
    
    #Save data
    symptom_name_data.append(symptom_name)
    tuple_data.append(best_tuple)
    alg_data.append(best_alg)
    value_data.append(best_value)
    metric_data.append(best_metrics)
    print()

#Convert metric_data to numpy array
metric_data=array(metric_data).T

#Create Pandas DataFrame of final data
#* Expands list to sequence of arguments
data_list = [symptom_name_data,tuple_data,alg_data,*metric_data]

data_array = array(data_list,dtype='object').T
data_df = pd.DataFrame(data_array,columns=['Symptom','Best Tuple','Algorithm','prod','sens','spec','perf'])

#Convert DF to latex
with open('symptom_table.tex','w') as table_file:
    latex_table = data_df.to_latex(table_file,index=False,na_rep='',float_format='{:.2f}'.format)

#Set font
font={'family':'serif'}
rc('font',**font)

#Convert values to numpy array
value_data=array(value_data)

#Plot
fig=figure(figsize=[12,5])
ax=fig.add_subplot(1,1,1)
ax.tick_params('both', length=0, width=0, which='major')
ind=arange(shape(metric_data)[1])
width=0.15
colors=['b','r','y','g']
#color=(0.2588,0.4433,1.0) #Light blue
bar_list=[]
print(metric_data)
print(shape(metric_data))
#Create bar for each metric
for i,metric in enumerate(metrics):
    print("i={}: {}".format(i,metric_names[i]))
    b=bar(ind+i*width,metric_data[i,:],width,color=colors[i])
    bar_list.append(b)
xticks(ind+2*width,symptom_name_data,rotation=45,ha='right')
yticks(linspace(0,1,11))
xlim([0,ind[-1]+len(metrics)*width])
ylim([0,1])
ax.yaxis.grid('on')
title('Chiari Machine Learning Success Rates for Symptoms')
legend(bar_list,metric_names,loc='upper right',bbox_to_anchor=(1,-0.4))
tight_layout()
savefig('symptom_success_plot.eps')
savefig('symptom_success_plot.png')

#Compile latex file
system("epstopdf symptom_success_plot.eps && pdflatex symptom_results.tex")

#learn.py
#Oliver Evans
#Spring 2016

#Machine Learning for Chiari Diagnosis

#For each number between 1 and 15:
    #For all combinations of that many features:
        #Divide samples into groups
        #For each group:
            #For each algorithm:
                #Train algorithm on all other groups
                #Test algorithm on this groups
                #Calculate accuracy
            #Average accuracies to get accuracy for this algorithm
        #Find best algorithm for these features

from numpy import *
import pandas as pd
from sklearn import svm,neighbors,tree,discriminant_analysis,naive_bayes,linear_model
from scipy import io
from scipy.special import binom
from itertools import combinations
from ast import literal_eval as make_tuple
from time import time,strftime
from os import system,chdir
from sys import argv#,exit
import warnings
#from IPython import embed
from os.path import isfile,split
import tarfile
import double_log

####################
## Set up logging ##
####################

#Change directory
chdir('/home/oevans/chiari')

#Get name of current script
script_name=split(argv[0])[1].split('.')[0]

#Get name of data file
data_name=argv[1]

#Determine filename to use for backup
name_date=strftime("{}-%m-%d-%Y".format(data_name))
output_name=name_date
output_num=0
#Increment number until unused filename is found
while isfile("backup/{}.tar.gz".format(output_name)):
    output_num+=1
    output_name="{}_{}".format(name_date,output_num)

print("Using output name: '{}'".format(output_name))

#Log all print statements to file in addition to stdout
Logger=double_log.Logger("logs/{}.log".format(output_name),'w')
print("Current script name:",script_name)
print("Data name:",data_name)

#ignore warning from pytables
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

######################
## Define Functions ##
######################

#Add algorithm to be run with arguments
def add_algorithm(name,algorithm,*these_args,**these_kwargs):
    global names,functions,args,kwargs
    names.append(name)
    functions.append(algorithm)
    args.append(these_args) #args is a tuple
    kwargs.append(these_kwargs) #kwargs is a dictionary

#Fit algorithm
def fit_algorithm(alg_num):
    global train_data,feature_numbers
    global names,functions,args,kwargs
    global group_algorithms
    global tuple_size
    global hdf_time_fit

    #Output name
    #print(names[alg_num])
    
    #Start timer
    tic(1)

    #Create instance
    learner=functions[alg_num](*args[alg_num],**kwargs[alg_num])
    #Fit to data
    learner.fit(train_data[:,feature_numbers],train_data[:,-1])
    #Save instance
    group_algorithms.append(learner)

    #Record time
    hdf_time_fit.iloc[size_index,alg_num]+=toc(1)

#Predict algorithm, accessing global variables
def predict_algorithm(alg_num,group_num):
    global group_algorithms 
    global tuple_sens,tuple_spec,tuple_perf
    global test_data,feature_numbers
    global n_pos,n_neg
    global tuple_size
    global hdf_time_predict 

    #Start timer
    tic(1)

    #Bool array which is True for posives and False for negatives (diagnosis)
    group_bool=test_data[:,-1].astype(bool)

    #Predict
    prediction=group_algorithms[alg_num].predict(test_data[:,feature_numbers])
    #Convert to bool so it's easy to invert to compute spec
    prediction=prediction.astype(bool)

    #Calculate sens and spec
    tuple_sens[alg_num,group_num]=sum(prediction[group_bool])/n_pos
    #print("Sensitivity:",sum(prediction[group_bool])/n_pos)
    tuple_spec[alg_num,group_num]=sum(~prediction[~group_bool])/n_neg
    #print("Specificity:",sum(~prediction[~group_bool])/n_neg)

    #Calculate percent correct
    tuple_perf[alg_num,group_num]=sum(prediction==group_bool)/len(prediction)

    #Record time
    hdf_time_predict.iloc[size_index,alg_num]+=toc(1)

#Add 2 to all values of tuple
def increment_tuple(a):
    return tuple([v+2 for v in a])

#Time algorithms, allowing for multiple simultaneous timers
t0=zeros(2)
def tic(i):
    global t0
    t0[i]=time()
def toc(i):
    global t0
    t1=time()
    return t1-t0[i]

######################
## Start main timer ##
######################

tic(0)

###############
## Read Data ##
###############

#Load data
alldata=loadtxt('data/{}.txt'.format(data_name))
#alldata=datafile[data_name]

#Data has 18 columns.
#First is current data[:,-1], should be ignored
#Last is positive or negative, not a feature
#Penultimate is missing data, should be ignored
#Other 15 are good to use
data=alldata[:,1:]
#savetxt('../data.txt',alldata,fmt='%.2g')

########################
## Features & Samples ##
########################

n_samples=len(data)
n_features=15
print("n_samples = {}".format(n_samples))
print("n_features = {}".format(n_features))

############
## Groups ##
############

#Split samples into groups for training and testing
n_groups=5

#Isolate positive and negatives
#There are 214 total
#First 50 are negative
#Last 164 are positive
total_n_pos=int(sum(data[:,-1]))
total_n_neg=int(n_samples-total_n_pos)
print(total_n_pos,"positives")
print(total_n_neg,"negatives")
neg_data=data[:total_n_neg]
pos_data=data[total_n_neg:]

#Split positives and negatives into 5 groups of 43 (last will be 42)
pos_groups=[]
neg_groups=[]
mixed_groups=[]

#Determine group size
#Because of ceil, last group will always be <= other groups
group_size=int(ceil(n_samples/n_groups))
pos_group_size=int(ceil(total_n_pos/n_groups))
neg_group_size=int(ceil(total_n_neg/n_groups))

for i in range(n_groups):
    pos_groups.append(pos_data[i*pos_group_size:(i+1)*pos_group_size])
    neg_groups.append(neg_data[i*neg_group_size:(i+1)*neg_group_size])

    #Then merge pos and neg groups
    mixed_groups.append(vstack((pos_groups[i],neg_groups[i])))

    #Print results
    """
    print()
    print("Group:",i)
    print("Length:",len(mixed_groups[i]))
    print("Positives:",sum(mixed_groups[i][:,-1]))
    print("Negatives:",len(mixed_groups[i])-sum(mixed_groups[i][:,-1]))
    """

################
## Algorithms ##
################

#Create algorithm lists
names=[]
functions=[]
args=[]
kwargs=[]

#Add algorithms
add_algorithm('SVM',svm.SVC,kernel='linear')
add_algorithm('4NN',neighbors.KNeighborsClassifier,4)
add_algorithm('DT',tree.DecisionTreeClassifier)
add_algorithm('LDA',discriminant_analysis.LinearDiscriminantAnalysis)
add_algorithm('QDA',discriminant_analysis.QuadraticDiscriminantAnalysis)
add_algorithm('NB',naive_bayes.GaussianNB)
add_algorithm('LR',linear_model.LogisticRegression)

#Count algorithms
n_algorithms=len(names)
print(n_algorithms,"algorithms:",names)

#################
## Tuple Sizes ##
#################

#Tuple sizes (inclusive)
size_range=[2,7]

size_list=range(size_range[0],size_range[1]+1)
n_sizes=len(size_list)
print(n_sizes,"sizes:",list(size_list))

#Total number of tuples, counting all sizes
n_tuples_total=int(sum(binom(n_features,size_list)))
print("Total # of tuples:",n_tuples_total)

#List of all possible tuples for all sizes
#These will be used for indices for pandas dataframes
all_tuples=[]
for i in size_list:
    all_tuples+=list(combinations(range(2,n_features+2),i))

########################
## HDF Data Structure ##
########################

#Mean sens & spec values for every algorithm for every tuple, searchable by tuple
hdf_sens_all=pd.DataFrame(zeros([n_tuples_total,n_algorithms]),index=all_tuples,columns=names)
hdf_spec_all=pd.DataFrame(zeros([n_tuples_total,n_algorithms]),index=all_tuples,columns=names)
hdf_perf_all=pd.DataFrame(zeros([n_tuples_total,n_algorithms]),index=all_tuples,columns=names)
#Best mean sens & spec values, like Malena's results
hdf_sens_vals=pd.DataFrame(zeros([n_sizes,n_algorithms]),index=size_list,columns=names)
hdf_spec_vals=pd.DataFrame(zeros([n_sizes,n_algorithms]),index=size_list,columns=names)
hdf_perf_vals=pd.DataFrame(zeros([n_sizes,n_algorithms]),index=size_list,columns=names)
#Tuples which produced best perf values
hdf_perf_tups=pd.DataFrame(zeros([n_sizes,n_algorithms]),index=size_list,columns=names)
#Average time per fit
hdf_time_fit=pd.DataFrame(zeros([n_sizes,n_algorithms]),index=size_list,columns=names)
#Average time per predict
hdf_time_predict=pd.DataFrame(zeros([n_sizes,n_algorithms]),index=size_list,columns=names)

##############
## Run Loop ##
##############

#Loop through tuple size: singles, pairs, triplets, etc.
for size_index,tuple_size in enumerate(size_list):
    #Tuple size
    print()
    print("Tuple size:",tuple_size)

    #Number of possible tuples of this size
    n_tuples=int(binom(n_features,tuple_size))
    print("n_tuples =",n_tuples)

    #Sensitivity & Specificity for this tuple size
    size_sens=zeros([n_tuples,n_algorithms])
    size_spec=zeros([n_tuples,n_algorithms])
    size_perf=zeros([n_tuples,n_algorithms])

    #All possible tuples for this size
    #Convert to list because combinations iterator behaves strangely
    size_tuples=list(combinations(range(n_features),tuple_size))

    #Loop through combinations of feature numbers (tuples)
    for tuple_num,feature_numbers in enumerate(size_tuples):
        #Indices to list
        feature_numbers=tuple(feature_numbers)
        #Indices to print (count starting at 2, not 0)
        natural_features=increment_tuple(feature_numbers)
        #print()
        #print("Tuple #{}: {}".format(tuple_num+1,natural_features))

        #Sensitivity and spec for this tuple
        tuple_sens=zeros([n_algorithms,n_groups])
        tuple_spec=zeros([n_algorithms,n_groups])
        tuple_perf=zeros([n_algorithms,n_groups])

        #Loop through groups
        for group_num,test_data in enumerate(mixed_groups):
            #print()
            #print("Group:",group_num)

            group_algorithms=[]

            #Count number of positives and negatives in this group
            n_pos=sum(test_data[:,-1])
            n_neg=len(test_data)-n_pos
            #print("n_pos =",n_pos)
            #print("n_neg =",n_neg)
            
            #Training group
            #Recombine data excluding test rows
            train_data=vstack(mixed_groups[:group_num]+mixed_groups[group_num+1:])

            #Loop through algorithms
            for alg_num in range(n_algorithms):
                fit_algorithm(alg_num)
                predict_algorithm(alg_num,group_num)

        #Report sens & spec for groups
        """
        print("tuple sens:")
        print(tuple_sens)
        print("tuple spec:")
        print(tuple_spec)
        print()
        """

        #Calculate average sens and spec for each algorithm and save to this size lists
        mean_tuple_sens=[mean(alg_sens) for alg_sens in tuple_sens]
        mean_tuple_spec=[mean(alg_spec) for alg_spec in tuple_spec]
        mean_tuple_perf=[mean(alg_perf) for alg_perf in tuple_perf]

        #Report mean sens & spec for groups
        """
        print("mean tuple sens:")
        print(mean_tuple_sens)
        print("tuple spec:")
        print(mean_tuple_spec)
        print()
        """

        #Save to size_sens
        size_sens[tuple_num]=mean_tuple_sens
        size_spec[tuple_num]=mean_tuple_spec
        size_perf[tuple_num]=mean_tuple_perf

        #Save to hdf DataFrames
        #loc searches for rows by key (I'm using tuples as keys)
        hdf_sens_all.loc[natural_features,:]=mean_tuple_sens
        hdf_spec_all.loc[natural_features,:]=mean_tuple_spec
        hdf_perf_all.loc[natural_features,:]=mean_tuple_perf

    #Scale times to get average per algorithm run
    hdf_time_fit.iloc[size_index,:]/=(n_groups*n_algorithms)
    hdf_time_predict.iloc[size_index,:]/=(n_groups*n_algorithms)


    #For each algorithm, find the best combination for sens. and best for spec. and save the feature numbers and value for each
    for alg_num in range(n_algorithms):
        #Find best tuple for this size and algorithm (return tuple index)
        best_sens_index=argmax(size_sens[:,alg_num])
        best_spec_index=argmax(size_spec[:,alg_num])
        best_perf_index=argmax(size_perf[:,alg_num])

        #Find feature numbers (list of features) for best tuple
        #We are saving feature numbers counting from 2, not 0
        #To align feature numbers with matlab. Hence increment_tuple
        best_sens_nums=increment_tuple(size_tuples[best_sens_index])
        best_spec_nums=increment_tuple(size_tuples[best_spec_index])
        best_perf_nums=increment_tuple(size_tuples[best_perf_index])

        #Save to DataFrame
        hdf_perf_tups.iloc[size_index,alg_num]=str(best_perf_nums)

        #Save to DataFrame
        #hdf_sens_vals.iloc[size_index,alg_num]=size_sens[best_sens_index,alg_num]
        #hdf_spec_vals.iloc[size_index,alg_num]=size_spec[best_spec_index,alg_num]
        hdf_perf_vals.iloc[size_index,alg_num]=size_perf[best_perf_index,alg_num]
        
#Find sens and spec values for tups with best pct per alg per size
for i in range(n_sizes):
    for j in range(n_algorithms):
        #Find tuple of feature numbers - convert str to tuple with make_tuple
        tup=make_tuple(hdf_perf_tups.iloc[i,j])
        #Save values from that tuple
        hdf_sens_vals.iloc[i,j]=hdf_sens_all.loc[[tup]].iloc[0,j]
        hdf_spec_vals.iloc[i,j]=hdf_spec_all.loc[[tup]].iloc[0,j]

print()

print("Overall Sensitivity")
print(hdf_sens_vals)
print()

print("Overall Specificity")
print(hdf_spec_vals)
print()

print("Performance")
print(hdf_perf_vals)
print()

print("Best Tuples")
print(hdf_perf_tups)
print()

#############################
## Write plain text output ##
#############################

with open('results/{}.txt'.format(output_name),'w') as f:
    f.write("Overall Sensitivity\n")
    f.write(hdf_sens_vals.to_string())
    f.write("\n\n")

    f.write("Overall Specificity\n")
    f.write(hdf_spec_vals.to_string())
    f.write("\n\n")

    f.write("Performance\n")
    f.write(hdf_perf_vals.to_string())
    f.write("\n\n")

    #Print every few (as defined by alg_set_len) algorithms on a new line
    #This is to prevent strange formatting from lines that are too long
    f.write("Best Tuples\n")
    alg_set_len=3
    n_alg_sets=int(ceil(n_algorithms/alg_set_len))
    print("n_algsets =",n_alg_sets)
    for alg_set_num in range(n_alg_sets):
        alg_set=hdf_perf_tups.iloc[:,alg_set_num*alg_set_len:(alg_set_num+1)*alg_set_len]
        f.write(alg_set.to_string())
        f.write("\n\n")

###############
## WRITE HDF ##
###############

print("Writing to hdf")

#Create directory if it doesn't already exist
system('mkdir -p hdf')

#Write hdf files
hdf_sens_all.to_hdf('hdf/sens_all.hdf','sens_all',mode='w',complib='blosc')
hdf_spec_all.to_hdf('hdf/spec_all.hdf','spec_all',mode='w',complib='blosc')
hdf_perf_all.to_hdf('hdf/perf_all.hdf','perf_all',mode='w',complib='blosc')

hdf_sens_vals.to_hdf('hdf/sens_vals.hdf','sens_vals',mode='w',complib='blosc')
hdf_spec_vals.to_hdf('hdf/spec_vals.hdf','spec_vals',mode='w',complib='blosc')
hdf_perf_vals.to_hdf('hdf/perf_vals.hdf','perf_vals',mode='w',complib='blosc')

hdf_perf_tups.to_hdf('hdf/perf_tups.hdf','perf_tups',mode='w',complib='blosc')

hdf_time_fit.to_hdf('hdf/time_fit.hdf','time_fit',mode='w',complib='blosc')
hdf_time_predict.to_hdf('hdf/time_predict.hdf','time_predict',mode='w',complib='blosc')

print("Done!")

####################
## End main timer ##
####################

print("Main timer: {:.2f}".format(toc(0)))

####################
## Save all files ##
####################

#Make sure everything is written to log
Logger.flush()

#Create tar archive
with tarfile.open('backup/{}.tar.gz'.format(output_name),'w:gz') as archive:

    #Add files
    archive.add('python/{}.py'.format(script_name))
    archive.add('python/read.py')
    archive.add('data/{}.txt'.format(data_name))
    archive.add('hdf')
    archive.add('logs/{}.log'.format(output_name))
    archive.add('results/{}.txt'.format(output_name))

#Done!
del Logger
print("Saved log - done!")

#read.py
#Read data produced by learn.py (hdf files)

import pandas as pd
from os import listdir

#Dictionary of files
hdfs={}

#Open all hdf files
for file_name in listdir('../restored/hdf'):
    data_name=file_name[:-4] #Remove file extension
    file_path='../restored/hdf/'+file_name
    hdfs[data_name] = pd.read_hdf(file_path,data_name)

#Function to lookup values
def data(data_name=0,*tup):
    #If no data_name is given, display the keys
    if(data_name==0):
        return list(hdfs.keys())

    #Show the whole array if no tuple index is given
    #In which case tup is empty
    elif(len(tup)==0):
        return hdfs[data_name]
    
    #Otherwise, return the row indexed by the given tuple
    #All tuples should be unique and sorted and enclosed as the only element of a list
    else:
        return hdfs[data_name].loc[[tuple(unique(tup))]]
    


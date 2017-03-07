#mat_to_txt.py
#Convert all .mat files in a directory to txt
#mat files are loaded into python as dictionaries
#Only the array with the same key as the filename will be loaded

from numpy import *
from scipy.io import loadmat
from os import listdir,chdir,system
from sys import argv

#Parse command line argument: directory to convert
if len(argv) != 2:
    print("Please specify the directory to convert.")
else:
    d=argv[1]
    chdir(d)
    l=listdir()
    for f in l:
        if f[-4:]==".mat":
            print(f)
            name=f[:-4]+".txt"
            a=loadmat(f)[f[:-4]]
            savetxt(name,a,fmt='%.3g')

            #Align data into table
            system('column -t {} > tmp && cat tmp > {} && rm -f tmp'.format(name,name))

#parse_xlsx_data.py

#Using the data from Urbizu_100CM_50Controls.xlsx:
#For each symptom, create a text file with the array of features
#Concatenate a boolean column vector to the right side of the array for the specific feature
#1 for yes, 0 for no
#If the symptom is unknown for a given patient, omit the patient from the data for this symptom file
#Separate different types of headaches as if they were different symptoms

"""
The contents of the spreadsheet (.xlsx) is as follows:

## Basic nformation 
1 - description
2:51 - controls
52:150 - chiari patients
A - patient #
B - method? (irrelevant)
C - diagnosis (control/patient)
D - id? (irrelevant)

## Features (2:150)
E:U - features (measurements), same order as before, no missing data
V:W - other features, missing lots of data

## Other info
X - sex
Y - age
Z - state (geographic)? (probably irrelevant)
AA:AB - ?? (irrelevant)

## Note about symptoms
Let a symptom with a "normal description" be described in the following way:
    0 - Unknown
    1 - Yes
    2 - No

## Symptoms (52:150)
AC:AI - 7 normal descriptions
AJ - description (text,irrelevant)
AK - Asymptotic (no symptoms) - normal description
AL - Age of symptom appearance - positive integer
AM - Long standing symptoms - normal description
AN - Headaches - normal description
AO - Headache localization
    0 - Unknown
    1 - 4 represent distinct locations
    5 - N/A (no headaches)
AP:BH - SIGNS AND SYMPTOMS - 19 normal descriptions
BI:BJ - 2 normal descriptions - not sure why they aren't grouped with SIGNS AND SYMPTOMS

## Theraputic Procedures (52:150)
BK:BO - 5 normal descriptions

## Summary
E2:U150 - All Features
E52:U150 - Chiari Features
AK2:AK150 - Asymptotic
AC52:AI150,AP2:BJ150 - Relevant features with normal descriptions
AN52:AN150 - Headache normal description
AO52:AO150 - headache localization
"""

#Imports
from numpy import *
from openpyxl import *
from os import chdir,system

#Initial settings
chdir('/home/oevans/chiari')


######################
## Define Functions ##
######################

#Extract numpy array from spreadsheet
#cells should be a string similar to 'A2:B43', specifying a block of cells
def extract(sheet,cells):
    a=array([[i.value for i in j] for j in sheet[cells]])
    #Replace missing datas with 0
    a[where(a==array(None))]=0 
    return a

#Combine symptom and feature information into an array and write it to a text file
#Any occurrence of '{}' in file_name string will be replaced with the column number from symptom_array
#symptom_description string array will be iteratively written as an initial comment
def combine(symptom_array,file_name,symptom_description):

    #Loop through columns
    #Transpose so as not to loop through rows (looping iterates through first axis)
    for j,symptom in enumerate(symptom_array.transpose()):

        #Turn symptom into a row vector
        symptom=symptom.reshape([size(symptom),1])

        #Renumber in the following way:
        #No=2 -> 0
        #Yes=1 -> 1
        #Unknown=0 -> 2
        #This is accomplished by x=2-x
        symptom=2-symptom

        #Combine with feature data, transposing symptom back to column vector
        combined_array=hstack((features,symptom))

        #Eliminate rows with unknown data (x==2)
        filtered_array=delete(combined_array,where(symptom==2),axis=0)

        #Determine file path
        file_path='data/symptoms/'+file_name.format(j)

        #Write data with initial comment
        savetxt(file_path,filtered_array,fmt='%.3g',header='Symptom: {}'.format(symptom_description[j]))

        #Make into table
        system('column -t {} > tmp && cat tmp > {} && rm -f tmp'.format(file_path,file_path))



#########################
## Extract Information ##
#########################

print("Extracting information")

#Load xlsx spreadsheet
ss=load_workbook('data/Urbizu_100CMI_50Controls_Converted.xlsx')['Sheet1']

#Extract feature array
features=extract(ss,'E52:U150')

#There are 50 controls; the rest have chiari
n_patients=len(features)

#Extract normal symptoms and combine symptom array horizontally
normal_symptoms=hstack((extract(ss,'AC52:AI150'),extract(ss,'AP52:BJ150')))
symptom_names=hstack((extract(ss,'AC1:AI1'),extract(ss,'AP1:BJ1')))
symptom_names=symptom_names.reshape(size(symptom_names))

#Extract other symptoms
asymptomatic=extract(ss,'AK52:AK150') #Yes means no symptoms
headache_bool=extract(ss,'AN52:AN150') #Yes means some type of headache
headache_localization=extract(ss,'AO52:AO150') #See definition above

#################################
## Split headache_localization ##
#################################

print("Splitting headache_localization")

#Split into a bool array with each column representing a type of headache
#Headache or no headache is already determined by headache_bool 
#5 means no headache so it should be discarded as it provides no new information
#0 is unknown, so it should also be discarded as it's useless
#This leaves 4 types of headaches to consider
#For now, I'll include 0 and 5 for simplicity. They can be discarded later.
n_headaches=6

#Here, we should follow the spreadsheet's notation: 1=Yes,2=No
#combine() will convert it to bool notation

"""
ex: 
headache #: 1  2  3  4
[5]        [2][2][2][2]
[2]        [2][1][2][2]
[1]  -->   [1][2][2][2]
[4]        [2][2][2][1]
[3]        [2][2][1][2]
[2]        [2][1][2][2]
...            ...
"""

#Create array
localization_array=zeros([n_patients,n_headaches])

#Identify unknowns
unknowns=where(headache_localization==0)

for j in range(n_headaches):
    #Find matches for this headache
    matches=where(headache_localization==j)
    #Find other headches
    others=where(headache_localization!=j)
    #1 for yes
    localization_array[matches,j]=1
    #2 for no
    localization_array[others,j]=2

#Set unknowns to 0
localization_array[unknowns,:]=0

################################################
## Combine various features with symptom data ##
################################################

print("Combining features")

combine(asymptomatic,'asymptomatic.txt',['1 means diagnosed but no symptoms'])
combine(normal_symptoms,'symptom{}.txt',symptom_names)
combine(headache_bool,'headache_bool.txt',['1 means patient experiences some headache'])
combine(localization_array,'headache{}.txt',['Headache {}'.format(j) for j in range(n_headaches)])

#############
## Woohoo! ##
#############

print("Done!")

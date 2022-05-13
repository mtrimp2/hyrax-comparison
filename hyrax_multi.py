'''
hyrax_multi.py
GDDS-297/ 316: Set up tests that compare data grids from cloud Hyrax against on-prem Hyrax

Same as hyrax_test.py except it can take any number of files for comparison as input (primarily for test_all.py multi-testing)
Developer: Maggie Trimpin
Updated: 05/13
'''

import xarray as xr
import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from itertools import chain

from multiprocessing import Pool
import contextlib


def compare(cloud_filepath, on_prem_filepath):
    '''
    Function: compare(cloud_filepath, on_prem_filepath)
    Inputs: cloud_filepath, on_prem_filepath

    Opens each filepath as xarray datasets, with decode_times=False (prevents discrepancies with int/datetime datatypes)
    Iterates through each variable in the cloud dataset, extracts dataarrays from cloud and onprem datasets for that variable
    Replaces onprem dataarray 'NaN' values with the corresponding fmissing_value (cloud dataset uses missing value, onprem uses fmissing_value)
    Each updated onprem dataarray is compared to the cloud dataarray for the same variable using xarray.DataArray.equals(other) function
    For each variable, if they do not produce identical dataarrays, the loop breaks (program returns False). 
    Otherwise, the loop continues ("True" appended to result "equals" array)
    Once all variables are iterated through, if all dataarrays are equal, program returns that they are identical
    '''

    cloud = xr.open_dataset(cloud_filepath, decode_times=False)
    on_prem =  xr.open_dataset(on_prem_filepath, decode_times=False)
    
    equal = []

    #iterate through each variable
    for var in list(cloud.data_vars): #compares all individual data arrays
        #The problem here is that cloud has missing values (100000000.0), and onprem has NaN values
        #Thus, extract missing val from on_prem ds, and then set nan values to that value
        on_prem[var] = on_prem[var].fillna(on_prem[var].attrs['fmissing_value'])
        '''
        #extract list values, put them all in one long list
        cloudList = list(chain.from_iterable(cloud[var].values))[0]
        onpremList = list(chain.from_iterable(on_prem[var].values))[0]
        for index in range(len(cloudList)):#for each element in each list
            currentCloud = cloudList[index]
            currentOnprem = onpremList[index]
            if (currentOnprem == currentCloud):#| (currentCloud != on_prem["Q850"].attrs['fmissing_value']):
                equal.append(True)
            else:
                equal.append(False)
        '''
        #print(var)
        if on_prem[var].equals(cloud[var]):
            equal.append(True)
        else:
            return f"Data grids are not the same for input files {cloud_filepath} and {on_prem_filepath}"
            break

    if all(equal): #If all data variable arrays are equal
        return f"Data grids are identical for input files {cloud_filepath} and {on_prem_filepath}"
    
if __name__ == "__main__":
    '''
    Function: main
    
    Multiprocessing for the purpose of testing multiple files against each other at once (useful in the case of test_all.py)
    Calls compare(cloud_filepath, on_prem_filepath) for each combination of datasets in input command
    Proper format: cloud1 onprem1 cloud2 onprem2 ... cloudi onpremi
    Once processing is complete, program outputs each item in resulting String array, containing each filename and whether or not they are identical
    '''
    if(len(sys.argv) < 2):
        print("Please enter at least one set of datasets for comparison")
    input = []
    for i in range(1,len(sys.argv), 2):#step=2
        cloud_filepath = sys.argv[i]
        on_prem_filepath = sys.argv[i+1]
        input.append((cloud_filepath, on_prem_filepath))

    with Pool() as p:
        results = p.starmap(compare, input)
        print()
        for element in results:
            print(element)
            print()

    #compare(cloud_filepath, on_prem_filepath)


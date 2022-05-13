'''
hyrax_test.py
GDDS-297/ 316: Set up tests that compare data grids from cloud Hyrax against on-prem Hyrax

Developer: Maggie Trimpin
Updated: 05/13
'''

import xarray as xr
import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from itertools import chain

def compare(cloud_filepath, on_prem_filepath):
    '''
    Function: compare(cloud_filepath, on_prem_filepath)
    Inputs: cloud_filepath, on_prem_filepath

    Opens each filepath as xarray datasets, with decode_times=False (prevents discrepancies with int/datetime datatypes)
    Iterates through each variable in the cloud dataset, extracts dataarrays from cloud and onprem datasets for that variable
    Replaces onprem dataarray 'NaN' values with the corresponding fmissing_value (cloud dataset uses missing value, onprem uses fmissing_value)
    Each updated onprem dataarray is compared to the cloud dataarray for the same variable using xarray.DataArray.equals(other) function
    For each variable, if they do not produce identical dataarrays, the loop breaks. Otherwise, the loop continues ("True" appended to result "equals" array)
    Once all variables are iterated through, if all dataarrays are equal, program reports that they are identical
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
            print("Identical")
        else:
            equal.append(False)
            print("Data grids are not the same for on-prem and cloud hyrax")
            break

    if all(equal): #If all data variable arrays are equal
        print("Data grids are identical for on-prem and cloud hyrax")
    
if __name__ == "__main__":
    cloud_filepath = sys.argv[1]
    on_prem_filepath = sys.argv[2]
    
    compare(cloud_filepath, on_prem_filepath)


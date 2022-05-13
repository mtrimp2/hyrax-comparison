'''
hyrax_test.py
GDDS-297/ 316: Set up tests that compare data grids from cloud Hyrax against on-prem Hyrax

Developer: Maggie Trimpin
Updated: 05/13

Sample input:
python hyrax_test.py https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200101.nc4 https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200101.nc4
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
    For each variable, if they do not produce identical dataarrays, the loop breaks, and 'equal' boolean is set to false. 
    Otherwise, the loop continues, and the 'equal' boolean remains true
    Once all variables are iterated through, if all dataarrays are equal (equal == True), program reports that they are identical
    '''

    cloud = xr.open_dataset(cloud_filepath, decode_times=False)
    on_prem =  xr.open_dataset(on_prem_filepath, decode_times=False)
    
    equal = True
    #iterate through each variable
    for var in list(cloud.data_vars): #compares all individual data arrays
        #The problem here is that cloud has missing values (100000000.0), and onprem has NaN values
        #Thus, extract missing val from on_prem ds, and then set nan values to that value
        if on_prem[var].attrs['fmissing_value'] is not None:
            #if variable dataarray has fmissing_value attribute for on_prem
            #set cloud and on_prem's NaN values to on_prem's missing value
            on_prem[var] = on_prem[var].fillna(on_prem[var].attrs['fmissing_value'])
            cloud[var] = cloud[var].fillna(on_prem[var].attrs['fmissing_value'])
        elif cloud[var].attrs['fmissing_value'] is not None:
            #if variable dataarray has fmissing_value attribute for cloud
            #set cloud and on_prem's NaN values to cloud's missing value
            on_prem[var] = on_prem[var].fillna(cloud[var].attrs['fmissing_value'])
            cloud[var] = cloud[var].fillna(cloud[var].attrs['fmissing_value'])

        if not on_prem[var].equals(cloud[var]):
            equal=False
            print("-------------------------------------------------------")
            print("Data grids are not the same for on-prem and cloud hyrax")
            print("-------------------------------------------------------")
            break

    if equal: #If all data variable arrays are equal
        print("-------------------------------------------------------")
        print("Data grids are identical for on-prem and cloud hyrax")
        print("-------------------------------------------------------")
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please enter the urls of two datasets to compare")
    else:    
        cloud_filepath = sys.argv[1]
        on_prem_filepath = sys.argv[2]
        compare(cloud_filepath, on_prem_filepath)


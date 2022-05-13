# GDDS-297/316 Testing Progress
Author: Maggie Trimpin\
Updated: 05/10/22

## Skeleton

1. Opening datasets (with xarray)
2. Iterating through variables, comparing dataarrays for each dataset
    * Some variables are equal, others not
    * Main issue is nan values being inequal/ missing value vs nan value discrepancy
3. If all dataarrays are equal, output that cloud and on-prem versions are the same

### Solution testing
* Tried fillna() method with xarray, slow and not quite working\
* Tried masking, also slow\
* Tried to work with different dataframe types 
    * Numpy arrays: just subtract two numpy arrays and see if all values come out either 0 or nan\
    * Pandas dataframes: Same problem, showing variables U850, V850, CLDPRS, TROPPT, Q850 as difffering

* Since nan != nan, trying something along the lines of ”if cloud != cloud and onprem != onprem, return true\
* Now trying fillna with fmissing value (in a try block, since not all datasets have those attrs)
    * Cloud dataset attrbutes are empty? Why

### Current Solution
**iterate through each variable**
```
for var in list(cloud.data_vars): 
```
^ compares all individual data arrays\

The problem is that cloud has missing values (100000000.0), and onprem has NaN values
Thus, extract missing val from on_prem ds, and then set nan values to that value
```
    on_prem[var] = on_prem[var].fillna(on_prem[var].attrs['fmissing_value'])
```

Each value in the list should now match one another, including nan/missing values\
Also execution time is once again reasonable 

```
if on_prem[var].equals(cloud[var]):
    equal.append(True)
else:
    equal.append(False)
```

Then, if all data vars match, then the datasets are identical
```
if all(equal):
    print("Data grids are identical for on-prem and cloud hyrax")
```

### Added functionality ideas
* Multiprocessing? Only really useful in the case of a mass-tester but still worth looking into if only for my own learning

* Functionality to stop the comparison once the first "False" is reached (ie. if the first dataarrays compared are not the same, why compare all of the others?)
A simple break statemet was required
```
if on_prem[var].equals(cloud[var]):
    equal.append(True)
else:
    equal.append(False)
    print("Data grids are not the same for on-prem and cloud hyrax")
    break
```
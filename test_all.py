'''
test_all.py

Purpose: Store all sample dataset urls for comparison, pass them all to hyrax_multi in one command for multiprocessing comparison
Developer: Maggie Trimpin
Updated: 05/13
'''

import os
from hyrax_multi import compare

cloud_test = [
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200101.nc4",
#"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200102.nc4",
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200103.nc4",
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200104.nc4",
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200105.nc4",
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200106.nc4",
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200107.nc4",
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200108.nc4",
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200109.nc4",
"https://opendap.uat.earthdata.nasa.gov/collections/C1215802944-GES_DISC/granules/M2T1NXSLV.5.12.4%3AMERRA2_400.tavg1_2d_slv_Nx.20200110.nc4"
]
onprem_test = [
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200101.nc4",
#"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200102.nc4",
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200103.nc4",
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200104.nc4",
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200105.nc4",
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200106.nc4",
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200107.nc4",
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200108.nc4",
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200109.nc4",
"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200110.nc4"
]

#iterate through each set of files, run hyrax_test.compare() on each
for i in range(len(cloud_test)):
    cloud = cloud_test[i]
    onprem = onprem_test[i]
    compare(cloud, onprem)


'''
input = 'python hyrax_multi.py'
for i in range(len(cloud_test)):
    #create output with all filenames
    input += f" {cloud_test[i]} {onprem_test[i]} "
#print(input)
os.system(input)
'''
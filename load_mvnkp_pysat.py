#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 09:33:46 2024
Load multiple mvn_kp days. Works for all variables except
Rotation_matrix_IAU_MARS_MAVEN_MSO and 
Rotation_matrix_SPACECRAFT_MAVEN_MSO

@author: tesman
"""


import pysat
import pysatNASA
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import xarray as xr


mvn_kp = pysat.Instrument(inst_module=pysatNASA.instruments.maven_insitu_kp)
mvn_kp.strict_time_flag = False



start_date = datetime(2016, 12, 30) #Change dates here
end_date = datetime(2017, 1, 2)

#mvn_kp.download(start = start_date, stop = end_date) #download works for multiple days


num_days = (end_date - start_date).days
    
for i in range(num_days + 1):
    
    
    START_YR = (start_date + timedelta(days = i)).year
    START_DOY = (start_date + timedelta(days = i)).timetuple().tm_yday
    
    
    END_YR = (start_date + timedelta(days = i + 1)).year
    END_DOY = (start_date + timedelta(days = i + 1)).timetuple().tm_yday
    
    
    mvn_kp.load(yr = START_YR, doy = START_DOY, end_yr = END_YR, end_doy = END_DOY)
    
    
    for name in mvn_kp.variables:
        if name not in ['Rotation_matrix_IAU_MARS_MAVEN_MSO', 'Rotation_matrix_SPACECRAFT_MAVEN_MSO']:
            if i == 0:
                exec(f"{name} = mvn_kp.data['{name}']")
            else:
                exec(f"{name}{i} = mvn_kp.data['{name}']")
            
for i in range(num_days):
    for name in mvn_kp.variables:

        if name not in ['Rotation_matrix_IAU_MARS_MAVEN_MSO', 'Rotation_matrix_SPACECRAFT_MAVEN_MSO']:
            exec(f"{name} = xr.concat([{name}, {name}{i+1}], dim = 'time')")
            exec(f"del {name}{i+1}")
            
            
del name, i, END_DOY, END_YR, START_DOY, START_YR, num_days #Just cleaning up variables

            
    
#Example plot
#plt.plot(time, MAG_field_MSO)
            
            
            
            
            
            
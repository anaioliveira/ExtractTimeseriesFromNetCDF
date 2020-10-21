##################################################################
#
#     Developed by: Ana Isabel Oliveira
#     Project: Soil4Ever
#     Date: MARETEC IST, 07/05/2020
#
##################################################################

#!/usr/bin/python

import sys
import os
import gc
import pygrib
import netCDF4
import numpy as np
import datetime as dt

#Variable long name: longitude, Units: degrees_east
#Variable long name: latitude, Units: degrees_north
#Variable long name: time, Units: hours since 1900-01-01 00:00:00.0
#Variable long name: 10 metre U wind component, Units: m s**-1
#Variable long name: 10 metre V wind component, Units: m s**-1
#Variable long name: 2 metre dewpoint temperature, Units: K
#Variable long name: 2 metre temperature, Units: K
#Variable long name: Surface solar radiation downwards, Units: J m**-2 *1/3600
#Variable long name: Total cloud cover, Units: (0 - 1)
#Variable long name: Total precipitation, Units: m
#Variable long name: Surface pressure, Units: Pa
#Variable long name: Total column rain water, Units: kg m**-2
#Variable long name: Total column snow water, Units: kg m**-2
#Variable long name: Snowfall, Units: m of water equivalent
#Variable long name: Snowmelt, Units: m of water equivalent

inspect_file = 0 #1 if user wants to see the list of properties. No values will be extracted. 0 otherwise.
property = ['Surface pressure', 1, 0] #[property long name, factor to multiply (to change units), factor to sum (to change units)] value*fmult+fsum
stations = [[38.171168, -8.55914, 'Grandola_SurfacePpressure_2020'],
            [37.955457, -8.136548, 'Roxo_SurfacePressure_2020']]
source_files = [r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-01.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-02.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-03.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-04.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-05.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-06.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-07.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-08.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-09.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-10.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-11.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-12.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-13.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-14.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-15.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-16.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-17.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-18.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-19.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-20.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-21.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-22.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-23.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-24.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-25.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-26.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-27.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-28.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-29.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-30.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-01-31.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-01.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-02.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-03.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-04.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-05.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-06.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-07.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-08.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-09.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-10.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-11.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-12.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-13.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-14.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-15.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-16.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-17.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-18.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-19.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-20.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-21.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-22.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-23.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-24.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-25.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-26.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-27.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-28.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-02-29.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-01.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-02.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-03.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-04.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-05.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-06.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-07.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-08.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-09.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-10.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-11.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-12.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-13.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-14.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-15.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-16.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-17.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-18.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-19.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-20.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-21.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-22.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-23.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-24.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-25.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-26.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-27.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-28.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-29.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-30.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-03-31.nc',
r'\\mldata\MLDATA02\Meteo\ERA5_Reanalysis\2020-04-01.nc',
]

dates = []
prop_values = [[] for s in range(len(stations))]

######## AUXILIAR FUNCTIONS ###########
def get_list_of_indexes (lat_array, lon_array):
    
    #print (len(np.shape(lat_array)))
    
    #Check coordinates array dimensions
    distances = np.full((1, len(stations)), np.inf)
    stats_xy = np.empty((np.shape(stations)[0], np.shape(stations)[1]-1))
    if len(np.shape(lat_array)) > 1:
        for x in range(np.shape(lon_array)[1]-1):
            for y in range(np.shape(lat_array)[0]-1):
                for s, sta in enumerate(stations):
                    if np.max(lon_array) > 180 and sta[1] < 0:
                        sta_lon = 360+sta[1]
                    else:
                        sta_lon = sta[1]
                    dist = ((lat_array[y][x]-sta[0])**2 + (lon_array[y][x]-sta[1])**2)**0.5
                    if dist < distances[0][s]:
                        stats_xy[s][0] = x
                        stats_xy[s][1] = y
                        distances[0][s] = dist
    else:
        for x, lon in enumerate(lon_array):
            for y, lat in enumerate(lat_array):
                for s, sta in enumerate(stations):
                    if np.max(lon_array) > 180 and sta[1] < 0:
                        sta_lon = 360+sta[1]
                    else:
                        sta_lon = sta[1]
                    dist = ((lat-sta[0])**2 + (lon-sta_lon)**2)**0.5
                    if dist < distances[0][s]:
                        stats_xy[s][0] = x
                        stats_xy[s][1] = y
                        distances[0][s] = dist
    
    return stats_xy

def get_time (ti):

    #jD = g['julianDay']
    #initial_instant = pygrib.julian_to_datetime(jD)
    #
    #sType = g['stepType']
    ##sUnits = g['forecastTime']
    #sUnits = g['endStep']
    #
    #print (initial_instant, sType, sUnits)
    #sys.exit()
    
    if len(ti) > 1:
        print (ti)

    return

def extract_grib_values(file):
    
    grbs = pygrib.open(file)
    grb = grbs.select(name=property)[0]
    lats, lons = grb.latlons()
    prop_data = grb.values
    
    #Dealing with time
    get_time(grb)

    if file == source_files[0] and prop == properties[0]:
        stations_indexes = get_list_of_indexes(lats, lons)

    t.append(t_)
    
    for s, sta in enumerate(stations):
        x = int(stations_indexes[s][0])
        y = int(stations_indexes[s][1])
        prop_values.append(prop_data[y][x])

    
    
    
    grbs.close()

    return

def extract_nc_values(file):

    nc_file = netCDF4.Dataset(file, 'r')
    
    nc_keys = nc_file.variables.keys()
    for key in nc_keys:
        if 'lat' in key:
            lats = nc_file.variables[key][:]
        elif 'lon' in key:
            lons = nc_file.variables[key][:]
        elif 'time' in key:
            time_key = nc_file.variables[key]
            time_instants = list(netCDF4.num2date(time_key[:],units=time_key.units,calendar=time_key.calendar))
            for i, ti in enumerate(time_instants):
                time_instants[i] = ti.strftime('%d-%m-%Y %H:%M:%S')
            dates.extend(time_instants)
        else:
            pass
    
    stations_indexes = get_list_of_indexes(lats, lons)

    for var in nc_file.variables:
        if property[0] == nc_file.variables[var].long_name:
            var_shortName = var
            
    prop_data = nc_file.variables[var_shortName]

    for s, sta in enumerate(stations):
        x = int(stations_indexes[s][0])
        y = int(stations_indexes[s][1])
        p_values = list(prop_data[:,y,x]*property[1]+property[2])
        prop_values[s].extend(p_values)

    nc_file.close()
    nc_file = None
    
    return

def write_timeseries_file():

    date0 = dates[0].split(' ')[0]
    time0 = dates[0].split(' ')[1]
    year0 = date0.split('-')[2]
    month0 = date0.split('-')[1]
    day0 = date0.split('-')[0]
    hour0 = time0.split(':')[0]
    minute0 = time0.split(':')[1]
    second0 = time0.split(':')[2]
    
    date0_python = dt.datetime.strptime(dates[0], '%d-%m-%Y %H:%M:%S')
    
    for s, sta in enumerate(stations):
        sta_name = sta[-1]
        # Create file
        fin = open (sta_name + '.dat', 'w')
        #Write headers
        fin.writelines('Time Serie Results File\n')
        fin.writelines('NAME                    : ' + sta_name + '\n')
        fin.writelines('COORDINATES             : ' + str(sta[0]) + ' ' + str(sta[1]) + '\n')
        fin.writelines('SERIE_INITIAL_DATA      : ' + year0 + '.' + (month0 + '.').rjust(4) \
                                                        + (day0 + '.').rjust(4) + (hour0 + '.').rjust(4) \
                                                        + (minute0 + '.').rjust(4) + (second0 + '.').rjust(4) + '\n')
        fin.writelines('TIME_UNITS              : HOURS' + '\n')
        fin.writelines('Hours'.rjust(13) + 'YY'.rjust(5) +'MM'.rjust(4) + 'DD'.rjust(4) \
                        + 'hh'.rjust(4) + 'mm'.rjust(4) + 'ss'.rjust(9) \
                        + (property[0].replace(' ', '_')).rjust(46) + '\n')
        fin.writelines('<BeginTimeSerie>\n')
        #Write dates and values
        for i, instant in enumerate(dates):
            di = dt.datetime.strptime(instant, '%d-%m-%Y %H:%M:%S')
            hours_from_beginning = (di-date0_python).total_seconds()/3600
            
            datei = instant.split(' ')[0]
            timei = instant.split(' ')[1]
            yeari = datei.split('-')[2]
            monthi = datei.split('-')[1]
            dayi = datei.split('-')[0]
            houri = timei.split(':')[0]
            minutei = timei.split(':')[1]
            secondi = timei.split(':')[2]
            
            line_to_write = str(round(hours_from_beginning,2)).rjust(14) + yeari.rjust(5) + \
                            monthi.rjust(4) + dayi.rjust(4) + houri.rjust(4) + \
                            minutei.rjust(4) + secondi.rjust(9) + str(prop_values[s][i]).rjust(45) + '\n'
                            
            fin.writelines(line_to_write)
        
        #Finish file
        fin.writelines('<EndTimeSerie>\n')
        
        #Write last line of file
        fin.close()

    return

############# MAIN FUNCTION #############
if __name__ == '__main__':
    
    for file in source_files:
        print ('Working on file ' + os.path.basename(file) + '.')
    
        # If file is grib format
        if file.endswith('grb2') or file.endswith('grb'):
            
            # List all the properties in file
            if inspect_file == 1:
                # Open file
                grbs = pygrib.open(file)
                for grb in grbs:
                    print(grb)
                grbs.close() # Close grib file.
                sys.exit()
            
            # If the user don't need to see the properties of the file
            #extract_grib_values(file)
            
        # If file is netcdf format
        elif file.endswith('nc'):
            # List all the properties in file
            if inspect_file == 1:
                # Open file
                nc_file = netCDF4.Dataset(file, 'r')
                for var in nc_file.variables:
                    print('Variable long name: ' + nc_file.variables[var].long_name + ', Units: ' + nc_file.variables[var].units)
                nc_file.close() # Close grib file.
                sys.exit()
            
            # If the user don't need to see the properties of the file
            extract_nc_values(file)
            
        # If file is hdf5 format
        elif file.endswith('hdf5'):
            pass
        else:
            print("The file format is not reconigzed.")
            
        gc.collect()
            
    write_timeseries_file()
    print ('Done!')
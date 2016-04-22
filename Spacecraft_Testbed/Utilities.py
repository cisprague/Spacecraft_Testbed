'''Import necessary modules'''
#For directory navigation
import os, sys
#For ephemeride computation
from jplephem.spk import SPK
#For TLE propogation
from sgp4.earth_gravity import wgs84 as grav_const
from sgp4.io import twoline2rv
#For Julian date conversion
from sgp4.ext import invjday
#For linear algebra
import numpy as np
#Specify the user's path to this directory
Directory = os.path.dirname(__file__)

#Celestial Body utilities
def Assign_Celestial_Body_Attributes(celestial_body):
  '''This function assigns the attributes to a known celestial body.
  These attributes include the various facts of the celestial body,
  and its orbiting satellites if specified to be included.'''
  #The name of the celestial body
  name = celestial_body.name
  #The attributes of the celestial body
  attributes = Celestial_Body_Attributes()[name]
  #Assign the factual attributes to the celestial body
  for attribute in attributes.keys():
    setattr(celestial_body, attribute, attributes[attribute] )
    pass
  return None

def Celestial_Body_Attributes():
  '''Returns all the attributes of a specified
  celestial body. All units are SI.'''
  cba ={
    'Earth': {'aphelion': 152100000000.0,
              'density': 5514.0,
              'diameter': 12756000.0,
              'distance_from_sun': 149600000000.0,
              'escape_velocity': 11200.0,
              'global_magnetic_field': True,
              'gravity': 9.8,
              'jplephem_index': (3, 399),
              'length_of_day': 86400.0,
              'mass': 5.969999999999999e+24,
              'mean_temperature': 15.0,
              'number_of_moons': 1,
              'obliquity_to_orbit': 0.40840722,
              'orbital_eccentricity': 0.017,
              'orbital_inclination': 0.0,
              'orbital_period': 31553280.0,
              'orbital_velocity': 29800.0,
              'perihelion': 147100000000.0,
              'ring_system': False,
              'rotation_period': 86040.0,
              'surface_pressure': 100000.0},
    'Jupiter': {'aphelion': 816600000000.0,
                'density': 1326.0,
                'diameter': 142984000.0,
                'distance_from_sun': 778600000000.0,
                'escape_velocity': 59500.0,
                'global_magnetic_field': True,
                'gravity': 23.1,
                'jplephem_index': (0, 5),
                'length_of_day': 35640.0,
                'mass': 1.898e+27,
                'mean_temperature': -110.0,
                'number_of_moons': 67,
                'obliquity_to_orbit': 0.054105230000000004,
                'orbital_eccentricity': 0.049,
                'orbital_inclination': 0.022689290000000004,
                'orbital_period': 374198400.0,
                'orbital_velocity': 13100.0,
                'perihelion': 740500000000.0,
                'ring_system': True,
                'rotation_period': 35640.0,
                'surface_pressure': None},
    'Mars': {'aphelion': 249200000000.0,
             'density': 3933.0,
             'diameter': 6792000.0,
             'distance_from_sun': 227900000000.0,
             'escape_velocity': 5000.0,
             'global_magnetic_field': False,
             'gravity': 3.7,
             'jplephem_index': (0, 4),
             'length_of_day': 88920.0,
             'mass': 6.42e+23,
             'mean_temperature': -65.0,
             'number_of_moons': 2,
             'obliquity_to_orbit': 0.43982316000000005,
             'orbital_eccentricity': 0.094,
             'orbital_inclination': 0.03316127,
             'orbital_period': 59356800.0,
             'orbital_velocity': 24100.0,
             'perihelion': 206600000000.0,
             'ring_system': False,
             'rotation_period': 88560.0,
             'surface_pressure': 1000.0},
    'Mercury': {'aphelion': 69800000000.0,
                'density': 5427.0,
                'diameter': 4879000.0,
                'distance_from_sun': 57900000000.0,
                'escape_velocity': 4300.0,
                'global_magnetic_field': True,
                'gravity': 3.7,
                'jplephem_index': (1, 199),
                'length_of_day': 15201360.000000002,
                'mass': 3.3e+23,
                'mean_temperature': 167.0,
                'number_of_moons': 0,
                'obliquity_to_orbit': 0.00017453300000000002,
                'orbital_eccentricity': 0.205,
                'orbital_inclination': 0.1221731,
                'orbital_period': 7603200.0,
                'orbital_velocity': 47400.0,
                'perihelion': 46000000000.0,
                'ring_system': False,
                'rotation_period': 5067360.0,
                'surface_pressure': 0.0},
    'Moon': {'aphelion': 406000000.0,
             'density': 3340.0,
             'diameter': 3475000.0,
             'distance_from_sun': 384000000.0,
             'escape_velocity': 2400.0,
             'global_magnetic_field': False,
             'gravity': 1.6,
             'jplephem_index': (3, 301),
             'length_of_day': 2551320.0,
             'mass': 7.3e+22,
             'mean_temperature': -20.0,
             'number_of_moons': 0,
             'obliquity_to_orbit': 0.11693711000000001,
             'orbital_eccentricity': 0.055,
             'orbital_inclination': 0.08901183,
             'orbital_period': 2358720.0,
             'orbital_velocity': 1000.0,
             'perihelion': 363000000.0,
             'ring_system': False,
             'rotation_period': 2360520.0,
             'surface_pressure': 0.0},
    'Neptune': {'aphelion': 4545700000000.0,
                'density': 1638.0,
                'diameter': 49528000.0,
                'distance_from_sun': 4495100000000.0,
                'escape_velocity': 23500.0,
                'global_magnetic_field': True,
                'gravity': 11.0,
                'jplephem_index': (0, 8),
                'length_of_day': 57960.00000000001,
                'mass': 1.0199999999999999e+26,
                'mean_temperature': -200.0,
                'number_of_moons': 14,
                'obliquity_to_orbit': 0.49392839000000005,
                'orbital_eccentricity': 0.011,
                'orbital_inclination': 0.03141594,
                'orbital_period': 5166720000.0,
                'orbital_velocity': 5400.0,
                'perihelion': 4444500000000.0,
                'ring_system': True,
                'rotation_period': 57960.00000000001,
                'surface_pressure': None},
    'Pluto': {'aphelion': 7375900000000.0,
              'density': 2095.0,
              'diameter': 2370000.0,
              'distance_from_sun': 5906400000000.0,
              'escape_velocity': 1300.0,
              'global_magnetic_field': True,
              'gravity': 0.7,
              'jplephem_index': (0, 9),
              'length_of_day': 551880.0,
              'mass': 1.46e+22,
              'mean_temperature': -225.0,
              'number_of_moons': 5,
              'obliquity_to_orbit': 2.13802925,
              'orbital_eccentricity': 0.244,
              'orbital_inclination': 0.30019676,
              'orbital_period': 7824384000.0,
              'orbital_velocity': 4700.0,
              'perihelion': 4436800000000.0,
              'ring_system': False,
              'rotation_period': -551880.0,
              'surface_pressure': 0.0},
    'Saturn': {'aphelion': 1514500000000.0,
               'density': 687.0,
               'diameter': 120536000.0,
               'distance_from_sun': 1433500000000.0,
               'escape_velocity': 35500.0,
               'global_magnetic_field': True,
               'gravity': 9.0,
               'jplephem_index': (0, 6),
               'length_of_day': 38520.0,
               'mass': 5.68e+26,
               'mean_temperature': -140.0,
               'number_of_moons': 62,
               'obliquity_to_orbit': 0.46600311000000005,
               'orbital_eccentricity': 0.057,
               'orbital_inclination': 0.043633250000000005,
               'orbital_period': 928540800.0,
               'orbital_velocity': 9700.0,
               'perihelion': 1352600000000.0,
               'ring_system': True,
               'rotation_period': 38520.0,
               'surface_pressure': None},
    'Uranus': {'aphelion': 3003600000000.0,
               'density': 1271.0,
               'diameter': 51118000.0,
               'distance_from_sun': 2872500000000.0,
               'escape_velocity': 21300.0,
               'global_magnetic_field': True,
               'gravity': 8.7,
               'jplephem_index': (0, 7),
               'length_of_day': 61920.0,
               'mass': 8.68e+25,
               'mean_temperature': -195.0,
               'number_of_moons': 27,
               'obliquity_to_orbit': 1.70693274,
               'orbital_eccentricity': 0.046,
               'orbital_inclination': 0.013962640000000002,
               'orbital_period': 2642889600.0,
               'orbital_velocity': 6800.0,
               'perihelion': 2741300000000.0,
               'ring_system': True,
               'rotation_period': -61920.0,
               'surface_pressure': None},
    'Venus': {'aphelion': 108900000000.0,
              'density': 5243.0,
              'diameter': 12104000.0,
              'distance_from_sun': 108200000000.0,
              'escape_velocity': 10400.0,
              'global_magnetic_field': False,
              'gravity': 8.9,
              'jplephem_index': (2, 299),
              'length_of_day': 10087200.0,
              'mass': 4.87e+24,
              'mean_temperature': 464.0,
              'number_of_moons': 0,
              'obliquity_to_orbit': 3.0962154200000005,
              'orbital_eccentricity': 0.007,
              'orbital_inclination': 0.05934122,
              'orbital_period': 19414080.0,
              'orbital_velocity': 35000.0,
              'perihelion': 107500000000.0,
              'ring_system': False,
              'rotation_period': -20997000.0,
              'surface_pressure': 9200000.0}}
  return cba
pass

def Position_and_Velocity_Celestial_Body(celestial_body, time):
  #The JPL ephemeris index of the celestial body
  jpli = celestial_body.jplephem_index
  #Path to ephemeris file
  path_ephem = Directory + '/Information/Celestial_Bodies/Ephemerides/de430.bsp'
  #The ephemeris kernel
  kernel = SPK.open(path_ephem)
  #The position and velocity
  pv = np.vstack(kernel[jpli].compute_and_differentiate(time))
  #If the ephemeris was wrt to its local barcyentre
  if not jpli[0] == 0:
    #Compute barycentric position rather
    pv = np.add(pv, np.vstack(kernel[0, jpli[0]].compute_and_differentiate(time)))
    pass
  #Convert km to m
  pv[0, :] = np.multiply(pv[0, :], 1e3)
  #Convert km/day to m/s
  pv[1, :]= np.multiply(pv[1, :], 0.0115741)
  #Return a (2,3) numpy array
  return pv
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  #Satellite Utilities
def Satellite_Dictionary(celestial_body_name):
  '''Returns a dictionary of Satellite class instances
  related to the celestial body.'''
  #The name of the celestial body
  name_cb = celestial_body_name
  #Path to celestial body's satellites
  path = Directory + '/Information/Celestial_Bodies/' + name_cb + '/Satellites'
  #Initialise the dictionary
  sat_dict = {}
  
  #Scan the Satellites folder for type collections
  for type_col in os.listdir(path):
    #Initialise a sub dictionary for the type collection
    sat_dict[type_col] = {}
    #Descend into the collection
    path1 = path + '/' + type_col
    
    #Scan the type collection for satellites
    for sat in os.listdir(path1):
      #Initialise a sub dictionary for the spacecraft
      sat_dict[type_col][sat] = {}
      #Descend into satellite
      path2 = path1 + '/' + sat
      
      #Scan the satellite  folder for TLE
      for f_name in os.listdir(path2):
        if f_name.endswith('.tle'):
          path3 = path2 + '/' + f_name
          #Read the TLE
          TLE = Read_TLE(path3)
          
          #Scan the TLE for objects
          for obj in TLE.keys():
            #First line of the object's TLE
            line1 = TLE[obj]['line1']
            #Second line of the object's TLE
            line2 = TLE[obj]['line2']
            #Instantiate a Satellite
            sat_dict[type_col][sat][obj] = (line1, line2)
          pass
        pass
      pass
    pass
  return sat_dict

def Read_TLE(file_path):
  '''Generates a dictionary from a two line element file'''
  #Make sure it is a TLE file
  if not file_path.endswith('.tle'):
    raise ValueError('The supplied file must be a two line element (.tle).')
  #Initialise the dictionary
  collection = {}
  #Open the two line element file of specified file path
  TLE = open(file_path)
  #Initialise the counter to accomodate three line repetition
  counter = 0
  #For each line in the TLE file
  for line in TLE:
    #Clean the line up
    line = line.rstrip('\n')
    line = line.rstrip('\r')
    #If the line is the header line
    if counter == 0:
      #Than this is the orbital body name
      header = line.strip()
      #Use underscore for versatility
      header = header.replace(' ', '_')
      header = header.replace('-', '_')
      header = header.title()
      #If the header is already used in dictionary
      if header in collection.keys():
        #Than subscripts must be added
        #Add count to times header has been used
        header_count += 1
        #Add header count subscript to header name
        header = header + '_' + str(header_count)
        #Instantiate header's dictionary in collection
        collection[header] = {}
      #If the header has not been used yet
      else:
        collection[header] = {}
        #Set the header counter back to zero
        header_count = 0
      counter += 1
    elif counter == 1:
      collection[header]['line1'] = line
      counter += 1
    elif counter == 2:
      collection[header]['line2'] = line
      #Reset the counter
      counter -= 2
  return collection

def Position_and_Velocity_Satellite(satellite, time):
  #The first line of the TLE
  line1 = satellite.line1
  #The second line
  line2 = satellite.line2
  #Fictitious SGP4 satellite object
  sat = twoline2rv(line1, line2, grav_const)
  #Convert Julian date to conventional
  time_conv = invjday(time)
  #The position and velocity of the satellite
  pv = np.asarray(sat.propagate( *time_conv))
  #Convert km to m and km/s to m/s
  pv = np.multiply(pv, 1e3)
  #The attracting body ephemeris
  PV = satellite.attracting_body.Position_and_Velocity(time)
  #Convert from geocentric to barycentric frame
  pv = np.add(pv, PV)
  return pv
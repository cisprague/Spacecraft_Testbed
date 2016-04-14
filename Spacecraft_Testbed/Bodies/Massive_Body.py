'''
Massive_Body.py

This package aims to construct the architecture from which one
may effectivly define a massive celestial body that is described
with particular physical attributes.
<<<<<<< HEAD
=======
Copyright (C) Christopher Iliffe Sprague

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
>>>>>>> 4849294fc9af7ef0087f692b4cddebe53ac92762
'''

#Import numpy linear algebra library
import numpy as np
<<<<<<< HEAD
#Import sys
import sys
#Import os
import os
#Import JPL SPICE Kernel with jplephem 2.5
from jplephem.spk import SPK
#Import utilies
from Body_Utilities import Make_Massive_Body_Information
from Body_Utilities import Assign_Orbital_Bodies
from Body_Utilities import Make_Massive_Body_Information
from Body_Utilities import Install_Ephemeris
#Specify the directory of this file
Directory = os.path.dirname(__file__)
#Import for web retrieval
import urllib




class Massive_Body(object):
  def __init__(self, name):
    #Catalogue of body imformation
    Body_Information = Make_Massive_Body_Information()
=======
import os
#Import JPL SPICE Kernel with jplephem 2.5
from jplephem.spk import SPK

def isfloat(value):
  try:
    float(value)
    #Return True if value is indeed a float
    return True
  except ValueError:
    #Rightfully return False if value is not a float
    return False
def Make_Body_Information():
  #Master dictionary for body information
  Body_Information = {}
  #Indicies for use in jplephem 2.5
  jplephem_Indicies = {'Mercury': (1, 199),  #Mercury barycentre with respect to solar system barycentre
                       'Venus': (2, 299),     #Venus barycentre with respect to solar system barycentre
                       'Earth': (3, 399),     #Earth barycentre with respect to solar system barycentre
                       'Mars': (0, 4),        #Mars barycentre with respect to solar system barycentre
                       'Jupiter': (0, 5),     #Jupiter barycentre with respect to solar system barycentre
                       'Saturn': (0, 6),      #Saturn barycentre with repsect to solar system barycentre
                       'Uranus': (0, 7),      #Uranus barycentre with respect to solar system barycentre
                       'Neptune': (0, 8),     #Neptune barycentre with respect to solar system barycentre
                       'Pluto': (0, 9),       #Pluto barycentre with respect to solar system barycentre
                       'Sun': (0, 10),        #Sun centre with respect to solar system barycentre
                       'Moon': (3, 301)}      #Moon centre with respect to Earth barycentre
  #Define folder path to planetary information file
  path = os.getcwd()
  path = path.split('Spacecraft_Testbed')[0]
  path = path + 'Spacecraft_Testbed/Bodies/Planetary_Information'
  #Open text file of planetary information (thanks NASA)
  Planetary_Information = open(path)
  #Generate a list of the rows
  Planetary_Information= Planetary_Information.readlines()
  #Planetary information list
  Planetary_Information_List = []
  Headers = []
  Siders = []
  #For each row in file
  for row in range(len(Planetary_Information)):
    Row = []
    #Split the items in the row by the delimeter
    for item in Planetary_Information[row].split('\t'):
      #Before the units
      item = item.split(' (')[0]
      #Remove the white space and other delimeters from each string item
      item = item.strip()
      #Make strings title case in order to validly reference the jplephem_Indices table
      item = item.title()
      item = item.replace(',', '')
      item = item.replace('*', '')
      item = item.replace(' ', '_')
      item = item.replace('?', '')
      if isfloat(item):
        item = float(item)
      elif item.lower() == 'yes':
        item = True
      elif item.lower() == 'no':
        item = False
      #Append the item to the row list
      Row.append(item)
    #Append all rows except header row to the list
    if row != 0 and row != 21:
      Planetary_Information_List.append(Row[1:])  #Without sider
      #Append to siders list without units
      Siders.append(Row[0].split(' (')[0])
    elif row == 0:
      Headers = Row[1:]
  Planetary_Information = Planetary_Information_List
  for itemi in range(len(Headers)):
    h = Headers[itemi]
    Body_Information[h] = {}
    Body_Information[h]['jplephem_index'] = jplephem_Indicies[h]
  for rowi in range(len(Siders)):
    for itemi in range(len(Headers)):
      #Title of header
      h = Headers[itemi]
      #Title of sider
      s = Siders[rowi]
      #Multiplier based on sider units
      if h in ['Mass']:
        #Convert 10^24 kg to kg
        m = 1e24
      elif h in ['Diameter','Escape Velocity','Orbital Velocity']:
        #Convert km to m
        m = 1e3
      elif h in ['Rotation Period', 'Length of Day']:
        #Convert hours to seconds
        m = 36e2
      elif h in ['Distance from Sun', 'Perihelion', 'Aphelion']:
        #Convert 10^6 km to m
        m = 1e9
      elif h in ['Orbital Period']:
        #Convert days to seconds
        m = 864e2
      #If already in SI units or no necessary
      else:
        m = 1.0
      item = Planetary_Information[rowi][itemi]
      if isfloat(item):
        Body_Information[h][s] = m * Planetary_Information[rowi][itemi]
      else:
        Body_Information[h][s] = item
  return Body_Information
class Massive_Body(object):
  def __init__(self, name):
    #Catalogue of body imformation
    Body_Information = Make_Body_Information()
>>>>>>> 4849294fc9af7ef0087f692b4cddebe53ac92762
    #List of body names
    body_names = Body_Information.keys()
    if name not in body_names:
      raise ValueError("Name must be in available ephemerides: ", ','.join(body_names))
    #Name name of body
    self.name = name
<<<<<<< HEAD
    #Assign the orbital bodies of the massive body
    Assign_Orbital_Bodies(self)
    #History list Julian dates at which ephemerides were referenced at, 
    #the first item being the date at which the simulation comences. 
    #Subsequent dates will be determined by the time step used by 
    #the integration scheme, which may be adaptive in nature.
=======
    #History list Julian dates at which ephemerides were referenced at, the first item being the date at which the simulation comences. Subsequent dates will be determined by the time step used by the integration scheme, which may be adaptive in nature.
>>>>>>> 4849294fc9af7ef0087f692b4cddebe53ac92762
    self.times = np.empty(shape = (0, 0), dtype = float)
    #History list of 3 dimensional position vectors [m]
    self.positions = np.empty(shape = (0, 3), dtype = float)
    #History list of 3 dimensional velocity vectors [m]
    self.velocities = np.empty(shape = (0, 3), dtype = float)
    for char in Body_Information[name].keys():
      setattr(Massive_Body, char.lower(), Body_Information[name][char])
  def Position_and_Velocity(self, time):
    '''Returns a list of 2 vectors of barycentric position and velocity'''
<<<<<<< HEAD
    path = Directory + '/Information/Ephemerides/'
    kernel = path + 'de430.bsp'
    #Does the user have an ephemeris installed
    Install_Ephemeris(path, kernel)
    #If you do not have the ephemeris
    #Assign kernel to a particular ephemerides catalog
    kernel = SPK.open(kernel)    
=======
    #Assign kernel to a particular ephemerides catalog
    kernel = SPK.open('/home/christopher/Documents/Spacecraft_Testbed/Bodies/Ephemerides/de430.bsp')    
>>>>>>> 4849294fc9af7ef0087f692b4cddebe53ac92762
    #Name of the body for which to compute
    Body_Name = self.name
    #Time at which to compute
    Time = time
    #Body imformation table
<<<<<<< HEAD
    Body_Information = Make_Massive_Body_Information()
=======
    Body_Information = Make_Body_Information()
>>>>>>> 4849294fc9af7ef0087f692b4cddebe53ac92762
    #Index for which to compute
    jplephem_Index = Body_Information[Body_Name]['jplephem_index']
    #First inicie of index
    jplephem_Index_0 = jplephem_Index[0]
    #Barycentric position and velocity vectors
    P, V = kernel[jplephem_Index].compute_and_differentiate(Time)
    #If the ephemeris is in reference from the local barycentre
    if jplephem_Index_0 != 0:
      #Than compute ephemeris of local barycentre with respect to solar systen barycentre
      jplephem_Index = (0, jplephem_Index_0)
      #Assign position and velocity to numpy arrays returned from jplephem 2.5
      p, v = kernel[jplephem_Index].compute_and_differentiate(Time)
      #Add the ephemerides
      P += p  #True barycentric position
      V += v  #True barycentric velocity
    #Convert kilometres to metres
<<<<<<< HEAD
    P = P * 1e3
=======
    P = P * 1000.
>>>>>>> 4849294fc9af7ef0087f692b4cddebe53ac92762
    #Convert kilometres per day to metres per second
    V = V * 0.0115741
    #Returns numpy arrays, each of size (0,3)
    return P, V
  def Position_and_Velocity_WRT(self, Body_Ref, time):
    '''This function takes as its arguments the body whose position and velocity are to be calculated for and the reference body from which measurements are referenced from'''
    #Barycentric position and velocity of reference body
    P0, V0 = Body_Ref.Position_and_Velocity(time)
    #Barycentric position and velocity of body
    P, V = self.Position_and_Velocity(time)
    #Local position and velocity of body with respect to reference body
    p = P - P0
    v = V - V0
    #Returns numpy arrays, each of size (0,3)
    return p, v
  def Update_Position_and_Velocity(self, time):
    '''This function takes as its argument time, which will be obtained from the time step of the simulation, and updates the historical arrays, namely: (1,_) times, (_,3) positions, and (_,3) velocities.'''
    #Barycentric position and velocity of body at time
    p, v = self.Position_and_Velocity(time)
    #Append results to history keeping list for this body
    self.times = np.append(self.times, time)
    self.positions = np.vstack([self.positions, p])
    self.velocities = np.vstack([self.velocities, v])
    #If it is desired to print for the sake of debugging
    return p, v

<<<<<<< HEAD
=======
Citations = '''
DE430 JPL Development Ephemeris
Folkner, W. M., Williams, J. G., Boggs, D. H., Park, R. S., & Kuchynka, P. (2014). The Planetary and Lunar Ephemerides DE430 and DE431.

jplephem 2.5 Python
Rhodes, B. (2015). jplephem 2.5. Python Software Foundation.
'''
>>>>>>> 4849294fc9af7ef0087f692b4cddebe53ac92762

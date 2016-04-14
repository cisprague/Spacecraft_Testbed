'''
Massive_Body.py

This package aims to construct the architecture from which one
may effectivly define a massive celestial body that is described
with particular physical attributes.
'''

#Import numpy linear algebra library
import numpy as np
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
    #List of body names
    body_names = Body_Information.keys()
    if name not in body_names:
      raise ValueError("Name must be in available ephemerides: ", ','.join(body_names))
    #Name name of body
    self.name = name
    #Assign the orbital bodies of the massive body
    Assign_Orbital_Bodies(self)
    #History list Julian dates at which ephemerides were referenced at, 
    #the first item being the date at which the simulation comences. 
    #Subsequent dates will be determined by the time step used by 
    #the integration scheme, which may be adaptive in nature.
    self.times = np.empty(shape = (0, 0), dtype = float)
    #History list of 3 dimensional position vectors [m]
    self.positions = np.empty(shape = (0, 3), dtype = float)
    #History list of 3 dimensional velocity vectors [m]
    self.velocities = np.empty(shape = (0, 3), dtype = float)
    for char in Body_Information[name].keys():
      setattr(Massive_Body, char.lower(), Body_Information[name][char])
    return
  
  def Position_and_Velocity(self, time):
    '''Returns a list of 2 vectors of barycentric position and velocity'''
    path = Directory + '/Information/Ephemerides/'
    kernel = path + 'de430.bsp'
    #Does the user have an ephemeris installed
    Install_Ephemeris(path, kernel)
    #If you do not have the ephemeris
    #Assign kernel to a particular ephemerides catalog
    kernel = SPK.open(kernel)    
    #Name of the body for which to compute
    Body_Name = self.name
    #Time at which to compute
    Time = time
    #Body imformation table
    Body_Information = Make_Massive_Body_Information()
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
    P = P * 1e3
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


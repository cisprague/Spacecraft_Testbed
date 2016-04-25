'''Import necessary modules'''
#For linear algebra
import numpy as np
#For plotting
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from matplotlib.colors import cnames
#Celestial body utilities
from Utilities import * 
  
  
#Initialise classes
class Body(object):
  '''
  In classical mechanics a physical body is collection of
  matter having properties including mass, velocity,
  momentum and energy. The matter exists in a volume
  of three-dimensional space called its extension.
  '''
  
  #Instance record
  _instances = []
  
  def __init__(self, name, mass = None):
    # __base__ attribute will return the Body class
    self.__base__ = Body
    #Name of body
    self.name = name
    #Mass of body
    self.mass = np.float64(mass)
    #Position record
    self.positions = np.empty(shape = (0, 3), dtype = np.float64)
    #Velocity record
    self.velocities = np.empty(shape = (0, 3), dtype = np.float64)
    #Append to _instances
    Body._instances.append(self)
    return None
  
  def Position_and_Velocity(self, time):
    return None
  
  def Position_and_Velocity_WRT(self, body_ref, time):
    '''Returns position and velocity of measured body
    with respect to a reference body, both of Body.'''
    #Reference body's barycentric position and velocity
    P0V0 = body_ref.Position_and_Velocity(time)
    #Measured body's barycentric position and velocity
    PV = self.Position_and_Velocity(time)
    #Measured body's position and velocity with respect 
    #to reference body
    pv = np.subtract(PV, P0V0)
    #Returns (2,3) numpy array
    return pv
  
  def Update_Position_and_Velocity(self, time):
    '''This function takes as its argument time,
    which will be obtained from the time step of
    the simulation, and updates the historical
    arrays, namely: (1,_) times, (_,3) positions,
    and (_,3) velocities.'''
    #Barycentric position and velocity of body at time (2,3)
    pv = self.Position_and_Velocity(time)
    #Append results to history keeping list for this body
    self.positions = np.vstack([self.positions, pv[0, :]])
    self.velocities = np.vstack([self.velocities, pv[1, :]])
    #Also returns barycentric position and velocty
    return None
  
  def Plot_3D(self, figure):
    ax = figure.gca(projection = '3d')
    ax._axis3don = False
    x = self.positions[:, 0]
    y = self.positions[:, 1]
    z = self.positions[:, 2]
    ax.plot(x, y, z)
    plt.show()
    return None

class Celestial_Body(Body):
  '''
  A celestial body is any natural body outside of
  Earth's atmosphere. Examples are the Moon,
  Sun, and other planets outside our solar system.
  '''
  
  #Instance record
  _instances = []
  
  def __init__(self, name, mass = None, satellites = True):
    
    #Fundamentally initialise the celestial body
    Body.__init__(self, name, mass)
    #Assign its unique attributes
    Assign_Celestial_Body_Attributes(self)
    
    #If it is specified to include satellites
    if satellites is True:
      
      try:
        #Instantiate the dictionary of satellite collections
        sat_dic = Satellite_Dictionary(name)
        #List of satellite collection types
        for sat_type in sat_dic.keys():
          #Instantiate the satellite collection type
          sct = Satellites()
          #List of collections within that type
          for sat_col in sat_dic[sat_type].keys():
            #Instantiate the satellite collection
            sc = Satellite_Collection(sat_col, self)
            sc.satellite_type = sat_type
            #List of object of that satellite
            for sat_obj in sat_dic[sat_type][sat_col].keys():
              #Instantiate the object as a Satellite instance
              s = Satellite(sat_obj, self)
              #Line 1 of the TLE for this object
              s.line1 = sat_dic[sat_type][sat_col][sat_obj][0]
              #Line 2
              s.line2 = sat_dic[sat_type][sat_col][sat_obj][1]
              #Assign the satellite object to its collection
              setattr(sc, sat_obj, s)
              pass
            setattr(sct, sat_col, sc)
            pass
          setattr(self, 'Satellites', sct)
          pass
        pass
      except:
        pass
      pass
    Celestial_Body._instances.append(self)
    return None
  
  def Position_and_Velocity(self, time):
    return Position_and_Velocity_Celestial_Body(self, time)
  pass


class Satellite(Body):
  '''
  A satellite is a moon, planet or machine that
  orbits a planet or star. For example, Earth is
  a satellite because it orbits the sun. Likewise,
  the moon is a satellite because it orbits Earth.
  Usually, the word "satellite" refers to a machine
  that is launched into space and moves around
  Earth or another body in space.
  '''
  #Instance tracking
  _instances = []
  
  def __init__(self, name,  attracting_body, mass = None):
    Body.__init__(self, name, mass)
    #The attracting body of the satellite
    self.attracting_body = attracting_body
    Satellite._instances.append(self)
    return None
  
  def Position_and_Velocity(self, time):
    return Position_and_Velocity_Satellite(self, time)
  pass

class Satellite_Collection(object):
  '''Acts as a namespace organising satellites'''
  def __init__(self, name, attracting_body):
    #The name of the collection
    self.name = name
    #The name of its attracting body
    self.attracting_body = attracting_body
    return None
  pass

class Satellites(object):
  '''Acts as a namespace organising satellite'''
  def __init__(self):
    return None
  pass



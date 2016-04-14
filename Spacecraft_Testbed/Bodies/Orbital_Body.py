'''
Orbital_Body.py

This package aims to attriute orbital bodies, defined with
particular physical attirbutes, to previously defined massive
celestial bodies.
'''

#Import Massive_Body.py in order to configure objects
import Massive_Body
#Obviously import the numpy linear algebra library
import numpy as np
#Import recent wgs84 gravity model for SGP4 propogator
from sgp4.earth_gravity import wgs72 as gravity_constant
#Import TLE translator
from sgp4.io import twoline2rv
#Import to convert julian date to conventional date
from sgp4.ext import invjday
#Import os for file path navigation
import os


class Orbital_Body(object):
  '''This class describes an object orbiting about its attracting body.
  Naturally, the initialisation of such an orbital body takes as its
  arguments the attracting body.'''
  def __init__(self, attracting_body, orbital_body_collection, name):
    #If the object used to initialise the orbital body is not derrived from
    #the Massive_Body class, than raise an error.
    if not isinstance(attracting_body, Massive_Body.Massive_Body):
      raise ValueError('Cannot assign orbital body to type not of Massive_Body')
    #The name of the orbital body
    self.name = name
    #Define the orbital body's attracting body
    self.attracting_body = attracting_body
    #The orbital body collection whom the orbital body pertains to
    self.orbital_body_collection = orbital_body_collection
    #History list of time
    self.times = np.empty(shape = (0, 0), dtype = float)
    #History list of 3 dimensional position vectors [m]
    self.positions = np.empty(shape = (0, 3), dtype = float)
    #History list of 3 dimensional velocity vectors [m]
    self.velocities = np.empty(shape = (0, 3), dtype = float)
  def Position_and_Velocity(self, time):
    '''This function generates the barycentric position and velocity of
    the orbital body at a specified time with the use of the
    SGP4 propogator.'''
    #The time to find the position and velocity at
    t = time
    #The first line of the orbital body's TLE
    line1 = self.TLE_line1
    #The second line of the orbital body's TLE
    line2 = self.TLE_line2
    #Fictitiously instantiate a SGP4 satellite object
    sat = twoline2rv(line1, line2, gravity_constant)
    #Convert Julian date to conventional
    time_conv = invjday(time)
    #Compute the geocentric position and velocity of the orbital body
    p, v = sat.propagate(*time_conv)
    #Turn the tuples into arrays
    p = np.asarray(p)
    v = np.asarray(v)
    #Convert km to m
    p = p * 1e3
    #Convert km/s to m/s
    v = v * 1e3
    #Compute the barycentric position and velocity of the attracting body
    P, V = self.attracting_body.Position_and_Velocity(time)
    #Compute the barycentric position of the orbital body
    p = p + P
    #compute the barycentric velocity of the orbital body
    v = v + V
    return p, v
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
class Orbital_Body_Collection(object):
  '''This class describes a collection of orbital bodies defined
  by the Orbital_Body class'''
  def __init__(self, attracting_body, name):
    #Check if the attracting body is of the Massive_Body class
    if not isinstance(attracting_body, Massive_Body.Massive_Body):
      raise ValueError('Cannot assign collection to type not of Massive_Body')
    #The name of the collection
    self.name = name
    #The name of the attracting body
    self.attracting_body = attracting_body

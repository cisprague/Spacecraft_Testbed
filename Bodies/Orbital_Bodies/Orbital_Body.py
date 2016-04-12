'''
Orbital_Body.py

This package aims to attriute orbital bodies, defined with
particular physical attirbutes, to previously defined massive
celestial bodies.
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
'''

#Import necessary modules
import sys
#Append the directory in which Massive_Body.py is located in
sys.path.append('../')
#Import Massive_Body.py in order to configure objects
from Massive_Body import Massive_Body
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

def TLE_Dictionary(file_path):
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
def Orbital_Body_Dictionary(attracting_body):
  '''This function takes as its arguement an attracting body of the
  Massive_Body class and generates a dictionary of all its orbital
  body collections and their individual orbital bodies'''
  #Instantiate the name of the attracting body
  attracting_body = attracting_body.name   
  #Initialise the dictionary of collections and bodies
  dictionary = {}  
  #The directory at runtime
  path = os.getcwd()
  #Acknowledge the personal absolute path
  path = path.split('Spacecraft_Testbed')[0]
  #Concatenate the absolute path with the ubiquitous relative path
  path = path + 'Spacecraft_Testbed/Bodies/Orbital_Bodies/Attracting_Bodies'
  path1 = path + '/' + attracting_body 
  for collection in os.listdir(path1):
    dictionary[collection] = {}
    path2 = path1 + '/' + collection
    for f_name in os.listdir(path2):
      if f_name.endswith('.tle'):
        f_path = path2 + '/' + f_name
        TLE = TLE_Dictionary(f_path)
        TLE_keys = TLE.keys()
        for key in TLE_keys:
          dictionary[collection][key] = TLE[key]
  return dictionary
def Assign_Orbital_Bodies(attracting_body):
  '''This function is to be implemented within the Massive_Body class
   to assign orbital bodies to a massive body.'''
  #Name of massive body for which the orbital body will be assigned to
  name = attracting_body.name
  #The dictionary of all collections and their orbital bodies
  catalogue = Orbital_Body_Dictionary(attracting_body)
  #List of collections
  collections = catalogue.keys()
  #For every collection in the catalogue
  for col in collections:
    #Create a orbital body collection
    Collection = Orbital_Body_Collection(attracting_body, col)
    #Assign the collection to the attracting body
    setattr(attracting_body, col, Collection)
    #List of orbital bodies
    bodies = catalogue[col].keys()
    #For every orbital body in the collection
    for body in bodies:
      #Classify the orbital body under the Orbital_Body class
      Body = Orbital_Body(attracting_body, Collection, body)
      #Instantiate the 1st line of the body's TLE
      Body.TLE_line1 = catalogue[col][body]['line1']
      #Instantiate the 2nd line of the body's TLE
      Body.TLE_line2 = catalogue[col][body]['line2']
      #Assign the body to the attracting body and collection
      setattr(attracting_body.__dict__[col], body, Body)
class Orbital_Body(object):
  '''This class describes an object orbiting about its attracting body.
  Naturally, the initialisation of such an orbital body takes as its
  arguments the attracting body.'''
  def __init__(self, attracting_body, orbital_body_collection, name):
    #If the object used to initialise the orbital body is not derrived from
    #the Massive_Body class, than raise an error.
    if not isinstance(attracting_body, Massive_Body):
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
    if not isinstance(attracting_body, Massive_Body):
      raise ValueError('Cannot assign collection to type not of Massive_Body')
    #The name of the collection
    self.name = name
    #The name of the attracting body
    self.attracting_body = attracting_body
#Examples
jd = np.array([2457061.5, 2457062.5, 2457063.5, 2457064.5])
Earth = Massive_Body('Earth')
Assign_Orbital_Bodies(Earth)
Sat = Earth.Cosmos_2251.COSMOS_2251_DEB
Mars = Massive_Body('Mars')
print Sat.Position_and_Velocity_WRT(Mars, jd[0])
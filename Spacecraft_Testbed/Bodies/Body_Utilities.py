'''
Utilities.py
This module contains all the necessary modules
involved in the construction of classes.
'''

#Import os for file specification
import os
#Import relevant module
from Orbital_Body import Orbital_Body, Orbital_Body_Collection
#Specify the directory of this file
Directory = os.path.dirname(__file__)
#Import web adress reading for the heavy .bsp epheride file
import urllib

def isfloat(value):
  '''Determines whether an object is a float'''
  try:
    float(value)
    #Return True if value is indeed a float
    return True
  except ValueError:
    #Rightfully return False if value is not a float
    return False

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

def Orbital_Body_Dictionary(attracting_body):
  '''This function takes as its arguement an attracting body of the
  Massive_Body class and generates a dictionary of all its orbital
  body collections and their individual orbital bodies'''
  #Instantiate the name of the attracting body
  attracting_body = attracting_body.name   
  #Initialise the dictionary of collections and bodies
  dictionary = {}  
  #Concatenate the absolute path with the ubiquitous relative path
  path0 = Directory + '/Information/'
  if attracting_body in os.listdir(path0):
    path1 = path0 + attracting_body + '/Orbital_Bodies/'
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

def Make_Massive_Body_Information():
  #Master dictionary for body information
  Body_Information = {}
  #Indicies for use in jplephem 2.5
  jplephem_Indicies = {'Mercury': (1, 199),   #Mercury barycentre with respect to solar system barycentre
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
  path = Directory + '/Information/Planetary_Information'
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
def Ephemeris_Pressence(Directory):
  if not isinstance(Directory, str):
    raise ValueError('Object must be a string.')
  Pressence = None
  for f_name in os.listdir(Directory):
    if f_name.endswith('.bsp'):
      Pressence = True
      break
    else:
      Pressence = False
  return Pressence
def Install_Ephemeris_Question():
  ans = raw_input('Would you like to install an ephemeris?')
  ans = ans.strip()
  ans = ans.lower()
  ans = ans[0]
  if ans == 'y':
    print 'Installing'
    ans = True
  elif ans == 'n':
    raise ValueError('Aborting.')
  else:
    raise ValueError('Did not recognise answer.')
  return ans
def Install_Ephemeris(Directory, f_name):
  if Ephemeris_Pressence(Directory):
    return
  else:
    if Install_Ephemeris_Question():
      urllib.urlretrieve('http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp', f_name)
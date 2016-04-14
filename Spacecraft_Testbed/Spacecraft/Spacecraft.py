'''
Spacecraft.py
This class describes a spacecraft that may
defined anywhere in interplanetary space.
'''

class Spacecraft(object):
  def __init__(self,
               name = 'Satellite',
               mass = 4.00,
               max_thrust = 11.16,
               specific_impulse = 220.00):
    #The mass of the spacecraft
    self.mass = mass
    #The max thrust the spacecraft can produce
    self.max_thrust = max_thrust
    #The specific impulse of the spacecraft
    self.isp = specific_impulse
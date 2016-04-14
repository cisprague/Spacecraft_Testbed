#Initialise test contexts
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
#Class describing massive celestial bodies of solar system
from Spacecraft_Testbed.Bodies.Massive_Body import Massive_Body
#Class describing orbital bodies of massive celestial bodies
from Spacecraft_Testbed.Bodies.Orbital_Body import Orbital_Body
#Class describing spacecraft
from Spacecraft_Testbed.Spacecraft.Spacecraft import Spacecraft
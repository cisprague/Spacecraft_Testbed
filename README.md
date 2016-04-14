#Spacecraft Testbed
This package models both the geocentric and interplanetary environmnet with the aim to facilate the testing and development of various types spacecraft guidance, navigation, and control schemes. 
##It's as easy as this
```python
#Import the necesary modules
from context import Massive_Body, Orbital_Body
#Instantiate Earth as a massive celestial object
Earth = Massive_Body('Earth')
#Instantiate Mars as a massive celestial object
Mars = Massive_Body('Mars')
#Instantiate the debris fragment as an orbital body
Sat = Earth.Fengyun_1C.Fengyun_1C_Deb_102
#Times at which to compute position and velocity
times = [2457061.5, 2457062.5, 2457063.5, 2457064.5]
#Compute the position and velocity of the debris
#fragment with respect to the centre of Mars.
p, v = Sat.Position_and_Velocity_WRT(Mars, times[0])
```

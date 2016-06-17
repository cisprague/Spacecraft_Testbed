#Spacecraft Testbed

[![Join the chat at https://gitter.im/CISprague/Spacecraft_Testbed](https://badges.gitter.im/CISprague/Spacecraft_Testbed.svg)](https://gitter.im/CISprague/Spacecraft_Testbed?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
This package models both the geocentric and interplanetary environment with the aim to facilitate the testing and development of various types spacecraft guidance, navigation, and control schemes.
<img src="https://cdn.rawgit.com/CISprague/Spacecraft_Testbed/master/tests/Figures/Fengyun_and_Earth_Barycentric_1.svg">
##It's as easy as this
```python
#Import the necessary modules
from context import Massive_Body
#Instantiate Earth as a massive celestial object
Earth = Celestial_Body('Earth')
#Instantiate Mars as a massive celestial object
Mars = Celestial_Body('Mars')
#Instantiate the debris fragment as an orbital body
Sat = Earth.Satellites.Fengyun_1C.Fengyun_1C_Deb_102
#Times at which to compute position and velocity
times = [2457061.5, 2457062.5, 2457063.5, 2457064.5]
#Compute the position and velocity of the debris
#fragment with respect to the centre of Mars.
p, v = Sat.Position_and_Velocity_WRT(Mars, times[0])

#Show results
print('The position [km] and velocity [km/s] of')
print('Fengyun_1C_Deb_102 with respect to the centre of Mars:')
print('Position:'), p * 1e-3
print('Velocity: '), v * 1e-3
```
```
The position [km] and velocity [km/s] of
Fengyun_1C_Deb_102 with respect to the centre of Mars:
Position: [ -3.16064398e+08   4.67978840e+07   2.47605342e+07]
Velocity:  [-15.22992539 -49.26948181 -14.59125297]
```

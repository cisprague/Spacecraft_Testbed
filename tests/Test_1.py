# Import the necesary modules
from context import *

'''In this test we will try three dimensionally
plotting Earth and some of its satellites from
a barycentric persepctive.'''

# Firstly instantiate Earth as a Celestial Body instance
Earth = Celestial_Body('Earth')
Moon  = Celestial_Body('Moon')
Mars  = Celestial_Body('Mars')
Venus = Celestial_Body('Venus')

# Times
times = np.linspace(2457388.000000, 2457392.200000, 1000)

# Spacecraft
SC = Spacecraft('CubeSat', Satellite._instances[0].Position_and_Velocity(times[0]), times[0])
#print SC.deriv(Celestial_Body._instances)

print SC.positions
print SC.velocities
print SC.accelerations

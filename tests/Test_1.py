# Import the necesary modules
from context import *

# Instantiate Earth and Moon and their satellites
Earth = Celestial_Body('Earth')
Moon  = Celestial_Body('Moon')

# Times
times = np.linspace(2457388.000000, 2457392.200000, 1000)

# Main module of Fengyun 1C
Sat = Earth.Satellites.Fengyun_1C.Fengyun_1C

# Instantiate Spacecraft
epoch_t = times[0]
epoch_p, epoch_v = Sat.Position_and_Velocity(epoch_t)
SC = Spacecraft('CubeSat', epoch_p, epoch_v, epoch_t)

for body in Celestial_Body._instances:
    g = SC.Gravitational_Acceleration(body)
    print('The gravitational acceleration in m/s^2 due to ' + body.name + ':')
    print('In vector form: ' + str(g))
    print('As magnitude: '   + str(np.linalg.norm(g)))

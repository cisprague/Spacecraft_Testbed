# Import the necesary modules
from context import *

# Instantiate Earth and Moon and their satellites
Earth            = Celestial_Body('Earth')
Moon             = Celestial_Body('Moon')
Sun              = Celestial_Body('Sun')

# Breeze satellites debris fragment just below altitude of ISS
Sat              = Earth.Satellites.Breeze.Breeze_M_Deb_10

# Times
times            = np.linspace(2457388.000000, 2457392.200000, 1000)
epoch_t          = times[0]
epoch_p, epoch_v = Sat.Position_and_Velocity(epoch_t)

# Spacecraft
SC = Spacecraft('CubeSat', epoch_p, epoch_v, epoch_t)
# Altitude in km
alt = SC.Altitude(Earth) * 1e-3
print SC.Aerodynamic_Acceleration(Earth)

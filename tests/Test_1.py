#Import the necesary modules
from context import *

'''In this test we will try three dimensionally
plotting Earth and some of its satellites from
a barycentric persepctive.'''

#Firstly instantiate Earth as a Celestial Body instance
Earth = Celestial_Body('Earth', satellites = True)

#Earth's satellites were already automatically
#instantiated as Satellite instances, so they may
#be readily accesed

#Our time range to plot
#From January 1st to 2nd , 2016 w/ 1000 point resolution
times = np.linspace(2457388.000000, 2457389.000000, 1000)

#Insantate the figure for our plot
fig = plt.figure

#For Earth and 10 of its satellites
for celestial_body, satellite in zip(Celestial_Body._instances, Satellite._instances[:10]):
  #For every time step in our time range
  for time in times:
    #Update the position and velocity of our bodies
    Celestial_Body.Update_Position_and_Velocity(time)
    Satellite.Update_Position_and_Velocity(time)
    pass
  #Now plot their position time-traces
  celestial_body.Plot_3D(fig)
  satellite.Plot_3D(fig)
  pass

#Be patient, this will take about 20 seconds.
#NUMBA JIT compillation will be implemented soon!

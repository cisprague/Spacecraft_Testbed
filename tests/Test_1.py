#Import the necesary modules
from context import *

'''In this test we will try three dimensionally
plotting Earth and some of its satellites from
a barycentric persepctive.'''

#Firstly instantiate Earth as a Celestial Body instance
Earth = Celestial_Body('Earth')

#Earth's satellites were already automatically
#instantiated as Satellite instances, so they may
#be readily accesed

#Our time range to plot
#From January 1st to 2nd , 2016 w/ 1000 point resolution
times = np.linspace(2457388.000000, 2457390.500000, 2000)

#the figure
fig = plt.figure()

#the satellites
for sat in Satellite._instances[:20]:
  for time in times:
    sat.Update_Position_and_Velocity(time)
    pass
  sat.Plot_3D(fig)
  pass

#the planets
for cb in Celestial_Body._instances:
  for time in times:
    cb.Update_Position_and_Velocity(time)
    pass
  cb.Plot_3D(fig)
  pass
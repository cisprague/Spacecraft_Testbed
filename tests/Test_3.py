'''
In this test, the trajectory of Earth and
its orbital bodies will be plotted.
'''

#Import necessary modules
from context import *
#Instantiate Earth as a massive celestial body
Earth = Celestial_Body('Earth')
Mars = Celestial_Body('Mars')
Mercury = Celestial_Body('Mercury')
#Time at which to begin position computations
epoch = 2457479.500000  #April 1, 2016
#Time at which to end position computations
end = 2457857.500000  #April 14, 2017
#Number of points to plot in time frame
N = 1000
#List of times at which to compute position
times = np.linspace(epoch, end, N)
#Record the position of Earth and its orbital bodies
for time in times:
  Earth.Update_Position_and_Velocity(time)
  Mars.Update_Position_and_Velocity(time)
  Mercury.Update_Position_and_Velocity(time)
#The canvas
fig = plt.figure()
#Plot the points
Earth.Plot_3D(fig)
Mars.Plot_3D(fig)
Mercury.Plot_3D(fig)
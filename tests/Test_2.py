'''
Instantiate a spacecraft
'''
from context import Spacecraft
Sat = Spacecraft('CubeSat', 10, 14, 255)

#Results
print('The max thrust is: ') + str(Sat.max_thrust) + ' Newtons.'
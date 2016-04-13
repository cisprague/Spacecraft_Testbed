import os, sys, inspect
sys.path.append('../Bodies')
from Massive_Body import Massive_Body
import numpy as np
jd = np.array([2457061.5, 2457062.5, 2457063.5, 2457064.5])
Earth = Massive_Body('Earth')
for j in jd:
  p, v = Earth.Update_Position_and_Velocity(j)
  print p
  print v
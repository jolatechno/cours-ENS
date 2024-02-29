#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
TASEP with open boundary conditions
and parallel update
"""
import numpy as np
from random import random
import matplotlib.pyplot as plt

plt.xlabel('position')
plt.ylabel('time')
plt.title('Parallel update')

#########################
# Initialisation
#########################

Linput = input('Taille du systeme? ')
LL= int(Linput) if Linput != '' else 7
tmaxinput = input('Tmax? ')
tmax=int(tmaxinput) if tmaxinput != '' else 15
dtinput = input('Time step dt? ')
dt=float(dtinput) if dtinput != '' else 1
alphainput = input('Entrance rate alpha? ')
alpha=float(alphainput) if alphainput != '' else 0.7
ppinput = input('Stepping rate p? ')
pp=float(ppinput) if ppinput != '' else 1.0
betainput = input('Exit rate beta? ')
beta=float(betainput) if betainput != '' else 0.5

print('L = ',LL)
print('tmax = ',tmax)
print('dt = ',dt)
print('alpha = ',alpha)
print('p = ',pp)
print('beta = ',beta)

palpha = alpha * dt
pbeta = beta * dt
ppp = pp * dt
if palpha > 1 or pbeta > 1 or ppp > 1:
  print("Time step too large for the given rates")
  exit()

lat1 = [0 for i in range(LL)]
lat2 = lat1[:]

for tt in range(tmax):
  # At the beginning of this loop, lat1 and lat2 are identical.

  tps = tt * dt

  #########################
  # Entrance
  #########################
  if lat1[0] == 0:
    if(random() < palpha):
      lat2[0] = 1

  #########################
  # Bulk
  #########################
  for ii in range(LL-1):
    if lat1[ii] == 1 and lat1[ii+1] == 0:
      if(random() < ppp):
        lat2[ii] = 0
        lat2[ii+1] = 1

  #########################
  # Exit
  #########################
  if lat1[LL-1] == 1:
    if(random() < pbeta):
      lat2[LL-1] = 0

  # Be careful that lat1 = lat2 would induces that changes
  # in lat2 are also performed in lat1.
  # We use slicing to avoid this effect.
  lat1 = lat2[:]

  # We have to unpack range to create a list.
  # We rather want only occupied sites:
  lat2plot = [np.nan if kk == 0 else 1 for kk in lat2]
  plt.scatter([*range(1,LL+1)],[dt + tps*jj for jj in lat2plot],color='b')

plt.ylim(0,tps + 2*dt)
plt.show(block=True)

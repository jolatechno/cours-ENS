#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
TASEP with open boundary conditions
and random sequential update.
"""
import numpy as np
from random import random
import matplotlib.pyplot as plt

bavard = False

plt.xlabel('position')
plt.ylabel('time')
plt.suptitle('Random sequential update')
plt.title('Particles at micro-timesteps in red, timesteps in blue')

#########################
# Initialisation
#########################

Linput = input('Taille du systeme? ')
LL= int(Linput) if Linput != '' else 5
tmaxinput = input('Tmax? ')
tmax=int(tmaxinput) if tmaxinput != '' else 15
dtinput = input('Time step dt? ')
dt=float(dtinput) if dtinput != '' else 1.0
alphainput = input('Entrance rate alpha? ')
alpha=float(alphainput) if alphainput != '' else 0.7
ppinput = input('Stepping rate p? ')
pp=float(ppinput) if ppinput != '' else 1.0
betainput = input('Exit rate beta? ')
beta=float(betainput) if betainput != '' else 0.3

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

for tt in range(tmax):

  tps = tt * dt
  if bavard:
    print('tps = ',tps)

  for tt2 in range(LL+1):
    i0 = int(random()*(LL+1)) # Choice of a link (i0-1,i0)
    if i0 == 0:
      #########################
      # Entrance link
      #########################
      if lat1[0] == 0:
        if(random() < palpha):
          lat1[0] = 1
    elif i0 == LL:
      #########################
      # Exit link
      #########################
      if lat1[LL-1] == 1:
        if(random() < pbeta):
          lat1[LL-1] = 0
    else:
      #########################
      # Bulk link i0-1, i0 for 0 < i0 < L
      #########################
      if lat1[i0-1] == 1 and lat1[i0] == 0:
        if(random() < ppp):
          lat1[i0-1] = 0
          lat1[i0] = 1

    if bavard:
      print('i0=',i0)
      print('lat1=',lat1)
    lat1plot = [np.nan if kk == 0 else 1 for kk in lat1]
    plt.scatter([*range(1,LL+1)],[(tps+dt*tt2/(LL+1))*jj for jj in lat1plot],color='r',marker="+")

  # We have to unpack range to create a list.
  # We rather want only occupied sites:
  lat1plot = [np.nan if kk == 0 else 1 for kk in lat1]
  plt.scatter([*range(1,LL+1)],[dt + tps*jj for jj in lat1plot],color='b',marker="o")

plt.ylim(0,tps + 2*dt)
plt.show(block=True)

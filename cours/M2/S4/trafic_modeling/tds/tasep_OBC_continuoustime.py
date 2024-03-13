#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
TASEP with open boundary conditions
and update in continuous time.
"""

class Transition():
 """
 Class for all possible stochastic transitions
 """
 def __init__(self,rate,typ,link):
   self.rate = rate
   self.typ  = typ
   self.link = link

 def __repr__(self):
   return f"t={self.typ}\nr={self.rate}\nl={self.link}"

import numpy as np
from random import random
#from random import seed,random,uniform,sample,choice
import matplotlib.pyplot as plt

bavard = False

plt.xlabel('position')
plt.ylabel('time')
plt.title('Update in continuous time (Gillespie algorithm)')

#########################
# Initialisation
#########################

Linput = input('Taille du systeme? ')
LL= int(Linput) if Linput != '' else 7
tmaxinput = input('Tmax? ')
tmax=int(tmaxinput) if tmaxinput != '' else 15
alphainput = input('Entrance rate alpha? ')
alpha=float(alphainput) if alphainput != '' else 0.7
ppinput = input('Stepping rate p? ')
pp=float(ppinput) if ppinput != '' else 1.0
betainput = input('Exit rate beta? ')
beta=float(betainput) if betainput != '' else 0.3

print('L = ',LL)
print('tmax = ',tmax)
print('alpha = ',alpha)
print('p = ',pp)
print('beta = ',beta)

lat1 = [0 for i in range(LL)]

tps = 0

while tps < tmax:

  ltrans = []
  # building the list of possible transitions

  #########################
  # Entrance
  #########################
  if lat1[0] == 0:
    ltrans.append(Transition(alpha,'I',0))
  #########################
  # Bulk
  #########################
  for ii in range(LL-1):
    if lat1[ii] == 1 and lat1[ii+1] == 0:
      ltrans.append(Transition(pp,'H',ii))
  #########################
  # Exit
  #########################
  if lat1[LL-1] == 1:
    ltrans.append(Transition(beta,'E',LL-1))

  if bavard:
    print(ltrans)

  # When will be the next transition ?
  sumw = sum([rr.rate for rr in ltrans])
  # Tirage selon une distribution exponentielle
  dtnext = np.log(1.0 / random()) / sumw

  tps = tps + dtnext

  # Which transition will be the next?
  sumw = sumw * random()
  while sumw >= 0.0:
      rr = ltrans.pop(0)
      sumw -= rr.rate

  # Perform the transition
  #########################
  # Entrance
  #########################
  if rr.typ == 'I':
      lat1[0] = 1

  #########################
  # Bulk
  #########################
  if rr.typ == 'H':
    lat1[rr.link] = 0
    lat1[rr.link+1] = 1

  #########################
  # Exit
  #########################
  if rr.typ == 'E':
    lat1[LL-1] = 0

  # We have to unpack range to create a list.
  # We rather want only occupied sites:
  lat1plot = [np.nan if kk == 0 else 1 for kk in lat1]
  plt.scatter([*range(1,LL+1)],[tps*jj for jj in lat1plot],color='b')

plt.show(block=True)

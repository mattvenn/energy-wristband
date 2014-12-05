#!/usr/bin/python
"""
functions to turn instant energy readings into energy differences from 1 to 4
"""

import sys
import datetime
import ipdb
import pickle

max_time = 5 * 60 #seconds before we disregard any large changes
num_divs = 4 #relate the change as a number from 1 to num_divs
max_energy = 3000 #watts - this should be adaptive
energy_per_div = max_energy / num_divs
sensitivity = energy_per_div #watts - only show differences more sensitivity

#limits between 1 and num_divs
def limit(energy):
    if energy > num_divs:
        energy = num_divs
    if energy < 1:
        energy = 1
    return energy
    
def diff(energy,logging):
    try:
        with open("hist.pk") as fh:
            last = pickle.load(fh)
    except:
        last = { 'time' : None, 'energy' : None }
        
    dt = datetime.datetime.now()
    #logging.info("got %f W at %s" % (energy, dt))
    last_energy = None
    current_energy = None
    if last['time']:
        diff_time = (dt - last['time']).total_seconds()
        #if it's been too long between samples, start again
        if diff_time < max_time:
            diff_energy = energy - last['energy']
            logging.info("diff energy = %f W" % diff_energy )

            #only if it's a big enough difference
            if abs(diff_energy) > sensitivity:
                #print dt, diff_energy, last_energy, energy
                last_energy = int(last['energy'] / energy_per_div) + 1
                current_energy = int(energy / energy_per_div) + 1

                last_energy = limit(last_energy)
                current_energy = limit(current_energy)

    last['time'] = dt
    last['energy'] = energy
    with open("hist.pk",'w') as fh:
        pickle.dump(last,fh)

    return (last_energy,current_energy)

if __name__ == '__main__':
    energy = float(sys.argv[1])
    diff(energy)

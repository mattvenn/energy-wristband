#!/usr/bin/python

import sys
import datetime
import ipdb
import pickle
import os


max_time = 5 * 60 #seconds before we disregard any large changes
num_divs = 4 #relate the change as a number from 1 to num_divs
max_energy = 2500 #watts - this should be adaptive
energy_per_div = max_energy / num_divs
sensitivity = energy_per_div # 100 #watts - only show differences more sensitivity

#limits between 0 and num_divs
def limit(energy):
    if energy > num_divs:
        energy = num_divs
    if energy < 0:
        energy = 0
    return energy
    
def diff(energy):
    try:
        with open("hist.pk") as fh:
            last = pickle.load(fh)
    except:
        last = { 'time' : None, 'energy' : None }
        
    dt = datetime.datetime.now()
    print("got %f W at %s" % (energy, dt))
    if last['time']:
        diff_time = (dt - last['time']).total_seconds()
        #if it's been too long between samples, start again
        if diff_time < max_time:
            diff_energy = energy - last['energy']
            print("diff energy = %f W" % diff_energy )

            #only if it's a big enough difference
            if abs(diff_energy) > sensitivity:
                #print dt, diff_energy, last_energy, energy
                last_energy = int(last['energy'] / energy_per_div)
                current_energy = int(energy / energy_per_div)

                last_energy = limit(last_energy)
                current_energy = limit(current_energy)
                print("sending: %d %d" % (last_energy, current_energy))
                os.system("../send.py %d %d >> send.log" % (last_energy,current_energy))

    last['time'] = dt
    last['energy'] = energy
    with open("hist.pk",'w') as fh:
        pickle.dump(last,fh)


if __name__ == '__main__':
    energy = float(sys.argv[1])
    diff(energy)

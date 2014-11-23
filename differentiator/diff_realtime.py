#!/usr/bin/python

import sys
import datetime
import ipdb
import pickle


max_time = 5 * 60 #seconds before we disregard any large changes
num_divs = 4 #relate the change as a number from 1 to num_divs
max_energy = 2500 #watts - this should be adaptive
energy_per_div = max_energy / num_divs
sensitivity = energy_per_div # 100 #watts - only show differences more sensitivity

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
                print("sending: %d %d" % ( int(last['energy'] / energy_per_div), int(energy / energy_per_div)))

    last['time'] = dt
    last['energy'] = energy
    with open("hist.pk",'w') as fh:
        pickle.dump(last,fh)


if __name__ == '__main__':
    energy = float(sys.argv[1])
    diff(energy)

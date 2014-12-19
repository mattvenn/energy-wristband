#!/usr/bin/python
"""
functions to turn instant energy readings into energy differences from 1 to 4
"""
import sys
import datetime
import ipdb
import pickle

max_time = 5 * 60  # seconds before we disregard any large changes
num_divs = 4  # relate the change as a number from 1 to num_divs
max_energy = 3000  # watts - this should be adaptive
energy_per_div = max_energy / num_divs
sensitivity = energy_per_div  # watts - only show differences more sensitivity


# limits between 1 and num_divs
def limit(energy):
    if energy > num_divs:
        energy = num_divs
    if energy < 1:
        energy = 1
    return energy


def diff(energy, logging):
    try:
        with open("hist.pk") as fh:
            last = pickle.load(fh)
    except:
        last = {'time': None, 'energy': None}

    dt = datetime.datetime.now()
    # logging.info("got %f W at %s" % (energy, dt))

    # current energy as value from 1 to num_divs
    current_energy = int(energy / energy_per_div) + 1
    current_energy = limit(current_energy)

    # can't do diff unless we have a last time
    if last['time'] is None:
        save_state(dt, energy)
        return(None, current_energy) 


    diff_time = (dt - last['time']).total_seconds()

    # if it's been too long between samples, start again
    if diff_time > max_time:
        save_state(dt, energy)
        return(None, current_energy) 

    diff_energy = energy - last['energy']
    # update last energy history
    save_state(dt,energy)
    logging.info("diff energy = %f W" % diff_energy)

    # last energy as value from 1 to num_divs
    last_energy = int(last['energy'] / energy_per_div) + 1
    last_energy = limit(last_energy)

    # only if it's a big enough difference
    if abs(diff_energy) > sensitivity:
        return (last_energy, current_energy)

    return(None, current_energy)

def save_state(dt, energy):
    last = {}
    last['time'] = dt
    last['energy'] = energy
    with open("hist.pk", 'w') as fh:
        pickle.dump(last, fh)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    energy = float(sys.argv[1])
    print(diff(energy,logging))

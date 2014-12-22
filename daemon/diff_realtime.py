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

# limits between 1 and num_divs
def energy_to_div(energy):
    # convert to div
    div = int(energy / energy_per_div) + 1

    # limit
    if div > num_divs:
        div = num_divs
    if div < 1:
        div = 1

    return div

# returns the last recorded energy, as long as it wasn't too long ago
# in which case, return the current energy
def diff(energy, logging):
    dt = datetime.datetime.now()

    try:
        with open("hist.pk") as fh:
            last = pickle.load(fh)
    except:
        save_state(dt, energy)
        logging.debug("no history")
        return energy

    # save current energy and time
    save_state(dt, energy)

    # if it's been too long between samples, start again
    diff_time = (dt - last['time']).total_seconds()
    if diff_time > max_time:
        logging.debug("time too long to differentiate")
        return energy

    return last['energy']

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

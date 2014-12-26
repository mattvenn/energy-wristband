"""
class to turn instant energy readings into energy differences from 1 to 4
"""

import time


class diff_energy():
    
    max_time = 30  # seconds before we disregard any large changes
    num_divs = 4  # relate the change as a number from 1 to num_divs
    sensitivity = 50 #  in watts per second

    def __init__(self, logging,max_energy=3000):
        self.logging = logging
        self.hist = None
        self.energy_per_div = max_energy / diff_energy.num_divs

    # limits between 1 and num_divs
    def energy_to_div(self,energy):
        # convert to div
        div = int(energy / self.energy_per_div) + 1

        # limit
        if div > diff_energy.num_divs:
            div = diff_energy.num_divs
        if div < 1:
            div = 1

        return div

    def add_hist(self,energy):
        self.hist = {"t": time.time(), "e": energy}

    # returns the last recorded energy, as long as it wasn't too long ago
    # in which case, return the current energy
    def diff(self, energy):

        now = time.time()

        # add new energy to our history
        hist = self.hist
        self.add_hist(energy)

        # no history
        if hist is None:
            return energy

        # too old
        if hist["t"] + diff_energy.max_time < now:
            self.logging.debug("history too old")
            return energy

        self.logging.debug("got hist t=%d e=%d" % (hist["t"],hist["e"]))

        # differentiate
        diff = float(energy - hist["e"]) / (time.time() - hist["t"] )
        diff = abs(diff)

        # if not enough of a change
        self.logging.info("energy diff = %f" % diff)
        if diff < diff_energy.sensitivity: 
            return energy

        # otherwise return historical energy
        return hist["e"]

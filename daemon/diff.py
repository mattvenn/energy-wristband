"""
class to turn instant energy readings into energy differences from 1 to 4
"""

import time
import logging

log = logging.getLogger(__name__)


class diff_energy():
    
    num_divs = 4  # relate the change as a number from 1 to num_divs

    def __init__(self, max_energy=3000, sens=50, max_time=30):
        self.hist = None
        self.energy_per_div = max_energy / diff_energy.num_divs
        self.sens = sens  # in watts per second
        self.max_time = max_time  # seconds before large change disregarded

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

    # records current energy
    # returns the last recorded energy, as long as:
    # * it wasn't too long ago
    # * it was a big enough change from the current
    # otherwise return the current energy
    def get_last_valid(self, energy):

        now = time.time()

        # add new energy to our history
        hist = self.hist
        self.add_hist(energy)

        # no history
        if hist is None:
            return energy

        # too old
        if hist["t"] + self.max_time < now:
            log.debug("history too old")
            return energy

        log.debug("got hist t=%d e=%d" % (hist["t"],hist["e"]))

        # differentiate
        diff = float(energy - hist["e"]) / (time.time() - hist["t"] )
        diff = abs(diff)

        # if not enough of a change
        log.debug("energy diff = %f" % diff)
        if diff < self.sens: 
            return energy

        # otherwise return valid historical energy point
        return hist["e"]

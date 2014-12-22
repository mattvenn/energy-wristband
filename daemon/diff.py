"""
class to turn instant energy readings into energy differences from 1 to 4
"""

import time


class diff_energy():
    
    max_time = 30  # seconds before we disregard any large changes
    min_time = 10  # seconds we have to wait till history point is valid
    num_divs = 4  # relate the change as a number from 1 to num_divs
    max_energy = 3000  # watts - this should be adaptive
    energy_per_div = max_energy / num_divs
    sensitivity = 50 #  in watts per second

    def __init__(self, logging):
        self.logging = logging
        self.hist = []

    # limits between 1 and num_divs
    def energy_to_div(self,energy):
        # convert to div
        div = int(energy / diff_energy.energy_per_div) + 1

        # limit
        if div > diff_energy.num_divs:
            div = diff_energy.num_divs
        if div < 1:
            div = 1

        return div

    def wipe_hist(self):
        self.hist = []

    def add_hist(self,energy,now):
        self.hist.append({"t": now, "e": energy})
    
    def get_hist(self):
        now = time.time()
        #print now
        #print self.hist

        # trim old history points
        self.logging.debug(self.hist)
        self.hist = [p for p in self.hist 
                        if p['t'] + diff_energy.max_time > now]

        #print self.hist
        # find points old enough
        valid = [p for p in self.hist
                    if p['t'] + diff_energy.min_time < now]

        self.logging.debug(valid)
        if len(valid) == 0:
            raise ValueError("not enough history")
    
        #print("valid = ", valid)
        # return oldest valid point
        #print("last point = ", valid[0])
        return valid[0]


    # returns the last recorded energy, as long as it wasn't too long ago
    # in which case, return the current energy
    def diff(self, energy, now=time.time()):
        # add new energy to our history
        self.add_hist(energy,now)

        # get history point
        try:
            hist = self.get_hist()
        except ValueError as e:
            self.logging.debug(e)
            return energy

        self.logging.debug("got hist t=%d e=%d" % (hist["t"],hist["e"]))

        # differentiate
        diff = float(energy - hist["e"]) / (time.time() - hist["t"] )
        diff = abs(diff)

        # if not enough
        self.logging.debug("diff = %f" % diff)
        if diff < diff_energy.sensitivity: 
            return energy

        # otherwise return historical energy
        return hist["e"]

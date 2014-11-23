import datetime
import dateutil.parser
import ipdb

with open("history.csv") as fh:
    hist = fh.readlines()

#get rid of top line
hist.pop(0)

max_time = 5 * 60 #seconds before we disregard any large changes
num_divs = 4 #relate the change as a number from 1 to num_divs
max_energy = 2500 #watts - this should be adaptive
energy_per_div = max_energy / num_divs
sensitivity = energy_per_div # 100 #watts - only show differences more sensitivity

last_dt = None
for line in hist:
    
    (date_time,energy,temp,line_ending) = line.split(',')
    energy = float(energy)
    dt = dateutil.parser.parse(date_time)
    if last_dt:
        diff_time = (dt - last_dt).total_seconds()
        #if it's been too long between samples, start again
        if diff_time > max_time:
            last_dt = None
            continue

        diff_energy = energy - last_energy

        #only if it's a big enough difference
        if abs(diff_energy) > sensitivity:
            #print dt, diff_energy, last_energy, energy
            print dt, int(last_energy / energy_per_div), int(energy / energy_per_div)

    last_dt = dt
    last_energy = energy


__author__ = 'margot'

import lvmr
import sys

files = sys.argv[0]
parameters = sys.argv[0].split()

rd = lvmr.Reducer(10, 400)

for file in files:
    if rd.integrate(file) is True:
        break

if rd.plotter() is True:
    print("All pulses complete. Please check your laser folder for plots and data.")
else:
    print("The program was unable to complete. Please try again.")
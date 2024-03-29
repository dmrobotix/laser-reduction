__author__ = 'margot paez'

import lvmr
from os import listdir
from os.path import isfile, join
import argparse
import re


parser = argparse.ArgumentParser(prog='python3 lvm-main.py', description='Reduce laser data. Any questions? '
                                                                         'Ask Margot: margot.paez@jpl.nasa.gov or '
                                                                         'mpz@ucsc.edu!')
parser.add_argument(type=int, dest='begin_pulse', help='the starting pulse number (count begins at 1)')
parser.add_argument(type=int, dest='end_pulse', help='the last pulse to get data from')
parser.add_argument(type=str, dest='location', help='the directory that contains the laser files, use full path!')

results = parser.parse_args()
begin = results.begin_pulse
end = results.end_pulse
mypath = results.location

# function for mapping taken from:
# http://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python
numbers = re.compile(r'(\d+)')


def numericalsort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

# process files
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

rd = lvmr.Reducer(begin, end)

for file in sorted(files, key=numericalsort):
    path = join(mypath, file)
    if rd.integrate(path) is True:
        break

if rd.plotter() is True:
    print("All pulses complete. Please check your laser folder for plots and data.\n")
else:
    print("The program was unable to complete. Please try again.\n")

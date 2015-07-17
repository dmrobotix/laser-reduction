__author__ = "Margot Paez"

import matplotlib.pylab as py
import os
import random
import numpy as np
from string import ascii_lowercase, digits


class Reducer(object):
    def __init__(self, begin, end):
        """ Reduces raw data from laser power testing using LabView and DAQ """
        self.__begin = begin
        self.__end = end
        self.__ingvolt = []
        self.__ingphot = []
        self.__ingcurr = []
        self.__ingttl = []
        self.__pulse = 0
        self.__counter = 0
        self.__directory = ''.join(random.choice(ascii_lowercase+digits) for _ in range(6))

        # check that the directory already exists
        if os.path.isdir("results") is False:
            os.makedirs("results/%s" % self.__directory)
        else:
            while os.path.isdir("results/%s" % self.__directory) is True:
                    self.__directory = ''.join(random.choice(ascii_lowercase+digits) for _ in range(6))
            os.mkdir("results/%s" % self.__directory)

    def integrate(self, filename):
        """ Pulls in data from the file and integrates the column data """

        # open the file
        fl = open(filename, 'r')
        for line in fl:
            # look for the last line of the header
            if line == "***End_of_Header***":
                break

        # skip the next line
        fl.readline()

        # continue reading the lines
        for line in fl:
                # the rest of the lines in the file are columns for various parameters
                # recorded during measurement determine if the values are within the pulse range

                self.__counter += 1

                if self.__begin <= self.__pulse <= self.__end:
                    # split the line
                    values = line.split()

                    # roh only wants them summed not truly integrated in the traditional sense
                    self.__ingvolt += values[1]
                    self.__ingphot += values[2]
                    self.__ingcurr += values[3]
                    self.__ingttl += values[4]

                elif self.__pulse < self.__begin:
                    # don't do anything with the data, just keep count of the data/pulse
                    self.__counter += 1

                elif self.__pulse > self.__end:
                    # complete integration and stop reading the file
                    self.__ingvolt = np.array(self.__ingvolt)
                    self.__ingphot = np.array(self.__ingphot)
                    self.__ingcurr = np.array(self.__ingcurr)
                    self.__ingttl = np.array(self.__ingttl)

                    # close the file and exit the function
                    fl.close()

                    return True

                if self.__counter == 200:
                    self.__counter = 0
                    self.__pulse += 1

    def plotter(self):
        """ Takes the integration data and plots them as histogram and line plots and saves them into
         a user defined directory """
        # duration of each pulse is 200 microseconds
        duration = 200e-06
        pulsedist = (self.__end - self.__begin)
        t = []

        for pulse in range(pulsedist+2):
            t.append(pulse*duration)

        results = {"Voltage": self.__ingvolt,
                   "Photo Diode": self.__ingphot,
                   "Current": self.__ingcurr,
                   "TTL Output": self.__ingttl}

        for parameter in results.keys():
            py.hist(results[parameter], bins=165, log=True)
            py.xlabel(parameter)
            py.title("Integrated %s Histogram" % parameter)
            py.savefig("results/%s/%s-hist.png" % (self.__directory, parameter))

            py.plot(t, results[parameter])
            py.xlabel("Time (microsecs)")
            py.ylabel(parameter)
            py.title("Line Plot for Integrated %s" % parameter)
            py.savefig("results/%s/%s-line.png" % (self.__directory, parameter))

        return True

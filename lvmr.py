__author__ = "Margot Paez"

import matplotlib.pylab as py
import os
import random
import numpy as np

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

    def integrate(self, filename):
        """ Pulls in data from the file and integrates the column data """

        # open the file
        fl = open(filename, 'r')

        # read each line
        for line in fl:
            # look for the last line of the header
            if line == "***End_of_Header***":
                break

        # skip the next line
        fl.readline()

        # continue reading the lines
        for line in fl:
                # the rest of the lines in the file are columns for various parameters recorded during measurement
                # determine if the values are within the pulse range

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

    def plotter(self, directory):
        """ Takes the ingration data and plots them as histogram and line plots and saves them into
         a user defined directory """

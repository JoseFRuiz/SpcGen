#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:20:08 2017

@author: josef
"""

#import os, path
#import glob
import numpy as np
import audioop
import wave

# Default values
SAMPLE_RATE = 24000     # Output/test data sample rate
Q_FACTOR = 1            # Additional linear quantization (for testing only)

def open_input(filename):
    stream = wave.open(filename,"rb")

    input_num_channels = stream.getnchannels()
    input_sample_rate = stream.getframerate()
    input_sample_width = stream.getsampwidth()
    input_num_frames = stream.getnframes()

    raw_data = stream.readframes(input_num_frames) # Returns byte data
    stream.close()

    total_samples = input_num_frames * input_num_channels

    print "Sample Width: {} ({}-bit)".format(input_sample_width, 8 * input_sample_width)
    print "Number of Channels: " + str(input_num_channels)
    print "Sample Rate " + str(input_sample_rate)

    print "Number of Samples: " + str(total_samples)
    print "Duration: {0:.2f}s".format(total_samples / float(input_sample_rate))
    print "Raw Data Size: " + str(len(raw_data))

    if input_sample_rate != SAMPLE_RATE:
        u_law = audioop.ratecv(raw_data, input_sample_width, input_num_channels, input_sample_rate, SAMPLE_RATE, None)
        u_law = audioop.lin2ulaw(u_law[0], input_sample_width)
    else:
        u_law = audioop.lin2ulaw(raw_data, input_sample_width)

    u_law = list(u_law)
    u_law = [ord(x)//Q_FACTOR for x in u_law]

    return np.asarray(u_law), input_sample_rate

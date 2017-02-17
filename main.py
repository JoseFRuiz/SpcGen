#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:14:54 2017

@author: josef
"""

import os, sys
sys.path.append(os.getcwd())
#import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.misc
import glob

### My packages
import libwav

### Load *.wav
disp=True
window_size_in_sec=0.2
overlap_ratio = 0.9400
files=glob.glob("Input/*.wav")

for namefile in files:
    print(namefile)
    aud, fs=libwav.open_input(namefile)
    ### Generate spectrogram
    spectro_window = window_size_in_sec*fs; # Windows value for spectrogram function
    window = signal.hamming(spectro_window)
    nperseg=spectro_window
    noverlap = nperseg-int(overlap_ratio*nperseg)
    f, t, Sxx = signal.spectrogram(aud, fs, window, nperseg,noverlap, nfft=None,
                               detrend='constant', return_onesided=True,
                               scaling='density',axis=-1, mode='psd')
    scipy.misc.imsave('Output/'+namefile[6:-4]+'.bmp', Sxx)
    if disp:
        plt.pcolormesh(t, f, Sxx)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()
        raw=raw_input('Press any key to continue: ')
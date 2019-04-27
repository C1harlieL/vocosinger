from __future__ import division, print_function, absolute_import
import scipy.constants as const
import scipy
from scipy.io import wavfile
from scipy import signal
import numpy as np
from numpy import sin, pi, arange, array
import struct
import warnings


# np.seterr(divide='ignore', invalid='ignore')

# Time stretching #

def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]

def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """

    phase  = np.zeros(window_size)
    zpadding = np.zeros(int(window_size*0.9))
    padding = np.concatenate(([1], zpadding))
    sound_array = np.concatenate((padding, sound_array))
    hanning_window = np.hanning(window_size)
    result = np.zeros( int(len(sound_array) /f + window_size))

    for i in np.arange(0, len(sound_array)-(window_size+h), h*f):
        i = int(i)
        # two potentially overlapping subarrays
        a1 = sound_array[i: i + window_size]
        a2 = sound_array[i + h: i + window_size + h]

        # resynchronize the second array on the first
        s1 =  np.fft.fft(hanning_window * a1)
        s2 =  np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

        # add to result
        i2 = int(i/f)
        result[i2 : i2 + window_size] += hanning_window*a2_rephased.real

    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)

    return result.astype('int16')

# pitch shifting

def pitchshift(snd_array, n, window_size=2**11, h=2**7):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)

def wavWrite(filename, data, rate=44100):
    """ Writes data to a .WAV file """
    wavfile.write(filename, rate, (2**15*data).astype(np.int16))
"""
def main():
    print("vocoder started")
    fps, soundwav = wavfile.read("hello.wav")
    output = pitchshift(soundwav, 20)
    tmp = np.interp(output, (output.min(), output.max()), (-1, +1))
    print("fps of sound file = ", fps)
    wavWrite("hello4.wav", tmp, fps)

if __name__ == "__main__": main()

"""

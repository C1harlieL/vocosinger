from gtts import gTTS
from os import path
from pydub import AudioSegment
import os
import argparse
from phasevocoder import speedx, stretch, pitchshift, wavWrite
from scipy.io import wavfile
import numpy as np
import subprocess

parser = argparse.ArgumentParser(description='Test to speech')
parser.add_argument('-t', '--textin', action='store', dest='textin', default='hey beesh', help='put your text after this')
parser.add_argument('integers', metavar='N', type=int, nargs='+', help='integers for pitch shift')

args = parser.parse_args()
textIn = args.textin
textIn = textIn.split()
pitches = args.integers

pad = np.zeros(10)

outfull = np.empty((0, 100))

for i, word in enumerate(textIn):
    tts = gTTS(text=word, lang='en')
    tts.save(word + ".mp3")
    sound = AudioSegment.from_mp3(word+".mp3")
    sound.export(word+".wav", format="wav")
    os.remove(word+".mp3")
    fps, soundwav = wavfile.read(word+".wav")
    out = pitchshift(soundwav, pitches[i])
    outlen = len(out) - 4000
    out = np.delete(out, np.s_[outlen:])
    out = np.delete(out, np.s_[0:1000])
    outfull = np.append(outfull, out)
    os.remove(word+".wav")

tmp = np.interp(outfull, (out.min(), out.max()), (-1, +1))
wavWrite("full.wav", tmp, fps)

def play():
    subprocess.call(["ffplay", "-nodisp", "-autoexit", "full.wav"])

play()

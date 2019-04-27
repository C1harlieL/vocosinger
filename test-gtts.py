from gtts import gTTS
from os import path
from pydub import AudioSegment
import os

tts = gTTS(text="Hello", lang='en', slow=True)
tts.save("pcvoice.mp3")
# to start the file from python
#os.system("start pcvoice.wav")
sound = AudioSegment.from_mp3("pcvoice.mp3")
sound.export("hello.wav", format="wav")

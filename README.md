# Python pitch shifting 'synthesiser' 

Tested on Ubuntu Linux 18.04

Generates wav file then plays it

## Python dependcies

`pip install pydub scipy gtts `

## Other dependecies

- ffmpeg

`sudo apt install ffmpeg`

## Usage

After words in add integer values to shift the voice by:

`-t "<Enter some text to speak here>" 1 4 -7 -3 5 12`

`python vocosinger.py -t "hey hows it going world" 1 5 -3 6 -4`


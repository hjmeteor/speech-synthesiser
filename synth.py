import os
import SimpleAudio as SA
import argparse
from nltk.corpus import cmudict
import re

import string
import wave
import numpy as np

### NOTE: DO NOT CHANGE ANY OF THE EXISITING ARGUMENTS
parser = argparse.ArgumentParser(
    description='A basic text-to-speech app that synthesises an input phrase using monophone unit selection.'
)
parser.add_argument(
    '--monophones',
    default="monophones",
    help="Folder containing monophone wavs")
parser.add_argument(
    '--play',
    '-p',
    action="store_true",
    default=False,
    help="Play the output audio")
parser.add_argument(
    '--outfile',
    '-o',
    action="store",
    dest="outfile",
    type=str,
    help="Save the output audio to a file",
    default=None)
parser.add_argument('phrase', nargs=1, help="The phrase to be synthesised")

# Arguments for extensions
parser.add_argument(
    '--spell',
    '-s',
    action="store_true",
    default=False,
    help="Spell the phrase instead of pronouncing it")
parser.add_argument(
    '--volume',
    '-v',
    default=None,
    type=float,
    help="A float between 0.0 and 1.0 representing the desired volume")

args = parser.parse_args()


class Synth(object):
    def __init__(self, wav_folder):
        self.phones = {}
        self.get_wavs(wav_folder)

    def get_wavs(self, wav_folder):
        for root, dirs, files in os.walk(wav_folder, topdown=False):
            for file in files:
                re_phones = re.compile(r'^(.+)(.wav)$')
                phones = re_phones.match(str(file)).groups()[0].upper()
                self.phones[phones] = os.path.join(wav_folder, file)


def get_normalised_seq(phrase):
    final_seq = ""
    # one way to delete the punctuation
    # tokens = phrase.split()
    # final_seq = " ".join(tokens)

    # the other way to delete the punctuation
    delset = string.punctuation
    final_seq = phrase.translate(None, delset)
    final_seq = final_seq.lower()

    return final_seq


def get_phone_seq(phrase):
    final_seq = ""
    phone_seq = []
    cmudict_ = cmudict.dict()
    tokens = phrase.split()
    # If in cmudict, just use cmudict
    for token in tokens:
        try:
            token = cmudict_[token]
        except KeyError as inst:
            print(inst.args[0] + " is not in the cmudict")
            return []
        phone_seq.append(" ".join(token[0]))
    final_seq = " ".join(phone_seq)
    return final_seq


def load_audio(audio, path):
    # Open the file for reading
    wf = wave.open(path, "rb")
    # Get information from the files header
    audio.format = audio.get_format_from_width(wf.getsampwidth())
    audio.nptype = audio.getNpType(audio.format)
    audio.chan = wf.getnchannels()
    audio.rate = wf.getframerate()
    # Read a chunk of data from the file
    raw = wf.readframes(audio.chunk)
    # Loop while there is data in the file
    while raw != "":
        # Convert the raw data to a numpy array
        array = np.fromstring(raw, dtype=audio.nptype)
        # Append the array to the class data attribute
        audio.data = np.concatenate((audio.data, array), axis=0)
        # Read the next chunk, ready for the next loop iteration
        raw = wf.readframes(audio.chunk)
    # Close the file
    wf.close()


if __name__ == "__main__":
    S = Synth(wav_folder=args.monophones)
    S.get_wavs(os.path.join(os.getcwd(), args.monophones))
    # out is the Audio object which will become your output
    # you need to modify out.data to produce the correct synthesis
    # ut.load(path=os.path.join(os.getcwd(), 'monophones', 'aa.wav'))

    out = SA.Audio(rate=16000)
    print out.data, type(out.data)
    normalised_seq = get_normalised_seq(args.phrase[0])
    phone_seq = get_phone_seq(normalised_seq)
    phone_seq = re.sub(r'[0-9]', '', phone_seq)
    print(str(phone_seq))
    tokens = phone_seq.split()
    for token in tokens:
        token = token.encode("utf-8")
        load_audio(out, path=S.phones[token])
    out.play()
    out.save(args.outfile)

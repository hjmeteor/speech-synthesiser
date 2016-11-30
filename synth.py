import os
import SimpleAudio as SA
import argparse
from nltk.corpus import cmudict
import re

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


def get_normalised_seq_all(phrase):
    phrase = phrase.strip()
    punctuations = r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
    final_seq = ""
    # one way to delete the punctuation
    # tokens = phrase.split()
    # final_seq = " ".join(tokens)

    # the other way to delete the punctuation
    final_seq = phrase.translate(None, punctuations)
    final_seq = final_seq.lower()

    return final_seq


def get_normalised_seq_norm(phrase):
    phrase = phrase.strip()
    punctuations = r'"#$%&\'()*+-/:;<=>@[\]^_`{|}~'
    normal_seq = ""
    final_seq = ""
    final_arr = []
    punctuations = ''
    # one way to delete the punctuation
    # tokens = phrase.split()
    # final_seq = " ".join(tokens)

    # the other way to delete the punctuation
    normal_seq = phrase.translate(None, punctuations)
    normal_seq = normal_seq.lower()
    tokens = normal_seq.split(' ')
    for token in tokens:
        if token[-1] in ',.?!':
            token = token[0:-1] + ' ' + token[-1]
        if token.isdigit():
            token = get_normalised_num(token)
        final_arr.append(token)
    final_seq = " ".join(final_arr)
    return final_seq
def get_normalised_num(phrase):

    final_seq = ""
    num_constant = {0:"zero ", 1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six", 7:"seven",
                8:"eight", 9:"nine", 10:"ten", 11:"eleven", 12:"twelve", 13:"thirteen",
                14:"fourteen", 15:"fifteen", 16:"sixteen", 17:"seventeen", 18:"eighteen", 19:"nineteen" };
    in_hundred_constant = {2:"twenty", 3:"thirty", 4:"forty", 5:"fifty", 6:"sixty", 7:"seventy", 8:"eighty", 9:"ninety"}
    base_constant = {0:" ", 1:"hundred", 2:"thousand", 3:"million", 4:"billion"};

    if phrase[0] == '0' and len(str(number)) > 1:
            final_seq = get_normalised_num(phrase[1:])
            return final_seq
    if int(phrase) < 20:
        final_seq = num_constant[int(phrase)]
        return
        elif int(number) < 100:
            if str(number)[1] == '0':
                return IN_HUNDRED_CONSTANT[int(str(number)[0])];
            else:
                return IN_HUNDRED_CONSTANT[int(str(number)[0])] + "-" + NUMBER_CONSTANT[int(str(number)[1])];
        else:
            locale.setlocale(locale.LC_ALL, "English_United States.1252");
            strNumber = locale.format("%d"    , number, grouping=True);
            numberArray = str(strNumber).split(",");
            stringResult = "";
            groupCount = len(numberArray) + 1;
            for groupNumber in numberArray:
                if groupCount > 1 and groupNumber[0:] != "000":
                    stringResult += str(getUnderThreeNumberString(str(groupNumber))) + " ";
                else:
                    break;
                groupCount -= 1;
                if groupCount > 1:
                    stringResult += BASE_CONSTANT[groupCount] + ",";
            endPoint = len(stringResult) - len(" hundred,");
            #return stringResult[0:endPoint];
            return stringResult;

    if type(eval(phrase)) == int:
    elif type(eval(phrase)) == float:

    if int(num) / 100 == 0:
        if int(num)

    return final_seq

def get_phone_seq(phrase):
    punctuations = ''
    final_seq = ""
    phone_seq = []
    cmudict_ = cmudict.dict()
    tokens = phrase.split(' ')
    # If in cmudict, just use cmudict
    for token in tokens:
        try:
            print(token)
            if token not in ',.?!':
                token = cmudict_[token]
                print(token)
        except KeyError as inst:
            print(inst.args[0] + " is not in the cmudict")
            return []
        phone_seq.append(" ".join(token[0]))
        # print(phone_seq)
        # if punctuation:
        #     print(punctuation)
        #     phone_seq[-1] += ' ' + str(punctuation)
        # punctuation = ''
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


def insert_silence(audio, time):
    if (audio.nptype == np.int8):
        silence = '0'
    elif (audio.nptype == np.int16):
        silence = '00'
    elif (audio.nptype == np.int32):
        silence = '0000'
    elif (audio.nptype == np.int64):
        silence = '00000000'
    # silence = '00'  # " " or hex(0) or chr(0)???
    for i in xrange(0, int(time * audio.rate / audio.chunk)):
        silence_data = silence * audio.chunk
        array = np.fromstring(silence_data, dtype=audio.nptype)
        audio.data = np.concatenate((audio.data, array), axis=0)


def get_letter_seq(phrase):
    phrase = phrase.strip()
    final_seq = ""
    final_arr = []
    tokens = phrase.split(' ')
    for token in tokens:
        if token not in ',.?!':
            token = list(token)
        final_arr.append(" ".join(token))
    final_seq += " ".join(final_arr)
    print(final_seq)
    return final_seq


if __name__ == "__main__":
    # Load the all phones' wavs file
    S = Synth(wav_folder=args.monophones)
    S.get_wavs(os.path.join(os.getcwd(), args.monophones))
    # out is the Audio object which will become your output
    # you need to modify out.data to produce the correct synthesis
    out = SA.Audio(rate=16000)

    #normalise the text (convert to lower case, remove punctuation(exclude ,.?!), etc.)
    normalised_seq = get_normalised_seq_norm(args.phrase[0])
    print(
        '**normalise the text (convert to lower case, remove punctuation(exclude ,.?!), etc.)'
    )
    print(normalised_seq)

    #if set the spell argument true, converting a string into a sequence of letters.
    if args.spell:
        normalised_seq = get_letter_seq(normalised_seq)

    #convert the word sequence to a phone sequence
    phone_seq = get_phone_seq(normalised_seq)
    phone_seq = re.sub(r'[0-9]', '', phone_seq)
    print('**convert the word sequence to a phone sequence')
    print(phone_seq)

    #concatenate the monophone wav files together in the right order to produce synthesised
    #audio.
    tokens = phone_seq.split()
    for token in tokens:
        token = token.encode("utf-8")
        if token in ',':
            insert_silence(out, 0.25)
            print('**inert silence 250ms')
        elif token in '.?!':
            insert_silence(out, 0.5)
            print('**inert silence 500ms')
        else:
            load_audio(out, path=S.phones[token])
            print('**load phones')

    #Allow the user to set the volume argument (--volume, -v) to a value between 0.0 and 1.0.
    out.rescale(args.volume)
    print(args.volume)

    #Play the result
    out.play()
    #Save the result
    out.save(args.outfile)

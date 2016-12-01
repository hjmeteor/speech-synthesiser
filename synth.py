import os
import SimpleAudio as SA
import argparse
from nltk.corpus import cmudict
import re
# what I import
from SimpleAudio import wave
import numpy as np
import datetime

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
                # record the path of every phones in the wav folder
                re_phones = re.compile(r'^(.+)(.wav)$')
                phones = re_phones.match(str(file)).groups()[0].upper()
                self.phones[phones] = os.path.join(wav_folder, file)


# This function is used to get normalised phrase seq(convert to lower/upper case, remove 'all' punctuation, etc.)
# The different between get_normalised_seq_norm function is if remove
# the comma, period, question mark or exclamation mark(which we used to insert some silence) and Left slash(which we used to fomat the date)
def get_normalised_seq_all(phrase):
    phrase = phrase.strip()
    #used to record the final result
    final_seq = ""
    final_arr = []
    #the punctuations Contains all the punctuations defined in the ASCII encoding table
    punctuations = r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
    #the way to delete the punctuation
    final_seq = phrase.translate(None, punctuations)
    #make all sequences become lower case
    final_seq = final_seq.lower()
    return final_seq


# This function is used to get normalised phrase seq(convert to lower/upper case, remove 'the most' punctuation, etc.)
# # The different between get_normalised_seq_norm function is if remove
# the comma, period, question mark or exclamation mark(which we used to insert some silence) and Left slash(which we used to fomat the date)
def get_normalised_seq_norm(phrase):
    phrase = phrase.strip()
    #used to record the final result
    final_seq = ""
    final_arr = []
    record_punctuations = ''

    #the punctuations Contains all the punctuations defined in the ASCII encoding table
    #exclude the comma, period, question mark or exclamation mark(which we used to insert some silence)
    #and Left slash(which we used to fomat the date)
    punctuations = r'"#$%&\'()*+-:;<=>@[\]^_`{|}~'
    # the way to delete the punctuation
    final_seq = phrase.translate(None, punctuations)

    #Process each part of the string
    tokens = final_seq.split(' ')
    for token in tokens:
        #record the punctuation and split it from the part
        if token[-1] in ',.?!':
            record_punctuations = token[-1]
            token = token[0:-1]

        #To determine whether this part is a number (this method also allows us to determine the float type)
        try:
            x = float(token)
        except TypeError:
            pass
        except ValueError:
            pass
        except Exception, e:
            pass
        #if this part of phrase is number, convert them to word sequences
        #by using function get_normalised_num
        else:
            token = get_normalised_num(str(token))

        #Defines the three different format of the dates that can be recognized
        re_date1 = re.compile(r'^\d{2}/\d{2}$')
        re_date2 = re.compile(r'^\d{2}/\d{2}/\d{2}$')
        re_date3 = re.compile(r'^\d{2}/\d{2}/\d{4}$')
        #To determine whether this part is the date(to meet our above requirements of the three requirements)
        if re_date1.match(str(token)):
            try:
                date_time = datetime.datetime.strptime(token, '%d/%m')
            #If the date does not satisfy the requirement
            #(for example, in a non-leap year the date format has such a form as 29/02)
            #An exception is thrown and the program exits
            except ValueError as inst:
                print("*WARNING* ValueError: " + inst.args[0])
                exit(1)
            y = False
            #call function get_normalised_date convert them to word sequences
            token = get_normalised_date(date_time, y)
        elif re_date2.match(str(token)):
            try:
                date_time = datetime.datetime.strptime(token, '%d/%m/%y')
            except ValueError as inst:
                print("*WARNING* ValueError: " + inst.args[0])
                exit(1)
            #y is used to record is there any year in the date
            y = True
            token = get_normalised_date(date_time, y)
        elif re_date3.match(str(token)):
            try:
                date_time = datetime.datetime.strptime(token, '%d/%m/%Y')
            except ValueError as inst:
                print("*WARNING* ValueError: " + inst.args[0])
                exit(1)
            y = True
            token = get_normalised_date(date_time, y)

    #Finally, get each part of the phrase together to become the final output
        final_arr.append(token + ' ' + record_punctuations)
        record_punctuations = ''
    final_seq = " ".join(final_arr)
    #make the final result become lower case
    final_seq = final_seq.lower()
    return final_seq


#this function is used to convert digits phrase to word sequences
#This function supports decimal and integer parts from 0 to 999 billion
def get_normalised_num(phrase):
    #used to record the integer part
    final_seq_int = ""
    #used to record the fractional part
    final_seq_fract = ""
    #used to record the final result
    final_seq = ""
    num_constant = {
        0: "zero ",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen"
    }
    in_hundred_constant = {
        2: "twenty",
        3: "thirty",
        4: "forty",
        5: "fifty",
        6: "sixty",
        7: "seventy",
        8: "eighty",
        9: "ninety"
    }
    base_constant = {
        0: " ",
        1: "hundred",
        2: "thousand",
        3: "million",
        4: "billion"
    }

    phrase_int = ""
    phrase_fract = ""
    #To determine whether it is a decimal, if it contains decimal part
    #the part of left decimal point will be assigned to the integer part
    #the part of right decimal point will be assigned to the fractional part, remove the decimal point
    if type(eval(phrase)) == float:
        for n in range(len(phrase)):
            if phrase[n] == '.':
                phrase_fract = phrase[n + 1:len(phrase) - 1]
                break
            #Assign values to integer parts
            phrase_int += phrase[n]
        #Remove the final number of meaningless 0 in right of the fractional part
        while phrase_fract[-1] == '0':
            phrase_fract = phrase_fract[:-1]

    #if it only contains integer part
    elif type(eval(phrase)) == int:
        phrase_int = phrase
    #Remove any nonsensical zeroes at the left of the integer section
    while phrase_int[0] == '0' and len(phrase_int) > 1:
        phrase_int = phrase_int[1:]

    #This is the case where the integer part is less than 20
    if int(phrase_int) < 20:
        final_seq_int = num_constant[int(phrase_int)] + ' '
    #This is the case where the integer part is less than 100 but greater than 20
    elif int(phrase_int) < 100 and int(phrase_int) >= 20:
        if phrase_int[1] == '0':
            final_seq_int = in_hundred_constant[int(phrase_int[0])] + ' '
        else:
            final_seq_int = in_hundred_constant[int(phrase_int[
                0])] + " " + num_constant[int(phrase_int[1])] + ' '
    #This is the case where the integer part is greater than 100
    else:
        #Add a thousand placeholder to the number
        phrase_int = format(int(phrase_int), ',')
        #Divide the numbers by the thousands placeholder
        num_array = phrase_int.split(",")
        #the number of groups needs to be plus 1
        group_count = len(num_array) + 1
        for group_num in num_array:
            #This flag is used to determine whether there is '000'
            flag = 0
            if group_count > 1:
                if len(group_num) < 3:
                    final_seq_int += get_normalised_num(group_num) + ' '
                elif len(group_num) == 3 and group_num[0:] == "000":
                    flag = 1  #This flag is used to determine whether the flag is '000'
                elif len(group_num) == 3 and group_num[1:] == "00":
                    final_seq_int += num_constant[int(group_num[
                        0])] + " " + base_constant[1] + ' '
                else:
                    final_seq_int += num_constant[int(group_num[
                        0])] + " " + base_constant[
                            1] + " and " + get_normalised_num(group_num[
                                1:]) + ' '
            else:
                break
            group_count -= 1
            #Each group needs the print base (except for the rightmost group)
            if group_count > 1 and flag == 0:
                final_seq_int += base_constant[group_count] + " "

    #Converts the fractional part to word sequence
    if phrase_fract:
        final_seq_fract = 'point' + ' '
        for num in phrase_fract:
            final_seq_fract += num_constant[int(num)] + ' '
    #combine the fractional part and integer part
    return final_seq_int + final_seq_fract


#this function is used to convert date phrase to word sequences
#need a datetime format input and a bool value representing there is or not a year
def get_normalised_date(datetime, y):
    #used to record final result
    final_seq = ""
    ordinal_num_constant = {
        1: "first",
        2: "second",
        3: "third",
        4: "fourth",
        5: "fifth",
        6: "sixth",
        7: "seventh",
        8: "eighth",
        9: "ninth",
        10: "tenth",
        11: "eleventh",
        12: "twelfth",
        13: "thirteenth",
        14: "fourteenth",
        15: "fifteenth",
        16: "sixteenth",
        17: "seventeenth",
        18: "eighteenth",
        19: "nineteenth",
        20: "twentieth",
        21: "twenty first",
        22: "twenty second",
        23: "twenty third",
        24: "twenty fourth",
        25: "twenty fifth",
        26: "twenty sixth",
        27: "twenty seventh",
        28: "twenty eighth",
        29: "twenty ninth",
        30: "thirtieth",
        31: "thirty-first"
    }

    datetime_date = ""
    datetime_month = ""
    datetime_year = ""

    #Converts the date to word sequence
    datetime_date = datetime.strftime('%d')
    datetime_date = ordinal_num_constant[int(datetime_date)]
    #Converts the month to word sequence
    datetime_month = datetime.strftime('%B').lower()
    #Converts the year to word sequence, if there is a year value
    if y:
        datetime_year = datetime.strftime('%Y')
    #Remove any nonsensical zeroes at the left of the year section
    while datetime_year[0] == '0' and len(datetime_year) > 1:
        datetime_year = datetime_year[1:]
    #This is the case when the year formate is like 2000
    if len(datetime_year) == 4 and datetime_year[1:] == "000":
        datetime_year = get_normalised_num(datetime_year[0]) + ' ' + 'thousand'
    #This is the case when the year formate is like 2003
    elif len(datetime_year) == 4 and datetime_year[1:-1] == "00":
        datetime_year = get_normalised_num(datetime_year[
            0]) + ' ' + 'thousand' + ' ' + 'and' + ' ' + get_normalised_num(
                datetime_year[-1])
    #This is the case when the year formate is like 1903
    elif len(datetime_year) == 4 and datetime_year[
            -2] == "0" and datetime_year[-1] != "0":
        datetime_year = get_normalised_num(datetime_year[
            0:2]) + ' ' + 'o' + ' ' + get_normalised_num(datetime_year[-1])
    #This is the case when the year formate is like 1900
    elif len(datetime_year) == 4 and datetime_year[2:4] == "00":
        datetime_year = get_normalised_num(datetime_year[0:
                                                         2]) + ' ' + 'hundred'
    #This is the case when the year formate is like 1963
    elif len(datetime_year) == 4 and datetime_year[-2] != "0":
        datetime_year = get_normalised_num(datetime_year[
            0:2]) + ' ' + get_normalised_num(datetime_year[2:4])

    # elif len(group_num) == 3 and group_num[1:] == "00":
    #     datetime_year = get_normalised_num(datetime_year[0]) + ' ' + 'hundred'
    # elif len(datetime_year) == 3 and datetime_year[-2] == "0":
    #     datetime_year = get_normalised_num(datetime_year[
    #         0]) + ' ' + 'o' + ' ' + get_normalised_num(datetime_year[-1])
    # elif len(datetime_year) == 3 and datetime_year[-2] != "0":
    #     datetime_year = get_normalised_num(datetime_year[
    #         0]) + ' ' + get_normalised_num(datetime_year[1:3])
    # elif len(datetime_year) == 2:
    #     datetime_year = get_normalised_num(datetime_year[0:2])
    # elif len(datetime_year) == 1:
    #     datetime_year = get_normalised_num(datetime_year[0])

    #combine the date, month and year as result
    final_seq = 'the' + ' ' + datetime_date + ' ' + 'of' + ' ' + datetime_month + ' ' + datetime_year
    return final_seq


#This function is used word sequence as input, and then matched with cmudict get phonemes sequence as output
def get_phone_seq(phrase):
    punctuations = ''
    final_seq = ""
    phone_seq = []
    #load the cmudict
    cmudict_ = cmudict.dict()
    #let every parts of word sequence matched with cmudict
    tokens = phrase.split()
    for token in tokens:
        try:
            if token not in ',.?!':
                token = cmudict_[token]
        #If it is not found in cmudict, throw an exception and exit the program
        except KeyError as inst:
            print("*WARNING* KeyError: \"" + inst.args[0] +
                  "\" is not in the cmudict")
            exit(1)
        phone_seq.append(" ".join(token[0]))
    final_seq = " ".join(phone_seq)
    return final_seq


#This function is used to concatenate wav data to Audio.data based on path as input
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
        # concatenate the array to the class data attribute
        audio.data = np.concatenate((audio.data, array), axis=0)
        # Read the next chunk, ready for the next loop iteration
        raw = wf.readframes(audio.chunk)

    # Close the file
    wf.close()


#This function is used to insert a silence into audio.data
def insert_silence(audio, time):
    if (audio.nptype == np.int8):
        silence = '0'
    elif (audio.nptype == np.int16):
        silence = '00'
    elif (audio.nptype == np.int32):
        silence = '0000'
    elif (audio.nptype == np.int64):
        silence = '00000000'

    for i in xrange(0, int(time * audio.rate / audio.chunk)):
        silence_data = silence * audio.chunk
        array = np.fromstring(silence_data, dtype=audio.nptype)
        audio.data = np.concatenate((audio.data, array), axis=0)


#This function is used to convert a string into a sequence of letters
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
    return final_seq


if __name__ == "__main__":
    # Load the all phones' wavs file
    S = Synth(wav_folder=args.monophones)
    S.get_wavs(os.path.join(os.getcwd(), args.monophones))
    # out is the Audio object which will become your output
    # you need to modify out.data to produce the correct synthesis
    out = SA.Audio(rate=16000)

    #normalise the text (convert to lower case, remove punctuation(exclude ,.?!), etc.)
    #exclude removing the comma, period, question mark or exclamation mark(which we used to insert some silence)
    #and Left slash(which we used to fomat the date)
    normalised_seq = get_normalised_seq_norm(args.phrase[0])

    #if set the spell argument true, converting a string into a sequence of letters.
    if args.spell:
        normalised_seq = get_letter_seq(normalised_seq)

    #convert the word sequence to a phone sequence
    phone_seq = get_phone_seq(normalised_seq)
    phone_seq = re.sub(r'[0-9]', '', phone_seq)

    #concatenate the monophone wav files together in the right order to produce synthesised
    #audio.
    tokens = phone_seq.split()
    for token in tokens:
        token = token.encode("utf-8")
        if token in ',':
            insert_silence(out, 0.25)
        elif token in '.?!':
            insert_silence(out, 0.5)
        else:
            load_audio(out, path=S.phones[token])

    #Allow the user to set the volume argument (--volume, -v) to a value between 0.0 and 1.0.
    if args.volume:
        out.rescale(args.volume)

    #Play the result
    out.play()
    #Save the result
    out.save(args.outfile)

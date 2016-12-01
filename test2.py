import datetime


def get_normalised_num(phrase):
    final_seq_int = ""
    final_seq_fract = ""
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
    if type(eval(phrase)) == float:
        for n in range(len(phrase)):
            if phrase[n] == '.':
                phrase_fract = phrase[n + 1:len(phrase) - 1]
                break
            phrase_int += phrase[n]
        while phrase_fract[-1] == '0':
            phrase_fract = phrase_fract[:-1]
    elif type(eval(phrase)) == int:
        phrase_int = phrase

    while phrase_int[0] == '0' and len(phrase_int) > 1:
        phrase_int = phrase_int[1:]

    if int(phrase_int) < 20:
        final_seq_int = num_constant[int(phrase_int)] + ' '
        # return final_seq
    elif int(phrase_int) < 100 and int(phrase_int) >= 20:
        if phrase_int[1] == '0':
            final_seq_int = in_hundred_constant[int(phrase_int[0])] + ' '
        else:
            final_seq_int = in_hundred_constant[int(phrase_int[
                0])] + " " + num_constant[int(phrase_int[1])] + ' '
    else:
        phrase_int = format(int(phrase_int), ',')
        num_array = phrase_int.split(",")
        group_count = len(num_array) + 1
        for group_num in num_array:
            flag = 0
            if group_count > 1:
                if len(group_num) < 3:
                    final_seq_int += get_normalised_num(group_num) + ' '
                elif len(group_num) == 3 and group_num[0:] == "000":
                    flag = 1
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
            if group_count > 1 and flag == 0:
                final_seq_int += base_constant[group_count] + " "

    if phrase_fract:
        final_seq_fract = 'point' + ' '
        for num in phrase_fract:
            final_seq_fract += num_constant[int(num)] + ' '
    return final_seq_int + final_seq_fract


def get_normalised_date(datetime, y):
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

    datetime_date = datetime.strftime('%d')
    datetime_date = ordinal_num_constant[int(datetime_date)]
    datetime_month = datetime.strftime('%B').lower()

    if y:
        datetime_year = datetime.strftime('%Y')
    while datetime_year[0] == '0' and len(datetime_year) > 1:
        datetime_year = datetime_year[1:]
    if len(datetime_year) == 4 and datetime_year[1:] == "000":
        datetime_year = get_normalised_num(datetime_year[0]) + ' ' + 'thousand'
    elif len(datetime_year) == 4 and datetime_year[1:-1] == "00":
        datetime_year = get_normalised_num(datetime_year[
            0]) + ' ' + 'thousand' + ' ' + 'and' + ' ' + get_normalised_num(
                datetime_year[-1])

    elif len(datetime_year) == 4 and datetime_year[
            -2] == "0" and datetime_year[-1] != "0":
        datetime_year = get_normalised_num(datetime_year[
            0:2]) + ' ' + 'o' + ' ' + get_normalised_num(datetime_year[-1])
    elif len(datetime_year) == 4 and datetime_year[2:4] == "00":
        datetime_year = get_normalised_num(datetime_year[0:
                                                         2]) + ' ' + 'hundred'
    elif len(datetime_year) == 4 and datetime_year[-2] != "0":
        datetime_year = get_normalised_num(datetime_year[
            0:2]) + ' ' + get_normalised_num(datetime_year[2:4])

    elif len(group_num) == 3 and group_num[1:] == "00":
        datetime_year = get_normalised_num(datetime_year[0]) + ' ' + 'hundred'
    elif len(datetime_year) == 3 and datetime_year[-2] == "0":
        datetime_year = get_normalised_num(datetime_year[
            0]) + ' ' + 'o' + ' ' + get_normalised_num(datetime_year[-1])
    elif len(datetime_year) == 3 and datetime_year[-2] != "0":
        datetime_year = get_normalised_num(datetime_year[
            0]) + ' ' + get_normalised_num(datetime_year[1:3])
    elif len(datetime_year) == 2:
        datetime_year = get_normalised_num(datetime_year[0:2])
    elif len(datetime_year) == 1:
        datetime_year = get_normalised_num(datetime_year[0])

    final_seq = 'the' + ' ' + datetime_date + ' ' + 'of' + ' ' + datetime_month + ' ' + datetime_year
    return final_seq


if __name__ == '__main__':
    token = '29/02/2001'
    date_time = datetime.datetime.strptime(token, '%d/%m/%Y')
    print(get_normalised_date(date_time, True))

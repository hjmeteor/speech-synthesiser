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


def testget_normalised_num():
    print("0: " + get_normalised_num('0'))
    print("9: " + get_normalised_num('9'))
    print("33: " + get_normalised_num('33'))
    print("40: " + get_normalised_num('40'))
    print("100: " + get_normalised_num('100'))
    print("103: " + get_normalised_num('103'))
    print("123: " + get_normalised_num('123'))
    print("1,121,912  " + get_normalised_num('1121912'))
    print("211,121,900  " + get_normalised_num('211121900'))
    print("11,000,000  " + get_normalised_num('11000000'))
    print("1,111,121,912  " + get_normalised_num('111121912'))
    print("2,211,121,900  " + get_normalised_num('2211121900'))
    print("1,111,000,000  " + get_normalised_num('1111000000'))
    print("123.000023423423400000" + get_normalised_num(
        '123.000023423423400000'))
    print("00.000023423423400000" + get_normalised_num(
        '00.000023423423400000'))
    print("0432000123000" + get_normalised_num('0432000123000'))


if __name__ == '__main__':
    testget_normalised_num()

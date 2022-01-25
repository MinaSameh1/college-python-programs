"""
This is a program for Dr. Ahmed Negm on Vigenere getting key length
"""

import sys
import getopt
import textwrap
from collections import Counter
import numpy as np
import logging
import re

# Taken from Dr Ahmed Negm Book
freq_english_letters = {
    "a": 0.0817,
    "b": 0.0150,
    "c": 0.0278,
    "d": 0.0425,
    "e": 0.1270,
    "f": 0.0223,
    "g": 0.0202,
    "h": 0.0609,
    "i": 0.0697,
    "j": 0.0015,
    "k": 0.0077,
    "l": 0.0403,
    "m": 0.0241,
    "n": 0.0675,
    "o": 0.0751,
    "p": 0.0193,
    "q": 0.0010,
    "r": 0.0599,
    "s": 0.0633,
    "t": 0.0906,
    "u": 0.0276,
    "v": 0.0098,
    "w": 0.0236,
    "x": 0.0015,
    "y": 0.0197,
    "z": 0.0007
}


def factors(num):
    """ Gets all factors of number """
    return set(x for tup in ([i, num//i]
                             for i in range(1, int(num**0.5)+1)
                             if num % i == 0) for x in tup)


def get_percent_dict(dict_orig) -> dict:
    """ Function that takes a dict and returns the percentage
    sorted
        args:
            dict_orignal dictonary that we will get its percents
        returns:
            dict with their percent
    """
    sum_of_factors = sum(dict_orig.values())
    dict_percent = {}
    for key, value in dict_orig.items():
        pct = value * 100.0 / sum_of_factors
        dict_percent[key] = pct
    sortdict = sorted(dict_percent.items(), key=lambda x: x[1], reverse=True)
    return dict(sortdict)


def get_all_indicies(enc_words) -> list:
    list_of_indicies = []
    for i in range(3, 9):
        # Clear the found words to be used in the next iteration.
        found_words = []
        for j in range(len(enc_words) - i):
            # Dont add the same word
            if enc_words[j:j+i] not in found_words:
                # Search the list and get all alike words
                """
                #Removed cuz it didnt find correct elements,
                #repleaced with regex
                #find = indiciess(textwrap.wrap(enc_words,i), enc_words[j:j+i])
                """
                find = [index.start()
                        for index in re.finditer(enc_words[j:j+i], enc_words)]
                if len(find) > 1:  # if list not empty
                    list_of_indicies.append(list(map(lambda x: x * i, find)))
                    found_words.append(enc_words[j:j+i])
        logging.info("FoundWords:%s", found_words)
    return list_of_indicies


def get_possible_keys(enc_words) -> tuple:
    """ Function that finds the key length
        args: lst that we will use to find length
        returns: key length
    """
    # In order to search undisrupted in the list we must first
    # remove all spaces and other non letters
    remove = [",", ".", "2081", "1", "(", ")", " ", "'", ":"]
    enc_words = enc_words.strip()
    for item_to_be_removed in remove:
        enc_words = enc_words.replace(item_to_be_removed, "")

    list_of_indicies = get_all_indicies(enc_words)
    # Get factors of the numbers
    dict_of_factors: dict[int, int] = {}
    for list_of_same_word_index in list_of_indicies:
        # First get the difference between them
        diff = np.diff(list_of_same_word_index)[0]
        # Then get their factors
        for factor in factors(diff):
            if factor in dict_of_factors:
                dict_of_factors[factor] += 1
            else:
                dict_of_factors[factor] = 1
    # Remove 1 and 2 from factors
    dict_of_factors.pop(1)
    dict_of_factors.pop(2)
    # Get their percent ordered descending
    dict_of_factors_percent = get_percent_dict(dict_of_factors)
    # Split the msg according to the length
    key_letters = ""
    possible_keys = []
    print("LETTERS and their percentage")
    for key in dict_of_factors_percent.keys():
        # Skip 3
        if key == 3:
            continue
        # Skip numbers larger than 6 for now
        if key > 6:
            break
        # Then divide them into coloums
        enc_words_divided = textwrap.wrap(enc_words, key)
        for i in range(0, key):
            # at the end you will have some left overs just ignore them for now
            list_of_letters: list[str] = [x[i] if len(x) == key else x[i % len(x)]
                       for x in enc_words_divided]
            # Get the first letter and then consider it E, shift it by E
            # We use this function as a desencding sorter
            letters_percent: dict[str, int] = get_percent_dict(Counter(list_of_letters))
            print(letters_percent)
            most_used_letter = list(letters_percent.keys())[0]
            print(f"LETTER 0:{most_used_letter}")
            key_letters += chr(
                (
                    ((ord(most_used_letter) - ord('A')) -  # Get the letter
                     (ord('E') - ord('A')))  # then shift it
                    % 26) + ord('A')  # Then return it to ASCII Format
            )
        possible_keys.append(key_letters)
        key_letters = ""
    return tuple(possible_keys)


def decode_vigenere_without_key(enc_words):
    """ Function that decode vigenere,
    gets the key and its length
        args:lst that will be decoded
    """
    logging.debug("Enc Words:%s", enc_words)
    print(get_possible_keys(enc_words))


def main(argv) -> int:
    """ Main Function """
    # Take the file name from user
    infile = ""
    try:
        opts, args = getopt.getopt(argv, "hgo", [])
    except getopt.GetoptError:
        print(sys.argv[0] + " -g <FILE> -o <FILE>")
        sys.exit(2)
    for opt, arg in opts:
        print(arg)
        if opt == '-h':
            print(sys.argv[0] + " -g <FILE> -o <FILE>")
            sys.exit(0)
        elif opt == "-g":
            infile = args[0]
    if infile != "":
        with open(infile, "rt", encoding="utf-8") as file:
            coded = file.read()
            decode_vigenere_without_key(coded)
    else:
        return 2
    return 0


if __name__ == "__main__":
    logging.basicConfig(filename='vigenere.log', level=logging.DEBUG)
    logging.debug("Starting -------------------------------------------------")
    sys.exit({
        main(sys.argv[1:])
    })

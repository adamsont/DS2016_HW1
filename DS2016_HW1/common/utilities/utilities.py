__author__ = 'Taavi'

import logging

# My very own fancy diff calculator
# Can be used for deletion and addition as well


def find_changes(longer_text, shorter_text):
    # logging.debug("Curr: " + unicode(current_text))
    # logging.debug("Last: " + unicode(last_text))

    row = 1
    col = 0

    final_row = 0
    final_col = 0

    diff = ""
    diff_found = 0
    counter = 0

    for i in range(len(shorter_text)):
        col += 1
        counter += 1

        if longer_text[i] == '\n':
            row += 1
            col = 0

        if diff_found == 0:
            if longer_text[i] != shorter_text[i]:
                diff_found += 1
                diff += unicode(longer_text[i])
                final_col = col - 1
                final_row = row
        else:
            if longer_text[i] != shorter_text[i-diff_found]:
                diff_found += 1
                diff += unicode(longer_text[i])
            else:
                return diff, final_row, final_col

    final_col = col
    final_row = row

    for j in range(len(longer_text) - counter):
        if j+counter == len(longer_text) and longer_text[j+counter] == '\n':
            logging.debug("Breaking")
            break
        diff += longer_text[j+counter]

    return diff, final_row, final_col
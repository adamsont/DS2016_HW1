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
            break
        diff += longer_text[j+counter]

    return diff, final_row, final_col


def replace_text(current_str, replace_str, row_start, row_end):
    current_lines = current_str.split('\n')
    replace_lines = replace_str.split('\n')

    if row_end > len(current_lines):
        row_end = len(current_lines) - 1

    logging.info("cur_len:" +str(len(current_lines)) + " rep_len:" +str(len(replace_lines))+ " rs:" + str(row_start) + " re:" + str(row_end))
    line_count = row_end - row_start

    for i in range(line_count):
        logging.info("Replacing line: " + current_lines[row_start + i] + " with: " + replace_lines[i])
        current_lines[row_start + i - 1] = replace_lines[i]

    current_text = ''

    for line in current_lines:
        current_text += line + '\n'

    return current_text

def delete_text(current_str, row_start, row_end):
    current_lines = current_str.split('\n')

    if row_end > len(current_lines):
        row_end = len(current_lines) - 1

    logging.info("cur_len:" +str(len(current_lines)) + " rs:" + str(row_start) + " re:" + str(row_end))
    line_count = row_end - row_start

    hold_on_lines = []

    for i in range(len(current_lines)):
        if i - 1 >= row_start and i - 1 <= row_end:
            logging.info("Not adding line: " + current_lines[i - 1])
        else:
            hold_on_lines.append(current_lines[i - 1])

    current_text = ''

    for line in hold_on_lines:
        current_text += line + '\n'

    return current_text
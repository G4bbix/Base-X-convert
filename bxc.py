#!/usr/bin/env python3

# pylint: disable=R0912
# pylint: disable=R0915

"""
Script to convert from one numeric system to another
"""

import argparse
import sys

def parse_args():
  """
  Parse command line arguments
  """
  PARSER = argparse.ArgumentParser(description='Convert values with Base X to Base Y')
  PARSER.add_argument('INPUT_VALUE', metavar='INPUT_VALUE', type=str, help='Input Value')
  PARSER.add_argument('-B', dest='INPUT_BASE', type=int, help='Base of input Value')
  PARSER.add_argument('-b', dest='OUTPUT_BASE', type=int, help='Base of output Value')
  PARSER.add_argument('-O', dest='INPUT_ORDER', type=str, help='Order of input Alphabet '
                      'e.g. "0aA" results in 0..9a..zA..Z')
  PARSER.add_argument('-o', dest='OUTPUT_ORDER', type=str, help='Order of output '
                      'Alphabet e.g. "0aA" results in 0..9a..zA..Z')
  PARSER.add_argument('-A', dest='INPUT_ALPHABET', type=str, help='Alternative input '
                      'alphabet (Will override -O)')
  PARSER.add_argument('-a', dest='OUTPUT_ALPHABET', type=str, help='Altvernative output '
                      'alphabet (Will override -o)')
  PARSER.add_argument('-P', dest='INPUT_ALPHABET_APPEND', type=str, help='Append '
                      'characters to input alphabet')
  PARSER.add_argument('-p', dest='OUTPUT_ALPHABET_APPEND', type=str, help='Append '
                      'characters to output alphabet')
  PARSER.add_argument('-e', dest='EXCEL_MODE', action="store_true", help='Excel Mode '
                      '(Excel Columns indicies, where 26 is AA instead of BA)')
  return PARSER.parse_args()

def calculate_alphabet_from_order(ORDER):
  """
  Generates aplhabet from order
  """
  LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
  UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  ALPHABET = ""

  for CHAR in ORDER:
    if CHAR.islower():
      ALPHABET = "%s%s" % (ALPHABET, LOWERCASE)
    elif CHAR.isupper():
      ALPHABET = "%s%s" % (ALPHABET, UPPERCASE)
    else:
      try:
        int(CHAR)
        ALPHABET = "%s%s" % (ALPHABET, "0123456789")
      except TypeError:
        pass
  return ALPHABET

def search_for_duplicates(ALPHABET):
  """
  Returns true if the alphabet contains any duplicate
  Returns false if all character are unique in the alphabet
  """
  AMOUNT_CHAR_OCCURENCES = {}
  for CHAR in ALPHABET:
    if CHAR not in AMOUNT_CHAR_OCCURENCES:
      AMOUNT_CHAR_OCCURENCES[CHAR] = 1
    else:
      AMOUNT_CHAR_OCCURENCES[CHAR] += 1

  for VALUE in AMOUNT_CHAR_OCCURENCES.values():
    if VALUE > 1:
      return False

  return True

def bx_2_dec(VALUE, ALPHABET, BASE):
  """
  Converts from base X to decimal
  """
  POSITION = 0
  TOTAL_DEC_VALUE = 0

  # Loop over string reversed
  for PLACE in VALUE[::-1]:
    TOTAL_DEC_VALUE += pow(BASE, POSITION) * ALPHABET.index(PLACE)
    POSITION += 1

  return TOTAL_DEC_VALUE

def dec_2_bx(VALUE, ALPHABET, BASE, EXCEL_MODE):
  """
  Convert from decimal to base X
  """
  if VALUE == 0:
    return ALPHABET[0]

  AMOUNT_PLACES = 0
  while pow(BASE, AMOUNT_PLACES) <= VALUE:
    AMOUNT_PLACES += 1

  RETURN_VALUE = ""
  for i in range(AMOUNT_PLACES - 1, -1, -1):
    for j in range(BASE, -1, -1):
      if pow(BASE, i) * j <= VALUE:
        if EXCEL_MODE and i == AMOUNT_PLACES - 1 and AMOUNT_PLACES > 1:
          RETURN_VALUE = f"{RETURN_VALUE}{ALPHABET[j - 1]}"
        else:
          RETURN_VALUE = f"{RETURN_VALUE}{ALPHABET[j]}"
        VALUE = VALUE - pow(BASE, i) * j
        break

  return RETURN_VALUE

def main():
  """
  Main entrypoint
  """
  # Default arguments
  INPUT_BASE = 10
  OUTPUT_BASE = 10
  INPUT_ORDER = None
  OUTPUT_ORDER = None
  INPUT_ALPHABET = None
  OUTPUT_ALPHABET = None
  INPUT_ALPHABET_APPEND = None
  OUTPUT_ALPHABET_APPEND = None
  EXCEL_MODE = False

  ARGS = parse_args()
  INPUT_VALUE = ARGS.INPUT_VALUE
  if ARGS.INPUT_BASE:
    INPUT_BASE = ARGS.INPUT_BASE
  if ARGS.OUTPUT_BASE:
    OUTPUT_BASE = ARGS.OUTPUT_BASE
  INPUT_ORDER = ARGS.INPUT_ORDER
  OUTPUT_ORDER = ARGS.OUTPUT_ORDER
  INPUT_ALPHABET = ARGS.INPUT_ALPHABET
  OUTPUT_ALPHABET = ARGS.OUTPUT_ALPHABET
  INPUT_ALPHABET_APPEND = ARGS.INPUT_ALPHABET_APPEND
  OUTPUT_ALPHABET_APPEND = ARGS.OUTPUT_ALPHABET_APPEND
  EXCEL_MODE = ARGS.EXCEL_MODE

  # Generate Alphabets
  if INPUT_ALPHABET is None:
    if INPUT_ORDER is not None:
      INPUT_ALPHABET = calculate_alphabet_from_order(INPUT_ORDER)
    else:
      INPUT_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"

  if OUTPUT_ALPHABET is None:
    if OUTPUT_ORDER is not None:
      OUTPUT_ALPHABET = calculate_alphabet_from_order(OUTPUT_ORDER)
    else:
      OUTPUT_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"

  if INPUT_ALPHABET_APPEND is not None:
    INPUT_ALPHABET = "%s%s" %(INPUT_ALPHABET, INPUT_ALPHABET_APPEND)

  if OUTPUT_ALPHABET_APPEND is not None:
    OUTPUT_ALPHABET = "%s%s" %(OUTPUT_ALPHABET, OUTPUT_ALPHABET_APPEND)

  # Check if there are any duplicates in Alphabets
  DUPLICATES = False
  if not search_for_duplicates(INPUT_ALPHABET):
    print("ERROR: Input alphabet contains duplicates, please check parameters.")
    DUPLICATES = True
  if not search_for_duplicates(OUTPUT_ALPHABET):
    print("ERROR: Output alphabet contains duplicates, please check parameters.")
    DUPLICATES = True
  if DUPLICATES:
    sys.exit(1)

  # Check if the alphabet is shorter than the base
  ALPHABET_TOO_SHORT = False
  if len(INPUT_ALPHABET) < INPUT_BASE:
    print("ERROR: Input alphabet is shorter than base. Use -P to append additonal chars")
    ALPHABET_TOO_SHORT = True
  if len(OUTPUT_ALPHABET) < OUTPUT_BASE:
    print("ERROR: Output alphabet is shorter than base. Use -p to append additonal chars")
    ALPHABET_TOO_SHORT = True
  if ALPHABET_TOO_SHORT:
    sys.exit(2)

  # Check if input contains chars that are not part of the alphabet
  for CHAR in INPUT_VALUE:
    if CHAR not in INPUT_ALPHABET:
      print("ERROR: The character \"%s\" is not part of the input alphabet" % CHAR)
      sys.exit(3)

  # Cut off excessive places in alphabets
  INPUT_ALPHABET = INPUT_ALPHABET[0:INPUT_BASE]
  OUTPUT_ALPHABET = OUTPUT_ALPHABET[0:OUTPUT_BASE]

  INPUT_DEC_VALUE = bx_2_dec(INPUT_VALUE, INPUT_ALPHABET, INPUT_BASE)
  print(dec_2_bx(INPUT_DEC_VALUE, OUTPUT_ALPHABET, OUTPUT_BASE, EXCEL_MODE))

if __name__ == "__main__":
  main()

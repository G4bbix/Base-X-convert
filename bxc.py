#/usr/bin/env python3

import argparse
import sys

def parse_args():
  """
  Parse command line arguments
  """
  parser = argparse.ArgumentParser(description='Convert values with Base X to Base Y')
  parser.add_argument('INPUT_VALUE', metavar='INPUT_VALUE', type=str, help='Input Value')
  parser.add_argument('-B', dest='INPUT_BASE', type=int, help='Base of input Value')
  parser.add_argument('-b', dest='OUTPUT_BASE', type=int, help='Base of output Value')
  parser.add_argument('-O', dest='INPUT_ORDER', type=str, help='Order of input Alphabet e.g. "0aA" results in 0..9a..zA..Z')
  parser.add_argument('-o', dest='OUTPUT_ORDER', type=str, help='Order of output Alphabet e.g. "0aA" results in 0..9a..zA..Z')
  parser.add_argument('-A', dest='INPUT_ALPHABET', type=str, help='Alternative input alphabet (Will override -O)')
  parser.add_argument('-a', dest='OUTPUT_ALPHABET', type=str, help='Altvernative output alphabet (Will override -o)')
  parser.add_argument('-P', dest='INPUT_ALPHABET_APPEND', type=str, help='Append characters to input alphabet')
  parser.add_argument('-p', dest='OUTPUT_ALPHABET_APPEND', type=str, help='Append characters to output alphabet')
  return parser.parse_args()

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
    if (CHAR not in AMOUNT_CHAR_OCCURENCES):
      AMOUNT_CHAR_OCCURENCES[CHAR] = 1
    else:
      AMOUNT_CHAR_OCCURENCES[CHAR] += 1

  for KEY, VALUE in AMOUNT_CHAR_OCCURENCES.items(): # pylint: disable=unused-variable
    if (VALUE > 1):
      return False

  return True

def bx_2_dec(VALUE, ALPHABET, BASE):
  """
  Converts from base X to decimal
  """
  POSITION=0
  TOTAL_DEC_VALUE=0

  # Loop over string reversed
  for PLACE in VALUE[::-1]:
    TOTAL_DEC_VALUE += pow(BASE, POSITION) * ALPHABET.index(PLACE)
    POSITION += 1

  return TOTAL_DEC_VALUE

def dec_2_bx(VALUE, ALPHABET, BASE):
  """
  Convert from decimal to base X
  """
  AMOUNT_PLACES = 0
  while pow(BASE, AMOUNT_PLACES) <= VALUE:
    AMOUNT_PLACES += 1

  RETURN_VALUE = ""
  for i in range(AMOUNT_PLACES - 1, -1, -1):
    for j in range(BASE, -1, -1):
      if pow(BASE, i) * j <= VALUE:
        RETURN_VALUE = "%s%s" % (RETURN_VALUE, ALPHABET[j])
        VALUE = VALUE - pow(BASE, i) * j
        break

  return RETURN_VALUE

def main():
  # Arguments
  INPUT_BASE = 10
  OUTPUT_BASE = 10
  INPUT_ORDER = None
  OUTPUT_ORDER = None
  INPUT_ALPHABET = None
  OUTPUT_ALPHABET = None
  INPUT_ALPHABET_APPEND = None
  OUTPUT_ALPHABET_APPEND = None

  args = parse_args()
  INPUT_VALUE = args.INPUT_VALUE
  if args.INPUT_BASE:
    INPUT_BASE = args.INPUT_BASE
  if args.OUTPUT_BASE:
    OUTPUT_BASE = args.OUTPUT_BASE
  INPUT_ORDER = args.INPUT_ORDER
  OUTPUT_ORDER = args.OUTPUT_ORDER
  INPUT_ALPHABET = args.INPUT_ALPHABET
  OUTPUT_ALPHABET = args.OUTPUT_ALPHABET
  INPUT_ALPHABET_APPEND = args.INPUT_ALPHABET_APPEND
  OUTPUT_ALPHABET_APPEND = args.OUTPUT_ALPHABET_APPEND

  # Generate Alphabets
  if INPUT_ALPHABET is None:
    if INPUT_ORDER is not None:
      INPUT_ALPHABET = calculate_alphabet_from_order(INPUT_ORDER)
    else:
      INPUT_ALPHABET = "0123456789"

  if OUTPUT_ALPHABET is None:
    if OUTPUT_ORDER is not None:
      OUTPUT_ALPHABET = calculate_alphabet_from_order(OUTPUT_ORDER)
    else:
      OUTPUT_ALPHABET = "0123456789"

  if INPUT_ALPHABET_APPEND is not None:
    INPUT_ALPHABET = "%s%s" %(INPUT_ALPHABET, INPUT_ALPHABET_APPEND)

  if OUTPUT_ALPHABET_APPEND is not None:
    OUTPUT_ALPHABET = "%s%s" %(OUTPUT_ALPHABET, OUTPUT_ALPHABET_APPEND)

  # Check if there are any duplicates in Alphabets
  DUPLICATES = False
  if not search_for_duplicates(INPUT_ALPHABET):
    print("ERROR: Input alphabet contains duplicates, please check parameters.")
    DUPLICATES=True
  if not search_for_duplicates(OUTPUT_ALPHABET):
    print("ERROR: Output alphabet contains duplicates, please check parameters.")
    DUPLICATES=True
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
  print(dec_2_bx(INPUT_DEC_VALUE, OUTPUT_ALPHABET, OUTPUT_BASE))

if __name__ == "__main__":
  main()
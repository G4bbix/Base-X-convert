# About
Base-X-convert is a Script that converts a value from one numeric system to another.
The definition of the numeric system used is very flexible. The definition, further called alphabet can be definied as any String. If nothing is specified the decimal system is used.
If there are more characters in the alphabet than the base any excessive characters will be cut off.

## Command line parameters
usage: bxc.py [-h] [-B INPUT_BASE] [-b OUTPUT_BASE] [-O INPUT_ORDER]
              [-o OUTPUT_ORDER] [-A INPUT_ALPHABET] [-a OUTPUT_ALPHABET]
              [-P INPUT_ALPHABET_APPEND] [-p OUTPUT_ALPHABET_APPEND] [-e]
              INPUT_VALUE

### Explanation

-B, -b
The base of the numeric system of the input- and output value.

-O, -o
The order of numbers, lowercase- and uppercase charaters in the alphabet.
e.G. "-o '1aA'" will set the order of the alphabet to [0-9][a-z][A-Z].
Any number or letter can be used.

-A, -a
Defines an alternative Alphabet. This option will override the -O and -o paramters.

-P, -p
Appends characters to the alphabet. Any special chars may be used.

-e
Excel Mode (Excel Columns indicies, where 26 is AA instead of BA)

# Examples

Hexadecimal to decimal

./bxc.py -B 16 -b 10 ff

255

Binary to decimal

./bxc.py -B 2 -b 10 100001

33

Base62 to decimal

./bxc.py -B 62 -b 10 -O 1aA z192AF

32081580369

Are you mad?

./bxc.py -B 62 -b 10 -O fF1 -a ',.-;:_+?*"' 1sfd3

?*?:__.?;

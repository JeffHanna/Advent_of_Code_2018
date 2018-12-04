#-*- coding: utf-8 -*-
"""
--- Day 2: Inventory Management System ---
You stop falling through time, catch your breath, and check the screen on the device. "Destination reached. Current Year: 1518. Current Location: North Pole Utility Closet 83N10." You made it! Now, to find those anomalies.

Outside the utility closet, you hear footsteps and a voice. "...I'm not sure either. But now that so many people have chimneys, maybe he could sneak in that way?" Another voice responds, "Actually, we've been working on a new kind of suit that would let him fit through tight spaces like that. But, I heard that a few days ago, they lost the prototype fabric, the design plans, everything! Nobody on the team can even seem to remember important details of the project!"

"Wouldn't they have had enough fabric to fill several boxes in the warehouse? They'd be stored together, so the box IDs should be similar. Too bad it would take forever to search the warehouse for two similar box IDs..." They walk too far away to hear any more.

Late at night, you sneak to the warehouse - who knows what kinds of paradoxes you could cause if you were discovered - and use your fancy wrist device to quickly scan every box and produce a list of the likely candidates (your puzzle input).

To make sure you didn't miss any, you scan the likely candidate boxes again, counting the number that have an ID containing exactly two of any letter and then separately counting those with exactly three of any letter. You can multiply those two counts together to get a rudimentary checksum and compare it to what your device predicts.

For example, if you see the following box IDs:

abcdef contains no letters that appear exactly two or three times.
bababc contains two a and three b, so it counts for both.
abbcde contains two b, but no letter appears exactly three times.
abcccd contains three c, but no letter appears exactly two times.
aabcdd contains two a and two d, but it only counts once.
abcdee contains two e.
ababab contains three a and three b, but it only counts once.
Of these box IDs, four of them contain a letter which appears exactly twice, and three of them contain a letter which appears exactly three times. Multiplying these together produces a checksum of 4 * 3 = 12.

What is the checksum for your list of box IDs?

--- Part Two ---
Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
"""

from collections import Counter
from difflib import SequenceMatcher
from typing import Sequence


def calculate_checksum( input_lines: Sequence[ str ] ) -> int:
	"""
	[summary]

	Arguments:
		input_lines {list} -- list of box ids

	Returns:
		int -- The calcuated checksum from the list of box ids.
	"""

	twos : int = 0
	threes : int = 0

	for il in input_lines:
		counter = Counter( il )
		if 2 in counter.values( ):
			twos += 1
		if 3 in counter.values( ):
			threes += 1

	return twos * threes


def get_matching_box_ids( input_lines: Sequence[ str ] ) -> str:
	"""
	Finds the two box IDs with the highest ratio of identical characters and returns the characters common to both of those box ids.

	Arguments:
		input_lines {list} -- list of box ids

	Returns:
		str -- characters common to the two box ids with the highest comparison ratio.
	"""

	highest_ratio = 0.00
	highest_lines = ( 0, 0 )

	for i, il in enumerate( input_lines ):
		for x in range( i+1, len( input_lines ) ):
			m = SequenceMatcher( None, il, input_lines[ x ] )
			if m.ratio( ) > highest_ratio:
				highest_ratio = m.ratio( )
				highest_lines = ( i, x )

	a = set( input_lines[ highest_lines[ 0 ] ].rstrip( ) )
	b = set( input_lines[ highest_lines[ -1 ] ].rstrip( ) )
	c = set.intersection( a, b )

	return ''.join( list( c ) )


if __name__ == '__main__':
	with open( r'day_02_input.txt', 'r' ) as f:
		input_lines = f.readlines( )

	checksum = calculate_checksum( input_lines )
	print( 'CHECKSUM: ', checksum )

	box_id_characters = get_matching_box_ids( input_lines )
	print( 'COMMON BOX ID CHARACTERS: ', box_id_characters )
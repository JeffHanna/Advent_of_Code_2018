#-*- coding: utf-8 -*-
"""
--- Day 3: No Matter How You Slice It ---
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of
the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with
edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and
4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the
diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example,
consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?

--- Part Two ---
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other  If you can somehow
draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
"""

from collections import defaultdict
from itertools import product
import re
from typing import List, Tuple


def _get_square_inches_overlap( claims : List[ tuple ] ) -> Tuple[ int, int ]:
	"""
	Finds the area of fabric overlap from all of the elves' fabric claims when laid out on a 1000 x 1000 inch piece of fabric.
	Also returns the claim id of the only claim that does not overlap any other

	**Arguments:**

		:``claims``: `list` A list of tuples ( id, x_coord, y_coord, width, height )

	**Keword Arguments:**

		None

	**Returns:**

		:``int``: The area of fabric overlap in square inches.
		:``str``: The id of the only claim that does not overlap any other
	"""

	overlaps = { }
	overlap_coords = defaultdict( list )
	for id, x_coord, y_coord, width, height in claims:
		overlaps[ id ] = set( )

		for x, y in product( range( x_coord, x_coord + width ), range( y_coord, y_coord + height ) ):
			numbers = overlap_coords.get( ( x, y ), [ ] )
			for n in numbers:
				overlaps[ n ].add( id )
				overlaps[ id ].add( n )

			overlap_coords[ ( x, y ) ].append( id )

	square_inches_overlap = len( [ z for z in overlap_coords if len( overlap_coords[ z ] ) > 1 ] )
	id_of_claim_with_no_overlap = [ z for z in overlaps if len( overlaps[ z ] ) == 0 ][ 0 ]
	return square_inches_overlap, id_of_claim_with_no_overlap


def _claims_parser( puzzle_input_filename : str ) -> List[ tuple ]:
	"""
	Returns a list of tuples ( id, x_coord, y_coord, width, height ) after parsing the input file.
	Each line of the input files is formatted as:
		#<id> @ <x_coord, y_coord: <width>x<height>

	**Arguments:**

		:``puzzle_input_filename``: `str`

	**Keword Arguments:**

		None

	**Returns:**

		:``list``:  a list of tuples ( id, x_coord, y_coord, width, height )
	"""

	re_sub_01 = r"[# ]"
	re_sub_02 = r"[@:x]"

	claims = [ ]


	with open( puzzle_input_filename, 'r' ) as f:
		for line in f.readlines( ):
			line = re.sub( re_sub_01, "", line )
			line_parts = re.sub( re_sub_02, ",", line ).split( ',' )
			claims.append( ( line_parts[ 0 ], int( line_parts[ 1 ] ), int( line_parts[ 2 ] ), int( line_parts[ 3 ] ), int( line_parts[ -1 ] ) ) )


	return claims


if __name__ == '__main__':
	claims = _claims_parser( r'day_03_input.txt' )
	square_inches_overlap, claim_id = _get_square_inches_overlap( claims )
	print( 'The total area of fabric overlap is: ', str( square_inches_overlap ) )
	print( 'The only claim with no overlap is claim #: ', str( claim_id ) )

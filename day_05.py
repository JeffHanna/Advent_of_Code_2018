# -*- coding: utf-8 -*-
"""
--- Day 5: Alchemical Reduction ---
You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are still struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better. You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymermers (one of which is available as your puzzle input).

The polymermer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymermer contains 10 units.

How many units remain after fully reacting the polymermer you scanned? (Note: in this puzzle and others, the input is large; if you copy/paste your input, make sure you get the whole thing.)

--- Part Two ---
Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.
In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
"""

import copy
import string
from typing import Iterator


def _react( polymer : str ) -> str:
	"""
	Reacts the polymer by repeatedly looping over it and removing 'aA', 'bB', 'Cc', etc.. pairs until none exist

	Arguments:
		polymer {str} -- The original string representing the polymer

	Returns:
		str -- The new string representing the reacted polymer
	"""

	pairs = [ ''.join( x ) for x in zip( string.ascii_lowercase, string.ascii_uppercase ) ]
	pairs.extend( p[ :: -1 ] for p in pairs[ : ] )

	while any( p in polymer for p in pairs ):
		for p in pairs:
			polymer = polymer.replace( p, '' )

	return polymer


def _find_best_reaction( polymer : str ) -> int:
	"""
	Removes all instances of a given letter and then reacts the polymer. This is done for all letters to find the shortest resultant polymer.

	Arguments:
		polymer {str} -- The original string representing the polymer

	Returns:
		int -- The length of the shortest, and therefor the most fully reacted, polymer
	"""

	counts = [ ]
	for l, u in zip( string.ascii_lowercase, string.ascii_uppercase ):
		new_polymer = polymer.replace( u, '' ).replace( l, '' )
		counts.append( len( _react( new_polymer ) ) )

	return min( counts )


if __name__ == '__main__':
	with open( 'day_05_input.txt', 'r' ) as f:
		polymer = f.read( )

	collapsed_polymer = _react( polymer )
	print( 'The length of the fully reacted polymer is: ', len( collapsed_polymer ) )

	shortest_polymer_count = _find_best_reaction( polymer )
	print( 'The length of the best reacted polymer is: ', shortest_polymer_count )
#-*- coding: utf-8 -*-
"""
Day 01 solutions for Advent of Code 2018
"""

import itertools

def run_part_1( steps: list ):
	"""
	Sums the provided list of frequency change steps
	
	Arguments:
		steps {list} -- Frequency tuning steps.
	"""

	print( 'FINAL FREQUENCY: ', sum( steps ) )


def run_part_2( steps: list, starting_frequency: int ):
	"""
	Finds the first repeated frequency encountered when stepping through
	the list of provided frequency changes. The list may be cycled over more than
	once before a duplicae is found.
	
	Arguments:
		steps {list} -- Frequency tuning steps.
		starting_frequency {int} -- The starting fequency
	"""

	tuned_frequencies = set( [ starting_frequency ] )
	current_frequency = starting_frequency

	for step in itertools.cycle( steps ):
		current_frequency += step
		if current_frequency in tuned_frequencies:
			print( 'DUPLICATE FREQUENCY: ', current_frequency )
			return

		tuned_frequencies.add( current_frequency )


if __name__ == '__main__':
	steps = [ int( x ) for x in open( 'day_01_input.txt' ).readlines( ) ]
	run_part_1( steps )
	run_part_2( steps, 0 )	

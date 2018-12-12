# -+- coding: utf-8 -*=
"""
--- Day 11: Chronal Charge ---
You watch the Elves and their sleigh fade into the distance as they head toward the North Pole.

Actually, you're the one fading. The falling sensation returns.

The low fuel warning light is illuminated on your wrist-mounted device. Tapping it once causes it to project a hologram of the situation: a 300x300 grid of fuel cells and their current power levels, some negative. You're not sure what negative power means in the context of time travel, but it can't be good.

Each fuel cell has a coordinate ranging from 1 to 300 in both the X (horizontal) and Y (vertical) direction. In X,Y notation, the top-left cell is 1,1, and the top-right cell is 300,1.

The interface lets you select any 3x3 square of fuel cells. To increase your chances of getting to your destination, you decide to choose the 3x3 square with the largest total power.

The power level in a given fuel cell can be found through the following process:

Find the fuel cell's rack ID, which is its X coordinate plus 10.
Begin with a power level of the rack ID times the Y coordinate.
Increase the power level by the value of the grid serial number (your puzzle input).
Set the power level to itself multiplied by the rack ID.
Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
Subtract 5 from the power level.
For example, to find the power level of the fuel cell at 3,5 in a grid with serial number 8:

The rack ID is 3 + 10 = 13.
The power level starts at 13 * 5 = 65.
Adding the serial number produces 65 + 8 = 73.
Multiplying by the rack ID produces 73 * 13 = 949.
The hundreds digit of 949 is 9.
Subtracting 5 produces 9 - 5 = 4.
So, the power level of this fuel cell is 4.

Here are some more example power levels:

Fuel cell at  122,79, grid serial number 57: power level -5.
Fuel cell at 217,196, grid serial number 39: power level  0.
Fuel cell at 101,153, grid serial number 71: power level  4.
Your goal is to find the 3x3 square which has the largest total power. The square must be entirely within the 300x300 grid. Identify this square using the X,Y coordinate of its top-left fuel cell. For example:

For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29); these fuel cells appear in the middle of this 5x5 region:

-2  -4   4   4   4
-4   4   4   4  -5
 4   3   3   4  -4
 1   1   2   4  -3
-1   0   2  -5  -2
For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30); they are in the middle of this region:

-3   4   2   2   2
-4   4   3   3   4
-5   3   3   4  -4
 4   3   3   4  -3
 3   3   3  -5  -1
What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?

Your puzzle input is 7315.

--- Part Two ---
You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power. Identify this square by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16.
For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.
What is the X,Y,size identifier of the square with the largest total power?

Your puzzle input is still 7315.
"""

import itertools
import numpy

_SERIAL_NUMBER = 7315


def _calculate_cell_power( x: int, y: int ) -> int:
	"""
	Function used by numpy.fromfunction( ) to build the full 300 x 300 fuel cell array with power levels.

	Arguments:
		x {int} -- The x coordinate in the fuel cell array.
		y {int} -- The y coordinate in the fuel cell array.

	Returns:
		int -- The fuel cell power level.
	"""

	rack_id = x + 1 + 10
	return ( ( ( ( ( rack_id * ( y + 1 ) ) + _SERIAL_NUMBER ) * rack_id ) // 100 ) % 10 ) - 5


def _get_block_power( fuel_cells: list, coord_x: int, coord_y: int, square_dim: int ) -> float:
	"""
	Determines the power level of a 3 x 3 block within the fuel cell array.
	X and Y coordinates into the fuel cells array are provided. A smaller 3 x 3 array
	is extracted from the fuel cells array and numpy.cumsum( ) is used to calculate the
	sum of all values in that new smaller 2D array.

	Arguments:
		fuel_cells {list} -- The 300 x 300 numpy array of fuel cell power levels.
		coord_x {int} -- The starting x coordinate in the fuel cells array.
		coord_y {int} -- The starting y coordinate in the fuel cells array.
		square_dim {1} -- The value for the width and height of the power block.

	Returns:
		float -- The total power of all 9 cells in the block.
	"""

	block = numpy.zeros( ( square_dim, square_dim ) )

	try:
		for y, x in itertools.product( range( square_dim ), range( square_dim ) ):
			block[ x ][ y ] =  fuel_cells[ coord_x + x ][ coord_y + y ]

		return numpy.cumsum( block )[ -1 ]
	except IndexError:
		return -999


def _find_strongest_cell_block( fuel_cells: list, variable_size = False ) -> tuple:
	"""
	Finds the X, Y upper left ( 1-based ) coordinates of the 3 x 3 block within the fuel cells array
	that has the most power remaining.

	Arguments:
		fuel_cells {list} -- A 300 x 300 numpy array of fuel cell power levels.

	Returns:
		tuple -- The 1-based X and Y coordinates of the upper left cell of the 3 x 3 block with the highest power levels.
	"""

	highest_power_level = -999
	location = ( )
	largest_square_dim = 0

	size_range = range( 3, 4 ) if not variable_size else range( 1, 301 )

	for square_dim in size_range:
		for y, x in itertools.product( range( 298 ), range( 298 ) ):
			power = _get_block_power( fuel_cells, x, y, square_dim )
			if power > highest_power_level:
				highest_power_level = power
				location = ( x + 1, y + 1 )
				largest_square_dim = square_dim

	return ( *location, largest_square_dim )


if __name__ == '__main__':
	fuel_cells = numpy.fromfunction( _calculate_cell_power, ( 300, 300 ) )
	x, y, _sd = _find_strongest_cell_block( fuel_cells )
	print( 'The location of the strongest fuel cell block is: {0}, {1}.'.format( x, y ) )

	x, y, sd = _find_strongest_cell_block( fuel_cells, variable_size = True )
	#242,13,9
	print( 'The location and size of the strongest fuel cell block is: {0},{1},{2}'.format( x, y, sd ) )
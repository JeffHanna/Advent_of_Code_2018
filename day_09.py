# -+- coding utf-8 -*-
"""
--- Day 9: Marble Mania ---
You talk to the Elves while you wait for your navigation system to initialize. To pass the time, they introduce you to their favorite marble game.

The Elves play this game by taking turns arranging the marbles in a circle according to very particular rules. The marbles are numbered starting with 0 and increasing by 1 until every marble has a number.

First, the marble numbered 0 is placed in the circle. At this point, while it contains only a single marble, it is still a circle: the marble is both clockwise from itself and counter-clockwise from itself. This marble is designated the current marble.

Then, each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles that are 1 and 2 marbles clockwise of the current marble. (When the circle is large enough, this means that there is one marble between the marble that was just placed and the current marble.) The marble that was just placed then becomes the current marble.

However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely different happens. First, the current player keeps the marble they would have placed, adding it to their score. In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle and also added to the current player's score. The marble located immediately clockwise of the marble that was removed becomes the new current marble.

For example, suppose there are 9 players. After the marble with value 0 is placed in the middle, each player (shown in square brackets) takes a turn. The result of each of those turns would produce circles of marbles like this, where clockwise is to the right and the resulting current marble is in parentheses:

[-] (0)
[1]  0 (1)
[2]  0 (2) 1
[3]  0  2  1 (3)
[4]  0 (4) 2  1  3
[5]  0  4  2 (5) 1  3
[6]  0  4  2  5  1 (6) 3
[7]  0  4  2  5  1  6  3 (7)
[8]  0 (8) 4  2  5  1  6  3  7
[9]  0  8  4 (9) 2  5  1  6  3  7
[1]  0  8  4  9  2(10) 5  1  6  3  7
[2]  0  8  4  9  2 10  5(11) 1  6  3  7
[3]  0  8  4  9  2 10  5 11  1(12) 6  3  7
[4]  0  8  4  9  2 10  5 11  1 12  6(13) 3  7
[5]  0  8  4  9  2 10  5 11  1 12  6 13  3(14) 7
[6]  0  8  4  9  2 10  5 11  1 12  6 13  3 14  7(15)
[7]  0(16) 8  4  9  2 10  5 11  1 12  6 13  3 14  7 15
[8]  0 16  8(17) 4  9  2 10  5 11  1 12  6 13  3 14  7 15
[9]  0 16  8 17  4(18) 9  2 10  5 11  1 12  6 13  3 14  7 15
[1]  0 16  8 17  4 18  9(19) 2 10  5 11  1 12  6 13  3 14  7 15
[2]  0 16  8 17  4 18  9 19  2(20)10  5 11  1 12  6 13  3 14  7 15
[3]  0 16  8 17  4 18  9 19  2 20 10(21) 5 11  1 12  6 13  3 14  7 15
[4]  0 16  8 17  4 18  9 19  2 20 10 21  5(22)11  1 12  6 13  3 14  7 15

# MOVE WITHOUT MODULUS 23 RULE
[5]  0 16  8 17  4 18  9 19  2 20 10 21  5 22 11(23) 1 12  6 13  3 14  7 15
However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely different happens. First, the current player keeps the marble they would have placed, adding it to their score. In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle and also added to the current player's score. The marble located immediately clockwise of the marble that was removed becomes the new current marble.

[5]  0 16  8 17  4 18(19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15
[6]  0 16  8 17  4 18 19  2(24)20 10 21  5 22 11  1 12  6 13  3 14  7 15
[7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15

Here are a few more examples:

10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
What is the winning Elf's score?

--- Part Two ---
Amused by the speed of your answer, the Elves are curious:

What would the new winning Elf's score be if the number of the last marble were 100 times larger?
"""

from collections import defaultdict
from itertools import cycle
import re


def _parse( filepath: str ) -> tuple:
	with open( filepath, 'r' ) as f:
		line = f.readline( )
		return tuple( [ int( x ) for x in re.findall( r'\d+', line ) ] )


class Game( ):
	"""
	Instance an Elf marble game. The provided player_count and final_marble_value are used to set the state of the game and establish
	the end-game trigger. Once the game is simulated the winning elf and their score are presented.
	"""

	def __init__( self, player_count: int, final_marble_value: int, part_2_scale : int = False ):
		self._player_count = player_count
		self._players = defaultdict( list )
		self._final_marble_value = final_marble_value if not part_2_scale else final_marble_value * 100
		self._current_marble_idx = 0
		self._marble = 0
		self._circle = [ self._marble ]


	def _calculate_score( self ):
		"""
		Sums the totals of all of the elves' marbles. The winner is the elf with the highest score.
		"""

		high_score = 0
		winning_player = 0

		for player, marbles in self._players.items( ):
			score = sum( marbles )
			if score > high_score:
				high_score = score
				winning_player = player

		print( 'The winning elf is: {0} with a score of: {1}'.format( winning_player, high_score ) )


	def _turn( self, player: int ):
		"""
		Simulates a game turn of the elf marble game. The turn rules can be found in the module docstring.

		Arguments:
			player {int} -- The current player
		"""

		self._marble += 1

		if self._marble % 23 == 0:
			extra_score_marble_idx = ( self._current_marble_idx - 7 ) % len( self._circle )
			self._current_marble_idx = ( extra_score_marble_idx )
			extra_score_marble = self._circle.pop( extra_score_marble_idx )
			self._players[ player ].extend( [ self._marble, extra_score_marble ] )
		else:
			insert_location = ( self._current_marble_idx + 1 ) % len( self._circle ) + 1
			self._circle.insert( insert_location, self._marble )
			self._current_marble_idx = insert_location

		if self._marble == self._final_marble_value:
			self._calculate_score( )


	def play( self ):
		"""
		Public method to start the game once the initial state is established.
		"""

		for p in cycle( range( 1, self._player_count + 1 ) ):
			self._turn( p )



if __name__ == '__main__':
	player_count, final_marble_value = _parse( r'day_09_input.txt' )
	game_1 = Game( player_count, final_marble_value )
	game_1.play( )
	game_2 = Game( player_count, final_marble_value, part_2_scale = True )
	game_2.play( )

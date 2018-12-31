# Title: Cursed Menus
# Created by: Jack Bartlett

from os import system
import sys
import curses

class CURSED_WINDOW:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.options = []

	def add_options(self, new_option):
		self.options.append(new_option)
	
	def create_window(self):
		window = curses.newwin(self.y, self.x, 0, 0)
		window.border(0)
		window.refresh()
		window.touchwin()

		output = window.subwin(int(self.y/2), self.x-4, 1, 2)
		output.border(0)
		output.refresh()

		window.getch()

def main():
	# initialising curses
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	screen.keypad(True)
	curses.curs_set(0)

	# get dimensions of screen
	dims = screen.getmaxyx()
	screenX = dims[1]
	screenY = dims[0]	

	# setup screen
	screen.clear()
	screen.refresh()

	#create window
	mainscr = CURSED_WINDOW(screenX, screenY)
	mainscr.create_window()
	screen.refresh()

	# clean up curses before exiting
	curses.nocbreak()
	screen.keypad(False)
	curses.echo()
	curses.endwin()

if __name__ == "__main__":
	main()
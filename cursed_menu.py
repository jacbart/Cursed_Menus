# Title: Cursed Menus
# Created by: Jack Bartlett

from os import system
import sys
import json
import curses

class CURSED_WINDOW:
	def __init__(self, x, y, json_data):
		self.x = x
		self.y = y
		self.title = json_data["name"]
		self.json = json_data
		self.options = []

	def add_options(self):
		for new_option in self.json["options"]:
			self.options.append(new_option)
	
	# function to navigate and display the options
	def navigate(self, window):
		while True:
			window.refresh()
			num_options = len(self.json["options"])
			for o in range(num_options):
				str = self.json["options"][o]["command"]
				window.addstr(int(self.y/2)+1+o, 2, str)

			c = window.getch()
			if c == ord('q'):
				break # exit
	
	def create_window(self):
		window = curses.newwin(self.y, self.x, 0, 0)
		window.border(0)
		window.addstr(0, 2, self.title, curses.A_BOLD)
		window.refresh()
		window.touchwin()

		output = window.subwin(int(self.y/2), self.x-4, 1, 2)
		output.border(0)
		output.refresh()

		self.navigate(window)

def main():
	# initialising curses
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	screen.keypad(True)
	curses.curs_set(0)

	# read in json data
	with open('cursed_scripts/'+'sc'+'.json') as f:
		json_data = json.load(f)

	# get dimensions of screen
	dims = screen.getmaxyx()
	screenX = dims[1]
	screenY = dims[0]	

	# setup screen
	screen.clear()
	screen.refresh()

	#create window
	mainscr = CURSED_WINDOW(screenX, screenY, json_data)
	mainscr.create_window()
	screen.refresh()

	# clean up curses before exiting
	curses.nocbreak()
	screen.keypad(False)
	curses.echo()
	curses.endwin()

if __name__ == "__main__":
	main()
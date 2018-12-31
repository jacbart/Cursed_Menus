# Title: Cursed Menus
# Created by: Jack Bartlett

from os import system
import sys
import json
import curses

class CURSED_WINDOW:
	def __init__(self, x, y, json_data):
		# Width
		self.x = x
		# Height
		self.y = y
		# Title of program
		self.title = json_data["name"]
		# Rest of the json data
		self.json = json_data
	
	# function to navigate and display the options
	def navigate(self, window):
		select = 0
		while True:
			# get number of options for looping
			num_options = len(self.json["options"])
			# loop through options and display them with seceted item being highlighted
			for o in range(num_options):
				str = self.json["options"][o]["name"]
				if o == select:
					window.addstr(int(self.y/2)+1+o, 2, str, curses.A_STANDOUT)
				else:
					window.addstr(int(self.y/2)+1+o, 2, str, curses.A_NORMAL)

			# get keyboard input
			c = window.getch()
			# quite if q is pressed
			if c == ord('q'):
				break # exit
			# move down if s or down arrow are pushed
			elif c == ord('s') or c == curses.KEY_DOWN:
				if select == num_options-1:
					select = 0
				else:
					select = select + 1
			# move up if w or up arrow are pushed
			elif c == ord('w') or c == curses.KEY_UP:
				if select == 0:
					select = num_options-1
				else:
					select = select - 1
			
			window.refresh()
	
	# Creates a window with an output display and leaves room for options
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
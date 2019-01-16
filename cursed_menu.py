# Title: Cursed Menus
# Created by: Jack Bartlett

from os import system
import sys
import time
import asyncio
import string
import json
import curses

class CURSED_WINDOW:
	def __init__(self, x, y, json_data, window_above):
		# Width
		self.x = x
		# Height
		self.y = y
		# Height of displayable space for output screen
		self.rows = int(self.y/2)-1
		# Width of displayable space for output screen
		self.columes = self.x-5
		# Title of program
		self.title = json_data["name"]
		# Rest of the json data
		self.json = json_data
		# Link windows together for traversal
		self.window_above = window_above

	def scroll_output(self, output, row, row_range, text):
		# Printing discription with formatting
		for row in range(row_range):
			if row+1 < self.rows:
				output.addstr(row+1, 2, text[row])
				output.refresh()
			else:
				time.sleep(1)
				output.addstr(1, 2, "testing")
				#self.scroll_output(output, row+1, row_range, text)
				break

	def window_draw(self, window, output, n, select):
		# Grab discription of selected object from json
		discription = self.json["options"][select]["discription"]
		# Spliting up the discription by \\n
		formatted_discription = discription.split("\\n")

		# Clearing, adding border back and refresh the output display
		output.clear()
		output.border(0)
		output.refresh()

		# loop through options and display them with seceted item being highlighted
		for o in range(n):
			str = self.json["options"][o]["name"]
			if o == select:
				window.addstr(int(self.y/2)+1+o, 2, str, curses.A_STANDOUT)
			else:
				window.addstr(int(self.y/2)+1+o, 2, str, curses.A_NORMAL)
		
		row_range = len(formatted_discription)
		self.scroll_output(output, 0, row_range, formatted_discription)
		
		output.refresh()
		window.refresh()
	
	# function to navigate and display the options
	def navigate(self, window, output):
		select = 0
		# get number of options for looping
		num_options = len(self.json["options"])
		self.window_draw(window, output, num_options, select)
		while True:
			is_enter = False
			# get keyboard input
			c = window.getch()
			# quite if q is pressed
			if c == ord('q'):
				break # exit
			# if enter key is pushed
			elif c == 10:
				is_enter = True
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
			self.window_draw(window, output, num_options, select)
			
	# Creates a window with an output display and leaves room for options
	def create_window(self):
		window = curses.newwin(self.y, self.x, 0, 0)

		window.nodelay(0)
		window.keypad(True)
		window.border(0)

		window.addstr(0, 2, self.title, curses.A_BOLD)
		window.addstr(self.y-1, self.x-16, "press q to quit", curses.A_NORMAL)

		window.refresh()
		window.touchwin()

		output = window.subwin(int(self.y/2), self.x-4, 1, 2)
		output.border(0)
		output.refresh()

		self.navigate(window, output)
		window.keypad(False)

def main():
	# initialising curses
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	screen.keypad(True)
	curses.curs_set(0)

	if len(sys.argv) == 1:
		# read in json data
		with open('cursed_scripts/'+'default'+'.json') as f:
			json_data = json.load(f)
	else:
		# read in json data
		script_name = sys.argv[1]
		with open('cursed_scripts/'+script_name+'.json') as f:
			json_data = json.load(f)

	# get dimensions of screen
	dims = screen.getmaxyx()
	screenX = dims[1]
	screenY = dims[0]	

	# setup screen
	screen.clear()
	screen.refresh()

	#create window
	mainscr = CURSED_WINDOW(screenX, screenY, json_data, None)
	mainscr.create_window()
	screen.refresh()

	# clean up curses before exiting
	curses.nocbreak()
	screen.keypad(False)
	curses.echo()
	curses.endwin()

if __name__ == "__main__":
	main()
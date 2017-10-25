#!/usr/bin/env python3
#----------------------------------------------------------------------#
#                        Console MP3 Player                            #
#                                                                      #
# Author: Drew Johnson                                                 #
# Email: drew.m.johnson2@gmail.com                                     #
# Date: October 24th 2017                                              #
#                                                                      #
# This is a mp3 player that can be run directly from your terminal!    #
# With just a few tweaks in the source code you can have this bad boy  #
# working in no time!                                                  #
#                                                                      #
#----------------------------------------------------------------------#

import curses, glob, os, subprocess

path = '/Users/drewjohnson/desktop/songs/*'        # Path for importing file names of songs
prefix = '/Users/drewjohnson/desktop/songs/'       # Prefix to be removed from filenames before displaying on screen
file=glob.glob(path)                               # Method used for grabbing file names from folder containing MP3's
file2 = file                                       # List of raw paths to file. Used for playing songs
files = []                                         # List of edited file names for displaying to user
message = "Arrow keys: select song - Space Bar: start/stop - esc: exit"   # Printed at bottom of screen
isRunning = False                                                               

#---------------------------------------------------------------#
# Function for starting audio player subprocess                 #
# Parameters:                                                   #
# row - The current location of cursor.                         #
#                                                               #
# proecessList - list of current processes.                     #
#---------------------------------------------------------------#

def playSong(row, processList):
    
    if processList[0] == '':                       # Starting first process
        processList[0] = subprocess.Popen(["afplay", file2[row]])
    
    elif processList[0].poll() == None:            # If a process is currently running, kill process, start new one
        processList[0].kill()
        processList[0] = subprocess.Popen(["afplay", file2[row]])
    
    else:                                          # Otherwise, start a process
        processList[0] = subprocess.Popen(["afplay", file2[row]])

#---------------------------------------------------------------#
# This function removes path prefix from file name and then is  #
# stored in a list for printing to the screen.                  #
# Parameters:                                                   #
# text - a full path name to be trimmed.                        #
#                                                               #
# prefix - string to be trimmed.                                #
#---------------------------------------------------------------#
def remove_prefix(text, prefix):
    
    if text.startswith(prefix):
        files.append(text[len(prefix):])

#---------------------------------------------------------------#
# Iterates through raw list of file paths and calls the         #
# function "remove_prefix" for string manipulation              #
#---------------------------------------------------------------#
def setList():
    
    for x in file:
        remove_prefix(x, prefix)

#---------------------------------------------------------------#
# Function behaves as name would suggest.                       #
# Parameters:                                                   #
# processList - list of current processes.                      #
#---------------------------------------------------------------#
def stopPlaying(processList):
    
    processList[0].kill()

#---------------------------------------------------------------#
# Function "beginConsole" creates an infinite loop. This loop   #
# is used for reading user input, namely the up/down/space/esc  #
# keys.                                                         #
#                                                               #
# Parameters:                                                   #
# row - The current location of cursor.                         #
#                                                               #
# isRunning - Used to determine if a current processes is still #
#             running.                                          #
#                                                               #
# window - the current window object used.                      #
#---------------------------------------------------------------#
def beginConsole(row, isRunning, window):
    
    processList = ['']          # Initializing a list to hold active processes
    
    checkRow = row              # Used for keeping track of whether song should be
                                # stopped or new song should be played.

    while (1):
        
        c = window.getch()      # Receive user input

        if c == curses.KEY_DOWN and row < len(files) - 1: # Check to keep user from moving curser past options

            rowDeselection(row, window)                   
            row = row + 1                                 # New position of curser
            window.move(row, 0)                           # Move position of curser down
            rowSelection(row, window)
            window.refresh()                              # Refresh screen
            checkRow = row - 1                            # Previous position of cursor

        elif c == curses.KEY_UP and row > 0:              # Check to keep user from moving curser past options

            rowDeselection(row, window)
            row = row - 1
            window.move(row, 0)
            rowSelection(row, window)
            window.refresh()
            checkRow = row + 1
        
        elif c == ord(' '):                               # Condition for detection of spacebar

            if isRunning == True:                         # If a process is running kill the 
                stopPlaying(processList)                  # process.
                isRunning = False

                if checkRow != row:                       # If curser is on a new line play song
                    playSong(row, processList)            # that is currently selected.
                    isRunning = True

            else:                                         # If no process is running play song
                playSong(row, processList)
                isRunning = True
        
            checkRow = row
        
        elif c == 27:                                           # Check for escape key
            newProc = subprocess.Popen(['killall', 'afplay'])   # Kill all processes
            break                                               # Break from loop for termination 
                                                                # of program.
            
#---------------------------------------------------------------#
# Function prints options from list to screen for user          #
# selection.                                                    #
#                                                               #
# Parameters:                                                   #
# row - The current location of cursor.                         #
#                                                               #
# height - height of window.                                    #
#                                                               #
# width - width of the window                                   #
#                                                               #
# window - the current window object used                       #
#---------------------------------------------------------------#
def printOptions(row, height, width, window):
    
    counter = 0
    for i in range(0, height):            # prints until bottom of screen is reached
        
        if i == len(files):               # If all files are printed to the screen
            break                         # then break out of loop

        if row == 0:                                       
                                                           
            window.addstr(files[i], curses.color_pair(1))  # Highlights first option                            
            row = row + 1                                  
            window.move(row, 0)

        else:
            
            window.addstr(files[i])                 #
            row = row + 1                           # Prints rest of list
            window.move(row, 0)                     #

    window.move(height - 3, 0)                      # Moves cursor to bottom of the screen
    window.addstr(message, curses.color_pair(2))    # Adds instructions with blue highlight
    

    for i in range(len(message), width - 2):        # adds color to remaining spaces of the line
        window.addstr(" ", curses.color_pair(2))

    window.move(0, 0)                               # Move cursor to the top

#---------------------------------------------------------------#
# Function reprints selected row with highlighted text          #
#                                                               #
# Parameters:                                                   #
# row - The current location of the cursor.                     #
#                                                               #
# window - The current window object used.                      #
#---------------------------------------------------------------#
def rowSelection(row, window):                  

    text = files[row]                                       # Line to reprint
    window.addnstr(text, len(text), curses.color_pair(1))   # Reprint line with highlight
    window.move(row, 0)                                     # Moves cursor back to beginning of line

#---------------------------------------------------------------#
# Function reprints selected without highlighted text           #
#                                                               #
# Parameters:                                                   #
# row - The current location of the cursor.                     #
#                                                               #
# window - The current window object used.                      #
#---------------------------------------------------------------#
def rowDeselection(row, window):
    # Function reprints previously selected row with normal color

    text = files[row]                           # Line to reprint
    window.addnstr(text, len(text))             # Reprint line with highlight
    window.move(row, 0)                         # Moves cursor back to beginning of line

#---------------------------------------------------------------#
# Do you really need to know what this function does?           #
#---------------------------------------------------------------#
def main():  
    
    row = 0
    setList()
    stdscr = curses.initscr()           # Begin curses window
    curses.noecho()                     #
    stdscr.idlok(True)                  # Use hardware line editing facilities.
    height,width = stdscr.getmaxyx()    # Get width and height of window
    window = stdscr.subwin(height-1, width-1, 1, 1) # Create subscreen
    window.scrollok(True)
    stdscr.border(0)            # Create border around subscreen.
    
                                
    curses.curs_set(0)          # Set cursor visibility to False
    window.keypad(1)            # Enable special keys
    

    stdscr.nodelay(1)           # getch() will be non-blocking.

    curses.start_color()        # Enable color for highlighting
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Color pair 1 for selection highlighting
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Color pair 2 for instruction bar

    printOptions(row, height, width, window)   # Prints selection options
   
    row = 0
    window.move(row, 0)         # Sets cursor position to (0,0)
    stdscr.refresh()            # Refreshes screen to print changes
    beginConsole(row, isRunning, window)   # Begin user input

    curses.nocbreak()           #
    stdscr.keypad(0)            # End curses and terminate program
    curses.echo                 #
    curses.endwin()             #

if __name__ == '__main__':
    main()
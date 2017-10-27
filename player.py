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
message = "Arrow keys: select song/change page - Space Bar: start/stop - esc: exit"  # Printed at bottom of screen
space = "    "
isRunning = False   
multiList = []
playList = []                                                    

#---------------------------------------------------------------#
# Function for starting audio player subprocess                 #
# Parameters:                                                   #
# row - The current location of cursor.                         #
#                                                               #
# proecessList - list of current processes.                     #
#                                                               #
# page - current location in multi-dimensional list             #
#---------------------------------------------------------------#
def playSong(row, processList, page):
    
    if processList[0] == '':                       # Starting first process
        processList[0] = subprocess.Popen(["afplay", playList[page][row]])
    
    elif processList[0].poll() == None:            # If a process is currently running, kill process, start new one
        processList[0].kill()
        processList[0] = subprocess.Popen(["afplay", playList[page][row]])
    
    else:                                          # Otherwise, start a process
        processList[0] = subprocess.Popen(["afplay", playList[page][row]])

#---------------------------------------------------------------#
# Function behaves as name would suggest.                       #
# Parameters:                                                   #
# processList - list of current processes.                      #
#---------------------------------------------------------------#
def stopPlaying(processList):
    
    processList[0].kill()

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
# This function gets the paths of all songs. It initializes     #
# a list that's used for playing audio files.                   #
# Parameters:                                                   #
# file - list of raw file paths                                 #
#                                                               #
# wheight - height of subwindow                                 #
#                                                               #
# playList - list that's used for playing audio files.          #
#                                                               #
# page - current location in multi-dimensional list.            #
#---------------------------------------------------------------#
def getPlaylist(file, wheight, playList, page):         
    filePlaceHolder = 0
    while(1):
    
        holdFile = []
    
        for x in range(0, wheight - 2):     # Adds items to a hold list
        
            holdFile.append(file[filePlaceHolder]) 
            filePlaceHolder += 1

            if filePlaceHolder == len(file):
                break
    
        playList.append(holdFile)           # Adds hold list to another list
        page += 1

        if filePlaceHolder == len(file):
            break

#---------------------------------------------------------------#
# This function moves the file names of all imported songs      #
# into a multidimensional list.                                 #
# Parameters:                                                   #
#                                                               #
# files - list of file names with full path stripped off        #
#                                                               #
# whight - height of subwindow                                  #
#                                                               #
# multiList - multi-dememsional list containing song names by   #
# by page number.                                               #
#                                                               #
# page - current location in multi-dimensional list.            #
#---------------------------------------------------------------#

def getList(files, wheight, multiList, page):
    filePlaceHolder = 0
    while(1):
    
        holdFile = []                # Adds items to a hold list
    
        for x in range(0, wheight - 2):
        
            holdFile.append(files[filePlaceHolder])
            filePlaceHolder += 1

            if filePlaceHolder == len(file):
                break
    
        multiList.append(holdFile)  # Adds hold list to another list
        page += 1

        if filePlaceHolder == len(files):
            break

#---------------------------------------------------------------#
# This function clears the screen for the next page to be       #
# displayed.                                                    #
# Parameters:                                                   #
#                                                               #
# window - The current window object used.                      #
#                                                               #
# multiList - multi-dememsional list containing song names by   #
# by page number.                                               #
#                                                               #
# whight - height of subwindow                                  #
#                                                               #
# wwidth - width of the subwindow                               #
#                                                               #
# row - The current location of the cursor.                     #
#---------------------------------------------------------------#
def clearLine(window, multiList, wheight, wwidth, row):
    
    window.move(0,0)

    for i in range(0, wheight - 1):
        
        for x in range(0, wwidth - 1):
            
            window.addstr(" ")

        row = row + 1
        window.move(row, 0)

    row = 0
    window.move(row,0)

#---------------------------------------------------------------#
# Function reprints selected row with highlighted text          #
#                                                               #
# Parameters:                                                   #
# row - The current location of the cursor.                     #
#                                                               #
# window - The current window object used.                      #
#                                                               #
# multiList - multi-dememsional list containing song names by   #
# by page number.                                               #
#                                                               #
# page - current location in multi-dimensional list.            #
#---------------------------------------------------------------#
def rowSelection(row, window, multiList, page):                  

    text = multiList[page][row]                             # Line to reprint
    window.addnstr(text, len(text), curses.color_pair(1))   # Reprint line with highlight
    window.move(row, 0)                                     # Moves cursor back to beginning of line

#---------------------------------------------------------------#
# Function reprints selected without highlighted text           #
#                                                               #
# Parameters:                                                   #
# row - The current location of the cursor.                     #
#                                                               #
# window - The current window object used.                      #
#                                                               #
# multiList - multi-dememsional list containing song names by   #
# by page number.                                               #
#                                                               #
# page - current location in multi-dimensional list.            #
#---------------------------------------------------------------#
def rowDeselection(row, window, multiList, page):

    text = multiList[page][row]                 # Line to reprint
    window.addnstr(text, len(text))             # Reprint line with highlight
    window.move(row, 0)                         # Moves cursor back to beginning of line

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
#                                                               #
# whight - height of subwindow                                  #
#                                                               #
# wwidth - width of the subwindow                               #
#                                                               #
# multiList - multi-dememsional list containing song names by   #
# by page number.                                               #
#                                                               #
# page - current location in multi-dimensional list.            #
#---------------------------------------------------------------#
def beginConsole(row, isRunning, window, wheight, wwidth, multiList, page):
    
    getPlaylist(file, wheight, playList, page)
    
    processList = ['']          # Initializing a list to hold active processes
    
    checkRow = row              # Used for keeping track of whether song should be
                                # stopped or new song should be played.

    while (1):
        
        c = window.getch()      # Receive user input

        if c == curses.KEY_DOWN and row < len(multiList[page]) - 1: # Check to keep user from moving curser past options

            rowDeselection(row, window, multiList, page)                   
            row = row + 1                                 # New position of curser
            window.move(row, 0)                           # Move position of curser down
            rowSelection(row, window, multiList, page)
            window.refresh()                              # Refresh screen
            checkRow = row - 1                            # Previous position of cursor

        elif c == curses.KEY_UP and row > 0:              # Check to keep user from moving curser past options

            rowDeselection(row, window, multiList, page)
            row = row - 1
            window.move(row, 0)
            rowSelection(row, window, multiList, page)
            window.refresh()
            checkRow = row + 1

        elif c == curses.KEY_RIGHT and page < len(multiList) - 1:
            
            page = page + 1                                # New page number
            row = 0
            clearLine(window, multiList, wheight, wwidth, row)  # Clears screen
            printOptions(row, window, wheight, wwidth, page)    # Prints next page to screen
            window.refresh()
            row = 0
            window.move(row, 0)
        
        elif c == curses.KEY_LEFT and page > 0:

            page = page - 1
            row = 0
            clearLine(window, multiList, wheight, wwidth, row)
            printOptions(row, window, wheight, wwidth, page)
            window.refresh()
            row = 0
            window.move(row, 0)
        
        elif c == ord(' '):                               # Condition for detection of spacebar

            if isRunning == True:                         # If a process is running kill the 
                stopPlaying(processList)                  # process.
                isRunning = False

                if checkRow != row:                       # If curser is on a new line play song
                    playSong(row, processList, page)            # that is currently selected.
                    isRunning = True

            else:                                         # If no process is running play song
                playSong(row, processList, page)
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
# window - the current window object used                       #
#                                                               #
# wheight - height of the subwindow.                            #
#                                                               #
# wwidth - width of the subwindow                               #
#                                                               #
# page - current location in multi-dimensional list.            #
#---------------------------------------------------------------#  
def printOptions(row, window, wheight, wwidth, page):

    for x in range(0, len(multiList[page])):
        
        if x == len(multiList[page]) or row == wheight - 1:  # Terminates printing if end of screen
            break                                            # or end of list is reached
        
        if row == 0:    # Highlights first option on screen
            window.addstr(multiList[page][x], curses.color_pair(1))
            row = row + 1
            window.move(row, 0)

        else:
            
            window.addstr(multiList[page][x])
            row = row + 1
            window.move(row, 0)

    fullMessage = "Page: " + str(page + 1) + space + message
    window.move(wheight - 2, 0)                      # Moves cursor to bottom of the screen
    window.addstr(fullMessage, curses.color_pair(2)) # Adds instructions with blue highlight

    for i in range(len(message), wwidth - 12):       # adds color to remaining spaces of the line
        window.addstr(" ", curses.color_pair(2))

    window.move(0, 0)                                # Move cursor to the top


#---------------------------------------------------------------#
# Do you really need to know what this function does?           #
#---------------------------------------------------------------#
def main():  
    
    page = 0  
    row = 0
    setList()                       
    stdscr = curses.initscr()           # Begin curses window
    curses.noecho()                     #
    stdscr.idlok(True)                  # Use hardware line editing facilities.
    height,width = stdscr.getmaxyx()    # Get width and height of window
    window = stdscr.subwin(height-1, width-1, 1, 1) # Create subscreen
    window.scrollok(True)
    stdscr.border(0)            # Create border around subscreen.
    wheight, wwidth = window.getmaxyx()
    
                                
    curses.curs_set(0)          # Set cursor visibility to False
    window.keypad(1)            # Enable special keys
    

    stdscr.nodelay(1)           # getch() will be non-blocking.

    curses.start_color()        # Enable color for highlighting
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Color pair 1 for selection highlighting
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Color pair 2 for instruction bar

    getList(files, wheight, multiList, page)    # Get list of options to print on screen
    printOptions(row, window, wheight, wwidth, page) # Display options on screen

    row = 0
    window.move(row, 0)         # Sets cursor position to (0,0)
    stdscr.refresh()            # Refreshes screen to print changes
    beginConsole(row, isRunning, window, wheight, wwidth, multiList, page)   # Begin user input

    curses.nocbreak()           #
    stdscr.keypad(0)            # End curses and terminate program
    curses.echo                 #
    curses.endwin()             #

if __name__ == '__main__':
    main()
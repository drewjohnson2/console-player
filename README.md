# Console MP3 Player

## What works
* Play/Stop
* Selection Highlighting
* Loading of file names to screen

## What doesn't work
* Pause
* Scrolling / Loading more options than can fit on screen
* Gathering songs from multiple directories

## Dependencies

| Dependency | Reason |
| ---------- | ------ |
| Curses     | You'll need this library because it's how the program makes the displayed information interactive with the                     user. Library should be installed by ```pip3 install ```|
| Glob | This library is needed to gather all of the filenames for the songs in your path. Library should be installed by ```pip3 install ```|
| Subprocess | This library handles the music player in the background. Library should be pre-installed with python3, however, if it is not library should be installed by ```pip3 install ```
| afplay | Afplay is a command line audio player that comes built in to most Macs. This is the audio player I chose to use for playing the music so if you don't already have it on your device you'll need to download it.
| Python 3 | I wrote this program in python 3 so trying to run it with any other version will more than likely give you a real bad time.|

## Modification
You'll need to modify a few lines of the source code to get the player working with your system. Below I'll highlight the lines needed to get the player up and running on your system.

### Path for file importing
On line 17 you'll see <br />
```python
path = '/Users/drewjohnson/desktop/songs/*'
``` 
You'll need to change this line to the path to directory containing the songs you wish to have the player reference. So, for example, you'll need something like this:<br />
```python
path = '/path/to/your/music/files/*'
```
<br />

**Note 1: it's important you leave the `*` at the end of your file path. This ensures that all the files in that directory get brought into the music player** <br/>
**Note 2: as of this version of the console player you'll need to limit the amount of songs brought into the player relative to the size of the screen due to the fact that scrolling is not yet supported.**

### Prefix
On line 18 you'll see something very similar
```python
prefix = '/Users/drewjohnson/desktop/songs/
```
This should be the same as line 17 but without the asterisk at the end. This line of code is used to match what we need to remove from the file names before we display them to the user.

## Contact
If you have any questions or have improved my console player in any way be sure to contact me so we can talk about it!
drew.m.johnson2@gmail.com

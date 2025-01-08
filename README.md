# What is this?
This is a small program that will make it easier to execute the command necessary to authenticate you into Dead Frontier 3D Inner City. This program also makes it super easy to authenticate your account when playing using Linux and Proton/Wine.

# Why you made this?
I made this to work together with my Greasy Fork script: [Dead Frontier at work](https://greasyfork.org/en/scripts/468944-dead-frontier-at-work)

This program provides a simple interface for the user to save the deadfrontier.exe path and to put his/her authentication token to login into the Inner City.

# How does it works?
Put the Executable Path and your Authentication Token in the desired input fields like in the image below:

![DF3Datwork](https://github.com/ils94/DF3D_at_Work/blob/main/f9KeG8h.png?raw=true)

In the new version of this program, your token will automatically be pasted into the Authentication Token field and immediately cleared from your clipboard (to prevent accidental exposure). If the automatic pasting doesn't work, you will need to paste your token manually. In this case, your clipboard will not be cleared, so beware.

If you do not want to type the whole path to deadfrontier.exe, you can copy all the files inside the df3datwork folder into the Dead Frontier folder, and leave the input for Executable Path empty.

Then you press the "Login" button, wait for the Standalone Client to open, and then once it open, press the "Play!" button and wait for the server to authenticate you into the Inner City.

# Download

You can download this from this [link](https://github.com/ils94/DF3D_at_Work/releases/download/release-v2/df3datwork.zip)

# Compiling it yourself

For reference, I use Python 3.8 32bits.

Download and install Python from: https://www.python.org/downloads/

Open your CMD and type: pip install pyinstaller

Then type: pyinstaller "path/to/df3datwork.py" --onedir --noconsole --icon="path/to/dficon.ico"

Wait for pyinstaller to compile the .py script into a .exe, and the result should be in a folder called "dist" inside the folder where df3datwork.py is.

If you do not have pip/python in your Window's Env:

Open Window's CMD and type:

"path/to/your/python/python.exe" "path/to/your/python/Scripts/pip.exe" install pyinstaller

and wait for the installation, then type:

"path/to/your/python/python.exe" "path/to/your/python/Scripts/pyinstaller.exe" "path/to/df3datwork.py" --onedir --noconsole --icon="path/to/dficon.ico"

Wait for pyinstaller to compile into a .exe, and the result should be in a folder called "dist" inside the folder where df3datwork.py is.

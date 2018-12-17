#!/usr/bin/python

#this example show how to write text to the LCD by the means of the LCD named pipe from python scripts

import os
#communicate with the LCD controller process through named pipe
wfPath = "/tmp/lcd_pipe"
try:
    os.mkfifo(wfPath)
except OSError:
    pass
wp = open(wfPath, 'w')

#write the expression "Your LCD is well configured" in the LCD display
wp.write("2|2|your LCD\n")
wp.write("3|2|is well configured\n")		
wp.close()

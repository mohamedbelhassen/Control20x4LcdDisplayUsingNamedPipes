#!/usr/bin/python
import os

#communicate with the LCD controller process through named pipe

#if you have changed the path of the named path of your LCD display, update the following line
pipePath = "/tmp/lcd_pipe"

#open the pipe file in wrting mode
wp = open(pipePath, 'w')

#write the expression "Your LCD is well configured" in the LCD display
wp.write("2|2|your LCD")
wp.write("3|2|is well configured")		

#finally, close the file object
wp.close()

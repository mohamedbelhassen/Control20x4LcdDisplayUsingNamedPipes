#!/usr/bin/python

#this library is based on the following tutorial (https://www.raspberrypi-spy.co.uk/2015/05/using-an-i2c-enabled-lcd-screen-with-the-raspberry-pi/)
#Our library is more powerful since it enables other scripts to control the content of the LCD through named pipes which could be accessed from various programs like python, c, c++, script shell, php, etc.
#author name: Mohamed Belhassen
#author website: www.creativeteam.tn

import smbus
import time
import sys
import cPickle
import os

i = 0
lcdTextContent = ["","","","",""] #L: array containing the text of line1..4  indexed with line number , initially does not contains anything
textCentering = ["1","1","1","1","1"] # centering: contains centering of text: 1:left 2:center: 3: right
separator="|"
#communicate with another process through named pipe
pipePath ="/tmp/lcd_pipe" #important: this path have to be configured such as it fits your home directory

try:
    os.mkfifo(pipePath)
except OSError:
    pass

# Define some device parameters
I2C_ADDR  = 0x3f # 0x27  I2C device address
LCD_WIDTH = 20   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

global LCD_BACKLIGHT
LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified
 
  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def refreshLCD():
	lcd_init()
	if RepresentsInt(textCentering[1])==True:				
		lcd_string(lcdTextContent[1],LCD_LINE_1,int(textCentering[1]))
	if RepresentsInt(textCentering[2])==True:				
		lcd_string(lcdTextContent[2],LCD_LINE_2,int(textCentering[2]))
	if RepresentsInt(textCentering[3])==True:				
		lcd_string(lcdTextContent[3],LCD_LINE_3,int(textCentering[3]))
	if RepresentsInt(textCentering[4])==True:				
		lcd_string(lcdTextContent[4],LCD_LINE_4,int(textCentering[4]))
	print "LCD display refreshed"


def main():
  # Main program block
  # Initialise display
	lcd_init()
	global LCD_BACKLIGHT

	while True:
	
		rp = open(pipePath, 'r')
		response = rp.read()
		rp.close()
		responseLines=response.split("\n")
		nbLines = len(responseLines)
		#print "nb line: %d" % len(responseLines)
		#print responseLines
		for i in range(0, nbLines):
			if len(responseLines[i])==0:
				continue
			elif responseLines[i] == "clear":
				lcd_init()
				print "LCD display cleared"
				continue
			elif responseLines[i] == "refresh":			
				refreshLCD()
				continue
			elif responseLines[i] == "backlight=off":
				#global LCD_BACKLIGHT
				LCD_BACKLIGHT = 0x00  #Off
				refreshLCD()
				print "LCD backlight turned off"
				continue
			elif responseLines[i] == "backlight=on":
				#global LCD_BACKLIGHT
				LCD_BACKLIGHT = 0x08  # On
				refreshLCD()
				print "LCD backlight turned on"
				continue
			#print "line nb: %d: %s length: %d" % (i, responseLines[i],len(responseLines[i]))
			sR=responseLines[i].split(separator)
			#showLine = 1

			if len(sR) != 3 :
				print "incorrect number of fields %d  lineArgPassed: %s" % (len(sR), responseLines[i])			
				continue
			style = int(sR[1])
			lineNb=int(sR[0])		

			if lineNb < 5:
				lcdTextContent[lineNb]=sR[2]
				textCentering[lineNb]=sR[1]
			if len(sR)==3: 
				if lineNb==1:   				
					cd_string(sR[2],LCD_LINE_1,style)				
				elif lineNb==2:
					lcd_string(sR[2],LCD_LINE_2,style)
				elif lineNb==3:
					lcd_string(sR[2],LCD_LINE_3,style)
				elif lineNb==4:
					lcd_string(sR[2],LCD_LINE_4,style)


if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)


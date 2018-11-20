# Control 20x4 LCD Display Using Named Pipes

This project let you easily controlling the 20x4 I2C LCD display from external scripts and programs using named pipes

# How to configure your Raspberry Pi before using this project?

This project assumes that the I2C interface is enabled in your Raspberry Pi. If not, please refer to the following youtube tutorial to activate this interface: 
https://www.youtube.com/watch?v=0Ny_88I9gWM

# which hardware I need to use this project?

This LCD controller is designed for 20x4 LCD display having I2C interface.

So, to use this project, you need the following components:

1-20x4 LCD display with I2C interface

2-Logic level shifter (3.3V - 5V)

3-some wires & ideally a breadboard

# How to wire LCD display to Raspberry Pi?

Please, refer to the following link to see how should you connect the LCD display to Raspberry Pi:


# How to use this controller?

In order to use this controller, you have to clone (copy) it to your Raspberry Pi.

After that, you have to navigate to the folder containing "lcd_controller.py" file and add the execution permission to this file using the following command

    sudo chmod +x ./lcd_controller.py

Then, execute this file using the following command (in the same folder):
    ./lcd_controller.py

----------------------------------------------------------------------------------------------------------------------------------

Note: You can add the following line toi the crontab using the (crontab -e) command to launch the controller at the starting of the Raspberry Pi

    @reboot   /<here type the full path to the folder containing the folder of the controller>/lcd_controller.py

----------------------------------------------------------------------------------------------------------------------------------

# how to write text on the LCD Display using this controller?

Our controller is designed so that it receives the text content and formatting through named pipes. 
In other words, each time we need to write text from any external script or program, we have to write a special command inside a text file which is located, by default, in the following path:

/tmp/lcd_pipe

For instance, if we would like to write the expression "Hello world" in the third line of our LCD display and align it to the center, we have to write the following command to the named pipe:  
    3|2|Hello world

To do so, from a terminal, just execute the following command:

    echo "3|2|Hello world" >> /tmp/lcd_pipe

The general format of the command to write on the pipi file is as following:

    NumberOfTheLineToWriteTo|TextAlignCode|TextToWriteInLCD
    
 Note:
 
 1- NumberOfTheLineToWriteTo is the number of the line of the LCD in which we intend to write to
 
 2- TextAlignCode: here just write :  1 to align the text to the left
                                      2 to align the text to the center
                                      3 to align the text to the right
                                      
 3- TextToWriteInLCD: is the text to write in the chosen line. Do not exceed 20 character per line
 
 4- By default, the controller uses the vertical line character to separate the various fields : "|". So, the text to write to the LCD has to not contain this special character. If so, you can edit the separator variable used in our controller and change it to another character.
 
 # Can I control the backlight of The LCD from external scripts?
 
 The short answer is "Yes". 
 
 But we can just switch from on to off and vice versa.
 
 If you would like to fine tune the level of lightening, you have to use a resistance in the two pins of the I2C interface.
 
 1- To turn on the LCD backlight from external script, you have to write "backlight=on" to the named pipe :
     echo "backlight=on" >> /tmp/lcd_pipe

2- To turn off the LCD backlight from external script, you have to write "backlight=off" to the named pipe :
     echo "backlight=off" >> /tmp/lcd_pipe
     
 # Can I refresh the LCD display content from external scripts?
 
  The short answer is "Yes".
  
  To refresh the LCD content from external script, you have to write "refresh" to the named pipe :
  
     echo "refresh" >> /tmp/lcd_pipe
   
   Refreshing the LCD content is useful in some cases like using magnetic Relay which may affect the content of LCD Display.
   
  # Can I clear the LCD display content from external scripts?
  
 The short answer is "Yes".
  
  To clear the LCD content from external script, you have to write "refresh" to the named pipe :
  
     echo "clear" >> /tmp/lcd_pipe


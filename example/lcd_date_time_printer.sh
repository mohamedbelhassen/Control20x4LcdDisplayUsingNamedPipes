#!/bin/bash

pipePath="/tmp/lcd_pipe" 
read hh mm day month year jourAbr dayOfWeek< <(date +"%H %M  %d  %m  %Y %a %a");
textToDisplay="$dayOfWeek.$day/$month/$year $hh:$mm"
echo "1|1|$textToDisplay">>$pipePath

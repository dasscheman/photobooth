#!/bin/bash
mogrify -rotate 90 -resize 942x628 /home/pi/photobooth/pics/*.jpg
montage /home/pi/photobooth/pics/*.jpg -tile 2x2 -geometry +10+10 /home/pi/photobooth/temp/temp_montage2.jpg
composite -gravity center /home/pi/photobooth/label.jpg  /home/pi/photobooth/temp/temp_montage2.jpg /home/pi/photobooth/temp/temp_montage3.jpg
#montage /home/pi/photobooth/temp/temp_montage2.jpg /home/pi/photobooth/label.jpg -tile 2x1 -geometry +5+5 /home/pi/photobooth/temp/temp_montage3.jpg
suffix=$(date +%H%M%S)
cp /home/pi/photobooth/temp/temp_montage3.jpg /home/pi/photobooth/assembled_pics/PB_${suffix}.jpg

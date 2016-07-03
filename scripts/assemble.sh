#!/bin/bash
mogrify -resize 942x628 /home/pi/photobooth/pics/*.jpg
montage /home/pi/photobooth/pics/*.jpg -tile 2x2 -geometry +10+10 /home/pi/photobooth/temp/temp_montage3.jpg
suffix=$(date +%H%M%S)
cp /home/pi/photobooth/temp/temp_montage3.jpg /home/pi/photobooth/assembled_pics/PB_${suffix}.jpg
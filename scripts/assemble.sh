#!/bin/bash
mogrify -resize 968x648 /home/pi/photobooth/pics/*.jpg
montage /home/pi/photobooth/pics/*.jpg -tile 2x2 -geometry +10+10 /home/pi/photobooth/temp/temp_montage2.jpg
montage /home/pi/photobooth/temp/temp_montage2.jpg /home/pi/photobooth/label.jpg -tile 2x1 -geometry +5+5 /home/pi/photobooth/temp/temp_montage3.jpg
suffix=$(date +%H%M%S)
cp /home/pi/photobooth/temp/temp_montage3.jpg /home/pi/photoboot/assembled_pics/PB_${suffix}.jpg
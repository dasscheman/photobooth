# Copy this file to config.py and replace the values with your information
file_path = '~/home/pi/photobooth/pics/' # path to save images tempory
file_path_gif = '~/home/pi/Website/pibooth/web/photobooth/' # path to save images for site

post_online = 1 # default 1. Change to 0 if you don't want to upload pics.
print_pic = 1 # default 1. Change to 0 if you don't want to print pics.
total_pics = 4 # number of pics to be taken
capture_delay = 2 # delay between pics
prep_delay = 3 # number of seconds at step 1 as users prep to have photo taken
gif_delay = 100 # How much time between frames in the animated gif
restart_delay = 5 # how long to display finished message before beginning a new session
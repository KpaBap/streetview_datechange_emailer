# streetview_datechange_emailer

-  Author: Iavor Todorov (kpabap@gmail.com)
Requires: Python 3.x, Selenium, and Chrome WebDriver
Install Selenium with - pip install selenium
Install: https://sites.google.com/a/chromium.org/chromedriver/ to /usr/local/bin or however your POS OS does it

This script loads a StreetView page and tries to find the image capture date based on a string provided in the script. 
If a match is found, a screenshot is taken and emailed.

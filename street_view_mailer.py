try:
    from selenium import webdriver
except:
    raise RuntimeError("Install Selenium for Python 3.x please")

import re
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

"""
Author: Iavor Todorov (kpabap@gmail.com)
Requires: Python 3.x, Selenium, and Chrome WebDriver
Install selenium with - pip install selenium
Install: https://sites.google.com/a/chromium.org/chromedriver/ to /usr/local/bin or however your OS does it
"""

def send_email_with_attachment(email_from, email_to, subject, smtp_ip_port, smtp_username, smtp_password, attachment_filename):
    """This function sends an email with an attachment using the provided credentials and filename """
    email = MIMEMultipart()
    email["From"] = email_from
    email["To"] = email_to
    email['Subject'] = subject
    email.preamble = email['Subject']

    content_type, encoding = mimetypes.guess_type(attachment_filename)
    if content_type is None or encoding is not None:
        content_type = "application/octet-stream"
    main_type, sub_type = content_type.split("/", 1)

    if main_type == "image":
        file_pointer = open(attachment_filename, "rb")
        attachment = MIMEImage(file_pointer.read(), _subtype=sub_type)
        file_pointer.close()
    else:
        file_pointer = open(attachment_filename, "rb")
        attachment = MIMEBase(main_type, sub_type)
        attachment.set_payload(file_pointer.read())
        file_pointer.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=attachment_filename)
    email.attach(attachment)

    server = smtplib.SMTP(smtp_ip_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(email_from, email_to, email.as_string())
    server.quit()

def load_page_and_save_screenshot_on_match(url, search_string, screenshot_filename):
    """This function loads a URL in Chrome Webdriver and tries to find the label "Image Capture" to determine when a particular
        StreetView picture was taken - if a match is found, a screenshot file is saved"""
    try:
        browser = webdriver.Chrome()
    except:
        raise RuntimeError("Probably need to install Chromedriver")
    browser.implicitly_wait(10)  # seconds
    browser.maximize_window()
    browser.get(url)

    image_capture_tag = browser.find_elements_by_xpath("//*[contains(text(), 'Image capture')]")[0]
    image_capture_date = image_capture_tag.text

    if re.match(".*{}".format(search_string), image_capture_date):
        browser.save_screenshot(screenshot_filename)
        print ("Search string was found. Saved screenshot file: {}".format(screenshot_filename))
        browser.close()
        return True
    else:
        browser.close()
        return False

if __name__ == "__main__":

    # Set these parameters for the page to load and the string to try and look for
    screenshot_filename = "screenshot.png"
    url = "https://www.google.com/maps/place/Golden+Gate+Bridge/@37.819352,-122.4783739,3a,60y,90t/data=!3m6!1e1!3m4!1sanDJxWsNq6y0PtH6JzfuZw!2e0!7i13312!8i6656!4m5!3m4!1s0x808586deffffffc3:0xcded139783705509!8m2!3d37.8199286!4d-122.4782551!6m1!1e1"
    search_string = "2016"

    # These are required to send emails
    smtp_ip_port = "smtp.gmail.com:587"
    smtp_username = "username@gmail.com "
    smtp_password = "abcedfgh123"
    email_from = smtp_username
    email_to = "email@wherever.com"
    subject = "Google StreetView image updated to {}!".format(search_string)

    if load_page_and_save_screenshot_on_match(url, search_string, screenshot_filename):
        send_email_with_attachment(email_from, email_to, subject, smtp_ip_port,smtp_username,smtp_password,screenshot_filename)
        print ("Email sent.")
    else:
        print ("Sorry, the image does not seem to be updated yet.")

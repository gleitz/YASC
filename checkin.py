#!/usr/bin/python

################################################################################
# YASC: Yet Another Southwest Checkin
# Benjamin Gleitzman (gleitz@mit.edu) - November 2012
#
# Usage: checkin.py <FIRSTNAME> <LASTNAME> <CONFIRMATIONNUMBER> <EMAIL>
#
# Cron may be used to schedule a future checkin.
# A sample cron entry to perform a checkin on December 20, 2013 at 8:45AM:
# 45 08 20 12 * python /path/to/checkin.py Firstname Lastname Confirmation Email
################################################################################

import requests
import sys
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def checkin(firstname, lastname, confirmation, email):
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Host': 'mobile.southwest.com',
               'Origin': 'http://mobile.southwest.com',
               }

    print 'Creating session...'
    s = requests.session()

    # Obtain the 'cacheid' cookie required for checkin
    r = s.get('http://mobile.southwest.com/p', headers=headers)
    cache_id = r.cookies.get('cacheid')
    time.sleep(2)

    print 'Finding reservation...'
    payload = {'cacheid': cache_id,
               'formid': 'CheckIn',
               'cat': 'large',
               'pfi': 'main',
               'textfieldconfirm': confirmation,
               'tffname': firstname,
               'tflname': lastname,
               'button35607event_': 'Retrieve Reservation'}
    r = s.post('http://mobile.southwest.com/p/CheckIn', data=payload, headers=headers)
    time.sleep(2)

    print 'Checking in...'
    payload = {'cacheid': cache_id,
               'formid': 'AvailBoardingPass',
               'cat': 'large',
               'pfi': 'CheckIn',
               'button7063701615128event_': 'Check In'}
    r = s.post('http://mobile.southwest.com/p/AvailBoardingPass',
               data=payload,
               headers=headers)

    with open('secret.txt', 'r') as f:
        lines = f.read().strip()
        username, password = lines.split('||')

    if not email:
        print 'Checked in successfully.'
        return

    print 'Sending boarding pass to {0}...'.format(email)
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(username, password)
    msg = MIMEMultipart('mixed')
    msg['Subject'] = 'You are checked into your flight'
    msg['To'] = email
    msg['From'] = username
    msg.attach(MIMEText('Boarding pass is attached', 'plain'))
    msg_bp = MIMEText(r.text, 'html')
    msg_bp.add_header('content-disposition', 'attachment', filename='boarding_pass.html')
    msg.attach(msg_bp)
    smtp.sendmail(email, username, msg.as_string())

    print 'Boarding pass sent successfully'
    smtp.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: checkin.py <FIRSTNAME> <LASTNAME> <CONFIRMATIONNUMBER> <EMAIL>'
    else:
        if len(sys.argv) == 5:
            email = sys.argv[4]
        else:
            email = ''
        checkin(sys.argv[1], sys.argv[2], sys.argv[3], email)

# -----------------------------------------------------------
# Generate a new access-code for the ISE Hotspot portal,
# push it to the ISE using API and send an email with
# new access-code
#
# requires the portal-id
#
# (C) 2019 Dmitry Golovach
# email dmitry.golovach@outlook.com
# -----------------------------------------------------------

import requests
import json
import random
import string
from requests.auth import HTTPBasicAuth
import smtplib

def send_email(access_code):
    """
    Send email with new generated access code
    Configuration could be different if another SMTP server is in use
    Current setup is for Gmail account.

    Parameters to change:
    YOUR_EMAIL@GMAIL.COM - email to use as from address
    YOUR_EMAIL@GMAIL.COM - email to use as to address
    YOUR_GMAIL_APP_PASSWORD - password for gmail account
    """
    fromaddr = "YOUR_EMAIL@GMAIL.COM"
    toaddr = "YOUR_EMAIL@GMAIL.COM"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, "YOUR_GMAIL_APP_PASSWORD")
    SUBJECT = "New Guest Password"
    TEXT = "New Guest Password: " + str(access_code)
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server.sendmail(fromaddr, toaddr, message)
    server.quit()
    return


def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def main():
    """
    Send email with new generated access code
    Configuration could be different if another SMTP server is in use
    Current setup is for Gmail account.

    Parameters to change:
    ISE_PAN_IP - ISE PAN IP address
    HOTSPOT-PORTAL-ID - ISE Hotspot Portal ID
    HOTSPOT-PORTAL-NAME - ISE Hotspot Portal NAME
    ISE_USERNAME - ISE API username
    ISE_PASSWORD - ISE API password
    """
    url = 'https://<ISE_PAN_IP>:9060/ers/config/hotspotportal/HOTSPOT-PORTAL-ID'

    access_code = randomStringDigits(6)
    data = {'HotspotPortal':
                {'id': 'HOTSPOT-PORTAL-ID',
                 'name': 'HOTSPOT-PORTAL-NAME',
                 'settings':
                     {"aupSettings":
                          {"includeAup": 'true',
                           "requireAccessCode": 'true',
                           "accessCode": access_code,
                           "requireScrolling": 'false'
                           }
                      }
                 }
            }

    headers = {"Content-Type": "application/json"}
    response = requests.put(url, data=json.dumps(data), headers=headers, verify=False, auth=HTTPBasicAuth('ISE_USERNAME', 'ISE_PASSWORD'))
    send_email(access_code)
    return



if __name__ == "__main__":
    main()

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random


def send_email(recipient):
    import smtplib

    subject = 'Auth code'
    pwd = 'ZshilBylPes'
    user = 'hackatonmoscow@gmail.com'
    FROM = user
    TO = recipient
    SUBJECT = subject
    code = str(random.randint(100000, 999999))
    TEXT = 'Your code ' + code

    # Prepare actual message
    message = "\r\n".join([
        "From: " + FROM,
        "To: " + TO,
        "Subject: " + SUBJECT,
        "",
        TEXT
    ])
    # try:
    # SMTP_SSL Example
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo()  # optional, called by login()
    server_ssl.login(user, pwd)
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(FROM, TO, message)
    # server_ssl.quit()
    server_ssl.close()

    return code

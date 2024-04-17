# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains notifications methods to send mail to users.

# --------------------  Imports  --------------------

from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify
from application.logger import logger
from jinja2 import Template
from flask import render_template, request, redirect, flash, url_for
import pandas as pd
import requests
from datetime import datetime
import os
import json
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
from email.mime.application import MIMEApplication
from application.globals import *


# --------------------  Code  --------------------


notification_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Alert</title>
</head>
<body>
    {% if occasion == "REGISTER_OCCASION" %}
        <p>Dear {{ data['username'] }},</p>
        <p>&emsp;You are registered on Online Support Ticket System , and the admin will approve your account shortly.</p>
    {% elif occasion == "account_approval" %}
        <p>Dear {{ data['username'] }},</p>
        <p>&emsp;Your account is now active.</p>
        <p>&emsp;You can login Online Support Ticket System with the credentials by which you registered. <a href="http://localhost:8080/login">here</a>.</p>
        <p>&emsp;You can login on discourse <a href="http://localhost:4200">Discourse</a>.</p>
        <p>&emsp;Your Discourse account credentials are:</p>
        <p>&emsp;&emsp;Discourse Username: {{ data['discourse_username'] }}</p>
        <p>&emsp;&emsp;Discourse Password: {{ data['discourse_password'] }}</p>
        <p>&emsp;<i>please change your discourse password, this is dummy password.</i></p>
    {% elif occasion == "ticket_creation" %}
        <p>Dear {{ data['username'] }},</p>
        <p>&emsp;Your query has been registered with the ticket ID: <b>{{ data['ticket_id'] }}</b>.</p>
        <p>&emsp;Ticket Category: {{ data['ticket_category'] }}</p>
            <p>&emsp;You can view your public ticket on discourse <a href={{data['discourse_url']}}>here</a>.</p>
        <p>&emsp;You can also put additional comment on Online Support Ticket System after login.</p>
        <p><i>We will respond to you query in 2 days</i></p>
    {% elif occasion == "ticket_resolution" %}
        <p>Dear {{ data['username'] }},</p>
        <p>&emsp;Your ticket with ticket ID: <b>{{ data['ticket_id'] }}</b> has been resolved.</p>
        <p>&emsp;Please login to your account and verify the solution.</p>
        <p>&emsp;Feel free to comment on the ticket if you need additional help.</p>
    {% endif %}
    </br>
    <p>Regards,</p>
    <p>OSTS Support Team</p>
</body>
</html>
"""





def check_internet():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        return False


def _send_mail(to, _from, data, subject, occasion, content="html"):
    message = MIMEMultipart()
    message["From"] = _from
    message["To"] = to
    message["Date"] = formatdate(localtime=True)
    message["Subject"] = subject
    msg = Template(notification_template).render(occasion=occasion, data=data)
    message.attach(MIMEText(msg, content))

    try:
        smtp = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
        smtp.login(SENDER_ADDRESS, SENDER_PASSWORD)
    except Exception as e:
        logger.error(f"Error during mail sending: {e}")
    else:
        smtp.send_message(msg=message)
        smtp.quit()
        logger.info("Mail sent successfully")


def send_email(
    occasion="",
    to=[],
    _from="",
    subject="",
    data=None,
    content="html"
):
    for user in to:
        if check_internet():
            # html_content = render_template('notification_template.html', data=data)
            _send_mail(
                to=user["email"],
                _from=_from,
                data=data,
                subject=subject,
                occasion=occasion,
                content=content
            )
        else:
            logger.error("No internet connection to send mail")




















# def check_internet():
#     try:
#         socket.create_connection(("1.1.1.1", 53))
#         return True
#     except OSError:
#         return False


# def _send_mail(to, _from, data, subject, content="html"):
#     message = MIMEMultipart()
#     message["From"] = SENDER_ADDRESS  # _from
#     message["To"] = to
#     message["Date"] = formatdate(localtime=True)
#     message["Subject"] = subject
#     msg = Template(notification_template).render(data=data)
#     message.attach(MIMEText(msg, content))

#     try:
#         # smtp = smtplib.SMTP('smtp.gmail.com', 587) # to actual mail address
#         smtp = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)  # to mailhog
#         smtp.login(SENDER_ADDRESS, SENDER_PASSWORD)
#     except Exception as e:
#         logger.error(f"Error during mail sending: {e}")
#     else:
#         smtp.send_message(msg=message)
#         smtp.quit()
#         logger.info(f"Mail sent successfully")


# def send_email(
#     to=[],
#     _from="",
#     sub="",
# ):
#     for user in to:
#         if check_internet():
#             _send_mail(
#                 user["email"],
#                 _from,
#                 data={"username": user["first_name"], "ticket_id": user["ticket_id"]},
#                 subject=sub,
#                 content="html",
#             )
#         else:
#             logger.error("No internet connection to send mail")


# --------------------  END  --------------------

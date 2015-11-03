#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from lib.send_mail import *
from lib.trello_lib import *

def build_message_text(data):
    intro = data["intro"]
    backend = data["backend"]
    outro = data["outro"]

    full_message = "{}{}{}".format(intro, backend, outro)
    return full_message

def send_email():
    con = Config()
    to_address = raw_input("What is the email address of the company?:")

    company = raw_input("What's the name of the company?:")
    title = raw_input("What's the job title?:")
    description = raw_input("""I am passionate about helping businesses use \
data to understand how to better their products for customers:""")
    personal_message = raw_input("Leave a personal message:")
    message = con.message(company, title, description, personal_message)
    print "data: ", message
    message_text =  build_message_text(message)
    sender = message["from_address"]
    to = to_address
    name = message["name"]
    subject = "{} at {} ({})".format(title, company, name)

    #Message = CreateMessage(sender, to, subject, message_text)
    #testSend = SendMessage(service, 'me', Message)

    return message_text

print send_email()

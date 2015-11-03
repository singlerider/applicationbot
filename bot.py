#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from lib.send_mail import *
from lib.trello_lib import *

con = Config()

def build_message_text(data):
    intro = data["intro"]
    backend = data["backend"]
    outro = data["outro"]
    full_message = "{}{}{}".format(intro, backend, outro)
    return full_message


def update_trello(data, company):
    board_id = data["trello_board"]
    list_id = data["trello_applied"]
    trello_key = data["trello_key"]
    trello_token = data["trello_token"]
    card_name = "{}. {}".format((len(get_cards(board_id, trello_key,
        trello_token)) + 1), company)
    return insert_card(board_id, list_id, card_name, company, trello_key,
        trello_token)


def send_email():
    to_address = raw_input("What is the email address of the company?:")
    company = raw_input("What's the name of the company?:")
    title = raw_input("What's the job title?:")
    description = raw_input("""I am passionate about helping businesses use \
data to understand how to better their products for customers:""")
    personal_message = raw_input("Leave a personal message:")
    data = con.message(company, title, description, personal_message)
    print "data: ", data
    message_text =  build_message_text(data)
    sender = data["from_address"]
    to = to_address
    name = data["name"]
    subject = "{} at {} ({})".format(title, company, name)
    message = CreateMessage(sender, to, subject, message_text)
    send = SendMessage(service, 'me', message)

    update_trello(data, company)
    return message_text


print send_email()

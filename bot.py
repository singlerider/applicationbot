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
    resume = data["resume"]
    full_message = "{}{}{}\n\nResume Link: {}".format(intro, backend, outro,
        resume)
    return full_message

def save_cover_letter(company, message_text):
    with open('cover_letters/{}_cover_letter.txt'.format(company.replace(" ", "_").lower()), 'w') as f:
        f.write(message_text)

def update_trello(data, company):
    board_id = data["trello_board"]
    list_id = data["trello_applied"]
    trello_key = data["trello_key"]
    trello_token = data["trello_token"]
    card_name = "{}. {}".format((len(get_cards(board_id, trello_key,
        trello_token)) + 1), company)
    return insert_card(board_id, list_id, card_name, company, trello_key,
        trello_token)


def send_email(to_address, company, title, description, personal_message, message_text):
    sender = data["from_address"]
    to = to_address
    name = data["name"]
    subject = "{} at {} ({})".format(title, company, name)
    #message = CreateMessage(sender, to, subject, message_text)
    #send = SendMessage(service, 'me', message)
    print message_text


def main(intialize):
    company = raw_input("What's the name of the company?:")
    title = raw_input("What's the job title?:")
    description = raw_input("""I am passionate about helping businesses use \
data to understand how to better their products for customers:""")
    personal_message = raw_input("Leave a personal message:")
    data = con.message(company, title, description, personal_message)
    print "data: ", data
    message_text =  build_message_text(data)
    print message_text
    if "y" in initialize[0].lower():
        to_address = raw_input("What is the email address of the company?:")
        send_email(to_address, company, title, description, personal_message,
            message_text)
    if "y" in initialize[1].lower():
        update_trello(data, company)
    save_cover_letter(company, message_text)


if __name__ == "__main__":
    initialize = raw_input("Are you sending an email?:"), raw_input("Are you updating your Trello?:")
    main(initialize)

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
    full_message = "{}{}{}".format(intro, backend, outro)
    return full_message


def save_cover_letter(company, message_text):
    with open('cover_letters/{}_cover_letter.txt'.format(company.replace(" ", "_").lower()), 'w') as f:
        f.write(message_text)


def update_trello(data, company, message_text):
    board_id = data["trello_board"]
    list_id = data["trello_applied"]
    trello_key = data["trello_key"]
    trello_token = data["trello_token"]
    card_number = len(get_cards(board_id, trello_key, trello_token))
    card_name = "{}. {}".format((card_number + 1), company)
    insert_card(board_id, list_id, card_name, company, trello_key, trello_token)
    insert_comment(card_number, message_text, trello_key, trello_token)
    print "Trello Updated"


def send_email(data, to_address, company, title, description, personal_message, message_text):
    sender = data["from_address"]
    to = to_address
    name = data["name"]
    # LASTNAME_FIRSTNAMEResume.pdf in your root dir
    filename = [name.split()[1] + "_" +  name.split()[0]][0].upper() + "Resume.pdf"
    subject = "{} at {} ({})".format(title, company, name)
    # uncomment line below to send an email WITH an attachment (your resume)
    message = CreateMessageWithAttachment(sender, to, subject, message_text, '', filename)
    # uncomment line below to send email WITHOUT an attachment
    #message = CreateMessage(sender, to, subject, message_text)
    send = SendMessage(service, 'me', message)


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
        send_email(data, to_address, company, title, description, personal_message,
            message_text)
    if "y" in initialize[1].lower():
        update_trello(data, company, message_taxt)
    save_cover_letter(company, message_text)


if __name__ == "__main__":
    initialize = raw_input("Are you sending an email?:"), raw_input("Are you updating your Trello?:")
    main(initialize)

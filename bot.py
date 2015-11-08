#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from lib.send_mail import *
from lib.trello_lib import *
import lib.scrape_craigslist
import lib.scrape_indeed

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


def update_trello(data, message_text):
    board_id = data["trello_board"]
    list_id = data["trello_applied"]
    trello_key = data["trello_key"]
    trello_token = data["trello_token"]
    desc = data["listing"]
    company = data["company"]
    card_number = len(get_cards(board_id, trello_key, trello_token)) + 1
    card_name = "{}. {}".format((card_number), company)
    insert_card(board_id, list_id, card_name, company, trello_key, trello_token)
    cards_info = get_cards(board_id, trello_key, trello_token)
    card_id = [x["id"] for x in cards_info if str(card_number) + "." in x["name"]][0]
    insert_comment(card_id, message_text, trello_key, trello_token)
    edit_description(card_id, desc, trello_key, trello_token)
    print "Trello Updated"


def send_email(data, to_address, title, message_text):
    sender = data["from_address"]
    name = data["name"]
    # LASTNAME_FIRSTNAMEResume.pdf in your root dir
    filename = [name.split()[1] + "_" +  name.split()[0]][0].upper() + "Resume.pdf"
    subject = "{} Job Posting ({})".format(title, name)
    # uncomment line below to send an email WITH an attachment (your resume)
    message = CreateMessageWithAttachment(sender, to_address, subject, message_text, '', filename)
    # uncomment line below to send email WITHOUT an attachment
    #message = CreateMessage(sender, to, subject, message_text)
    send = SendMessage(service, 'me', message, to_address)


def main(intialize):
    company = raw_input("What's the name of the company?:")
    title = raw_input("What's the job title?:")
    description = raw_input("""I am passionate about helping businesses use \
data to understand how to better their products for customers:""")
    personal_message = raw_input("Leave a personal message:")
    data = con.message(company, title, description, personal_message)
    data["initialize"] = initialize
    data["title"] = ' '.join([x.capitalize() for x in title.split()]) # ex: Python Engineer from python engineer
    data["personal_message"] = personal_message
    data["listing"] = " " # empty description by default - job listing will go here
    data["company"] = company
    print "data: ", data
    message_text =  build_message_text(data)
    print message_text
    if "y" in initialize[0] and "y" not in initialize[2]:
        to_address = raw_input("What is the email address of the company?:")
        send_email(data, to_address, title, message_text)
    if "y" in initialize[1] and "y" not in initialize[2]:
        update_trello(data, message_text)
    save_cover_letter(company, message_text)
    if "y" in initialize[2]:
        scrape_craigslist.scrape_and_apply(data, message_data)
    print "All done"


if __name__ == "__main__":
    sending_email = raw_input("Are you only sending an email?:").lower()
    updating_trello = raw_input("Are you only updating your Trello?:").lower()
    web_scraping = raw_input("Will you be web scraping?:").lower()
    initialize = sending_email, updating_trello, web_scraping
    main(initialize)

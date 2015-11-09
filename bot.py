#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
import lib.scrape_craigslist as craigslist
import lib.scrape_indeed
from lib.helpers import *

con = Config()

def main(intialize):
    if "y" in initialize[0] and "y" not in initialize[2]:
        company = raw_input("What's the name of the company?:")
    else:
        company = " "
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
    #print "data: ", data
    message_text =  build_message_text(data)
    print message_text
    if "y" in initialize[0] and "y" not in initialize[2]:
        to_address = raw_input("What is the email address of the company?:")
        send_email(data, to_address, title, message_text)
    if "y" in initialize[1] and "y" not in initialize[2]:
        update_trello(data, message_text)
    save_cover_letter(company, message_text)
    if "y" in initialize[2]:
        craigslist.scrape_and_apply(data)
    print "All done"


if __name__ == "__main__":
    sending_email = raw_input("Are you sending an email?:").lower()
    updating_trello = raw_input("Are you updating your Trello?:").lower()
    web_scraping = raw_input("Will you be web scraping?:").lower()
    initialize = sending_email, updating_trello, web_scraping
    main(initialize)

# -*- coding: utf-8 -*-

class Config(object):

    def message(self, company, title, description, personal_message):
        self.company = company
        self.title = title
        self.description = description
        self.personal_message = personal_message

        name = "YOURNAME"

        trello_key = ""
        trello_secret = ""
        trello_token = "" # get this by going here and replacing YOURAPIKEY:
        # https://trello.com/1/authorize?key=YOURAPIKEY&name=My+App&expiration=30days&response_type=token&scope=read,write
        trello_board = "" # Your job board!
        trello_applied = "" # The ID for your "Applied" list on your job board

        from_address = "YOUR AUTHENTICATED EMAIL ADDRESS"
        phone_number = "YOUR PHONE NUMBER"

        intro = """Hi {0}, \n
I'm an Engineer engineer and I'm really excited to apply for the \
{1} role at {0}. I am passionate about helping businesses use data to \
understand how to better their products for customers {2}. I believe that {0} \
is a place where I can contribute to success of the software engineering team \
from day one.""".format(self.company, self.title, self.description)
        backend = """ \n
As a backend software engineer at COMPANY NAME with a \
team of three engineers, \
"""
        outro = """\n
I am passionate about applying my software development skills to help move \
{0} forward. I can be reached at {2} or on my cell at {3}. \
{1}\n
Best Wishes,\n
{4}""".format(self.company, self.personal_message, from_address, phone_number, name)

        data = {
            "trello_key": trello_key,
            "trello_secret": trello_secret,
            "trell_token": trello_token,
            "trello_board": trello_board,
            "trello_applied": trello_applied,
            "from_address": from_address,
            "phone_number": phone_number,
            "company": self.company,
            "title": self.title,
            "description": self.description,
            "personal_message": self.personal_message,
            "name": name,
            "intro": intro,
            "backend": backend,
            "outro": outro
        }

        return data

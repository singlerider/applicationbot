# -*- coding: utf-8 -*-

from_address = "yourauthenticatedemailaddress"
to_address = raw_input("What is the email address of the company?:")
company = raw_input("What's the name of the company?:")
title = raw_input("What's the job title?:")
description = raw_input("""I am passionate about helping businesses use data \
to understand how to better their products for customers:""")
personal_message = raw_input("Leave a personal message:")

intro = """
Hi {0}, \n
{1}{0}{2}{0}\
""".format(company, title, description)
backend = """\n
As a backend software engineer..."""
outro = """\n
{0} I can be reached at. {1}\n
Best Wishes,\n
Your Name""".format(company, personal_message)

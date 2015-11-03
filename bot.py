#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
from lib.send_mail import *

def build_message_text():
    full_message = "{}{}{}".format(intro, backend, outro)
    return full_message

sender = from_address
to = to_address
subject = "{} at {} ({})".format(title, company, name)
message_text = build_message_text()

print message_text

Message = CreateMessage(sender, to, subject, message_text)
testSend = SendMessage(service, 'me', Message)

#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from config import *
from lib.send_mail import *

sender = email_address
to = "haroboy876@gmail.com"
subject = "test"
message_text = personal_message.encode('utf-8')

Message = CreateMessage(sender, to, subject, message_text)
testSend = SendMessage(service, 'me', Message)

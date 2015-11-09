from lib.send_mail import *
from lib.trello_lib import *

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

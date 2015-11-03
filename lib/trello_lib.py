import requests
import json
from config import *

# The way the API organizes card information isn't ideal for quick id-ing
# Let's convert it to a nice dict with the list_name: list_id
def get_job_board(board_id):
    url = "https://api.trello.com/1/boards/{}?lists=open&list_fields=name&\
fields=name,desc&key={}&token={}".format(board_id, trello_key, trello_token)
    resp = requests.get(url=url)
    data = json.loads(resp.content)
    applied = data["lists"][[x for x in range(len(data["lists"])) if data["lists"][x]["name"] == "Applied" ][0]]["id"]
    completed = data["lists"][[x for x in range(len(data["lists"])) if data["lists"][x]["name"] == "Completed" ][0]]["id"]
    phone_screens = data["lists"][[x for x in range(len(data["lists"])) if data["lists"][x]["name"] == "Phone Screens" ][0]]["id"]
    code_challenges = data["lists"][[x for x in range(len(data["lists"])) if data["lists"][x]["name"] == "Code Challenges" ][0]]["id"]
    technical_screens = data["lists"][[x for x in range(len(data["lists"])) if data["lists"][x]["name"] == "Technical Screens" ][0]]["id"]
    on_sites = data["lists"][[x for x in range(len(data["lists"])) if data["lists"][x]["name"] == "On Sites" ][0]]["id"]
    offers = data["lists"][[x for x in range(len(data["lists"])) if data["lists"][x]["name"] == "Offers" ][0]]["id"]
    lists = {
        "applied": applied,
        "completed": completed,
        "phone_screens": phone_screens,
        "code_challenges": code_challenges,
        "technical_screens": technical_screens,
        "on_sites": on_sites,
        "offers": offers
    }
    return lists

# To increment the number of jobs applied to, add the length of the result of
# the below function plus one
def get_cards(board_id):
    url = "https://api.trello.com/1/boards/{}/cards?key={}&token={}".format(board_id,
        trello_key, trello_token)
    resp = requests.get(url=url)
    data = json.loads(resp.content)
    return data

def insert_card(list_id, card_name):
    url = "https://api.trello.com/1/lists/{}/cards?name={}&key={}&token={}".format(
        list_id, card_name, trello_key, trello_token)
    resp = requests.post(url=url)
    data = json.loads(resp.content)
    return data

card_name = "{}. Hey, David. This card was inserted automatically by my bot".format((len(get_cards(trello_board)) + 1))
print insert_card(trello_applied, card_name)

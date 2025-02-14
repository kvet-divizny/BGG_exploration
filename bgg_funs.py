import requests
from dataclasses import dataclass
from typing import Optional
from xml.etree import ElementTree
from datetime import datetime, time
import time

@dataclass
class Game():
    id: int
    name: str
    weight: Optional[float] = None

@dataclass
class ColItem():
    id: int
    name: str
    numplays: int
    userrating: int
    owned: bool
    want: bool
    wanttoplay: bool
    wanttobuy: bool
    wishlist: bool

def to_int(str):
    if str.isdigit():
        i = int(str)
    else:
        i = None

    return i
    

def check_response(resp):
    if resp.status_code:
        print(f"{datetime.now().time()}: OK response for {resp.url}.")
        return True
    else:
        print(f"{datetime.now().time()}: The response is not OK -- {resp.status_code}")

def req_collection(username):
    base_url = "https://boardgamegeek.com/xmlapi2/collection"
    payload = {
        "username": username,
        "subtype": "boardgame",
        "stats": 1        
    }

    status_code = 0
    pause = 2
    while status_code != 200:
        r = requests.get(url=base_url, params=payload)
        status_code = r.status_code
        print(status_code)
        time.sleep(pause)
        pause = pause * 1.5

    return r

def parse_collection(node):
    status = node.find("status")
    item = ColItem(
        id = to_int(node.get("objectid")),
        name = node.find("name").text,
        numplays = to_int(node.find("numplays").text),
        userrating = to_int(node.find("stats/rating").get("value")),
        owned = status.get("own"),
        want = status.get("want"),
        wanttoplay = status.get("wanttoplay"),
        wanttobuy = status.get("wanttobuy"),
        wishlist = status.get("wishlist")
    )
    return(item)
   
def req_games(gameid):
    base_url = "https://boardgamegeek.com/xmlapi2/thing"
    payload = {
        "id": gameid,
        "stats": 1,
    }

    r = requests.get(url = base_url, params=payload)
    check_response(r)

    # print(r.url)
    # print(r.status_code)
    return r
    
def parse_response(node):
    game = Game(
        id = node.get("id"),
        name = node.find("name").get("value"),
        weight = float(node.find("statistics/ratings/averageweight").get("value"))
    )
    return game

def main(id):
    # id = "311715,355326"
    games = []

    resp = req_games(id)
    tree = ElementTree.fromstring(resp.content)

    for node in tree:
        game = parse_response(node)
        games.append(game)

    return games


if __name__ == "__main__":
    resp = req_collection("baninka")
    tree = ElementTree.fromstring(resp.content)

    for node in tree:
        parse_collection(node)

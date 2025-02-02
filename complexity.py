import requests
from dataclasses import dataclass
from typing import Optional
from xml.etree import ElementTree

@dataclass
class Game():
    id: int
    name: str
    weight: Optional[float] = None

def req_games(gameid):
    base_url = "https://boardgamegeek.com/xmlapi2/thing"
    payload = {
        "id": gameid,
        "stats": 1,
    }

    r = requests.get(url = base_url, params=payload)

    # print(r.url)
    # print(r.status_code)
    return r
    
def parse_response(node):
    game = Game(
        id = node.get("id"),
        name = node.find("name").get("value"),
        weight = node.find("statistics/ratings/averageweight").get("value")
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
    main()

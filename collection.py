import bgg_funs as bf
from xml.etree import ElementTree


user = "baninka"

col_resp = bf.req_collection(user)

tree = ElementTree.fromstring(col_resp.content)

collection = []

for node in tree:
    item = bf.parse_collection(node)
    collection.append(item)

N = 20

ids = [item.id for item in collection]
ids_chunks = [ids[i:i+N] for i in range(0, len(ids), N)]

col_games = []
for chunk in ids_chunks:
    game_ids = ', '.join(map(str, chunk))
    chunk_data = bf.main(game_ids)
    col_games.extend(chunk_data)

print(col_games)


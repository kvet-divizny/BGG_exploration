import polars as pl
import complexity
from time import sleep, strftime

db_csv = pl.read_csv("data/boardgames_ranks.csv")

game_ids = db_csv.select(
    pl.col("id")
)

N = 20
ids_iter = [iter(db_csv["id"])] * N
ids_chunks = list(zip(*ids_iter))

chunks = []

for chunk in ids_chunks:
    chunk_text = ','.join(map(str, chunk))
    chunks.append(chunk_text)

ids = []
names = []
weights = []

for chunk in chunks:
    chunk_data = complexity.main(chunk)

    for game in chunk_data:
        ids.append(game.id)
        names.append(game.name)
        weights.append(game.weight)

    print(f"{strftime('%H:%M:%S')}: fetching another 20 games...")
    sleep(1.5)


game_df = pl.DataFrame({
    "id": ids,
    "name": names,
    "weight": weights
})

game_df.write_csv("data/games_weights.csv", separator=";")
print(f"{strftime("%H:%M:%S")}: all games fetched!!!")

# game_weight = 3.3

# weight_rank = len(game_df.filter(pl.col("weight") <= game_weight)) / len(game_df)

# print(weight_rank)

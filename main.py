import polars as pl
import complexity

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

for chunk in chunks[0:5]:
    chunk_data = complexity.main(chunk)

    for game in chunk_data:
        ids.append(game.id)
        names.append(game.name)
        weights.append(game.weight)

game_df = pl.DataFrame({
    "id": ids,
    "name": names,
    "weight": weights
})

print(game_df.head)
# print(game_data)
# print(len(db_csv))

import pandas as pd
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

#Load and clean CSV
print("Loading data from test_items.csv...")
df = pd.read_csv("data/test_items.csv")  #my csvfilename

#Fill missing values if any
df["title"] = df["title"].fillna("")
df["description"] = df["description"].fillna("")

#Create a unified text input for embedding
df["combined"] = df["title"] + ". " + df["description"]

#Load embedding model
print("Loading SentenceTransformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

if model.device.type == "cuda":
    print(f"Using GPU: {model.device}")
else:
    print(f"Using CPU: {model.device}")

#Generate embeddings
print("⚙️ Generating embeddings...")
embeddings = model.encode(
    df["combined"].tolist(),
    show_progress_bar=True,
    batch_size=64
)

#Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "items"
VECTOR_SIZE = 384  # 'all-MiniLM-L6-v2' embedding size

#Recreate collection
print(f"Recreating Qdrant collection: '{COLLECTION_NAME}'")
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
)

#Upload to Qdrant
BATCH_SIZE = 256
print("Uploading vectors to Qdrant...")

for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Uploading"):
    batch = df.iloc[i:i + BATCH_SIZE]
    batch_embeddings = embeddings[i:i + BATCH_SIZE]

    points = [
        PointStruct(
            id=int(row.item_id),
            vector=embedding.tolist(),
            payload={
                "item_id": int(row.item_id),
                "title": row.title,
                "description": row.description
            }
        )
        for row, embedding in zip(batch.itertuples(index=False), batch_embeddings)
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)

print("Embeddings uploaded to Qdrant.")

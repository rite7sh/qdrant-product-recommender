from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

# Scroll through a few stored vectors to inspect the payloads
results, _ = client.scroll(
    collection_name="items",
    limit=5
)

for point in results:
    print(point.id, point.payload)

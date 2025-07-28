from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

# Scroll through items
response = client.scroll(
    collection_name="items",
    limit=5,
    with_payload=True  # include title/description
)

for point in response[0]:
    print(f"ID: {point.id}, Payload: {point.payload}")

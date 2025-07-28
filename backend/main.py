from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "items"

#Initialize FastAPI
app = FastAPI(title="Product Recommender API 🚀")

#Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Load sentence-transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

#Connect to Qdrant
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": " Backend is running"}

@app.get("/items", tags=["Items"])
def list_all_items():
    """
    Return a list of all items from Qdrant (for dropdowns or initial UI load).
    """
    scroll = client.scroll(
        collection_name=COLLECTION_NAME,
        with_payload=True,
        limit=100  #increase if needed
    )

    return {
        "items": [
            {
                "item_id": point.payload.get("item_id"),
                "title": point.payload.get("title"),
                "description": point.payload.get("description")
            }
            for point in scroll[0]
        ]
    }

@app.get("/recommend", tags=["Recommendation"])
def recommend(
    item_id: int = Query(..., description="The item ID to find similar items for"),
    top_k: int = Query(5, description="Number of similar items to return")
):
    """
    Recommend similar items based on a given item ID.
    """
    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="item_id",
                    match=models.MatchValue(value=item_id)
                )
            ]
        ),
        with_vectors=True,
        limit=1
    )

    if not scroll_result or not scroll_result[0]:
        raise HTTPException(status_code=404, detail="Item ID not found")

    point = scroll_result[0][0]
    query_vector = point.vector

    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k + 1
    )

    recommendations = []
    for hit in hits:
        if hit.payload.get("item_id") != item_id:
            recommendations.append({
                "id": hit.id,
                "score": hit.score,
                "item_id": hit.payload.get("item_id"),
                "title": hit.payload.get("title"),
                "description": hit.payload.get("description")
            })
        if len(recommendations) == top_k:
            break

    return {
        "query_item_id": item_id,
        "recommendations": recommendations
    }

@app.get("/search", tags=["Semantic Search"])
def search(
    query: str = Query(..., description="Enter a product-related query, like 'shoes for gym'"),
    top_k: int = Query(5, description="Number of relevant products to return")
):
    """
    Perform semantic search on the products based on a natural language query.
    """
    query_vector = model.encode(query).tolist()

    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )

    results = []
    for hit in hits:
        results.append({
            "id": hit.id,
            "score": hit.score,
            "item_id": hit.payload.get("item_id"),
            "title": hit.payload.get("title"),
            "description": hit.payload.get("description")
        })

    return {
        "query": query,
        "results": results
    }

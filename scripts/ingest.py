import csv
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()

COLLECTION = "products"
EMBEDDING_MODEL = "all-mini-lm-l6-v2"
VECTOR_SIZE = 384
BATCH_SIZE = 32
CSV_PATH = Path(__file__).parent.parent / "data" / "products.csv"

openai_client = OpenAI(
    api_key=os.getenv("DO_INFERENCE_API_KEY"),
    base_url=os.getenv("DO_INFERENCE_BASE_URL"),
)

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)


def embed_batch(texts: list[str]) -> list[list[float]]:
    resp = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def setup_collection() -> None:
    existing = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION in existing:
        print(f"Collection '{COLLECTION}' already exists — deleting and recreating.")
        qdrant.delete_collection(COLLECTION)

    qdrant.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print(f"Collection '{COLLECTION}' created.")


def load_csv() -> list[dict]:
    rows = []
    with open(CSV_PATH, newline="") as f:
        for i, row in enumerate(csv.reader(f)):
            if len(row) < 2:
                continue
            rows.append({
                "id": i + 1,
                "product_id": row[0].strip(),
                "name": row[1].strip(),
                "description": row[2].strip() if len(row) > 2 else "",
            })
    return rows


def ingest() -> None:
    print(f"Reading products from {CSV_PATH}")
    products = load_csv()
    print(f"Loaded {len(products)} products.")

    setup_collection()

    total = 0
    for i in range(0, len(products), BATCH_SIZE):
        batch = products[i : i + BATCH_SIZE]
        texts = [f"{p['name']}. {p['description']}" for p in batch]

        vectors = embed_batch(texts)

        points = [
            PointStruct(
                id=p["id"],
                vector=v,
                payload={
                    "product_id": p["product_id"],
                    "name": p["name"],
                    "description": p["description"],
                },
            )
            for p, v in zip(batch, vectors)
        ]

        qdrant.upsert(collection_name=COLLECTION, points=points)
        total += len(batch)
        print(f"  Ingested {total}/{len(products)} products...")

        time.sleep(0.2)

    print(f"\nDone. {total} products ingested into '{COLLECTION}'.")


if __name__ == "__main__":
    ingest()

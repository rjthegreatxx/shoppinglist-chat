import argparse
import csv
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()

sys_path = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(sys_path))

from app.config import settings

BATCH_SIZE = 32
MAX_RETRIES = 3
CSV_PATH = Path(__file__).parent.parent / "data" / "products.csv"

openai_client = OpenAI(
    api_key=settings.do_inference_api_key,
    base_url=settings.do_inference_base_url,
)

qdrant = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key,
)


def embed_batch(texts: list[str]) -> list[list[float]]:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = openai_client.embeddings.create(
                model=settings.embedding_model,
                input=texts,
            )
            return [d.embedding for d in resp.data]
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise
            wait = 2 ** attempt
            print(f"  Embed attempt {attempt} failed ({e}), retrying in {wait}s...")
            time.sleep(wait)
    return []


def setup_collection(recreate: bool) -> None:
    existing = [c.name for c in qdrant.get_collections().collections]
    if settings.qdrant_collection in existing:
        if not recreate:
            print(f"Collection '{settings.qdrant_collection}' exists — upserting without recreating. Use --recreate to wipe first.")
            return
        print(f"Collection '{settings.qdrant_collection}' exists — deleting and recreating.")
        qdrant.delete_collection(settings.qdrant_collection)

    qdrant.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=VectorParams(
            size=settings.embedding_dimensions,
            distance=Distance.COSINE,
        ),
    )
    print(f"Collection '{settings.qdrant_collection}' created.")


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


def ingest(recreate: bool) -> None:
    print(f"Reading products from {CSV_PATH}")
    products = load_csv()
    print(f"Loaded {len(products)} products.")

    setup_collection(recreate)

    total = 0
    failed = 0
    for i in range(0, len(products), BATCH_SIZE):
        batch = products[i : i + BATCH_SIZE]
        texts = [f"{p['name']}. {p['description']}" for p in batch]

        try:
            vectors = embed_batch(texts)
        except Exception as e:
            print(f"  Skipping batch {i}-{i+len(batch)}: embed failed after {MAX_RETRIES} retries — {e}")
            failed += len(batch)
            continue

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

        qdrant.upsert(collection_name=settings.qdrant_collection, points=points)
        total += len(batch)
        print(f"  Ingested {total}/{len(products)} products...")

        # Avoid hitting rate limits
        time.sleep(0.2)

    print(f"\nDone. {total} ingested, {failed} failed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest product catalog into Qdrant.")
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete and recreate the collection before ingesting.",
    )
    args = parser.parse_args()
    ingest(recreate=args.recreate)

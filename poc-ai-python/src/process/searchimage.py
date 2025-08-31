import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
from PIL import Image
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
from src.database.database import get_db_connection

print("Loading CLIP model...")
model = SentenceTransformer('clip-ViT-B-32')


# --- 4. Search Function: Find the best match in the DB ---
def search_images(text_query):
    with get_db_connection() as conn:
        # This is crucial to make psycopg2 understand the VECTOR type
        register_vector(conn)

        with conn.cursor() as cur:
            print(f"\nSearching for: '{text_query}'")

            # Generate the embedding for the text query
            text_embedding = model.encode(text_query, convert_to_numpy=True)

            # Perform the similarity search in PostgreSQL
            # The '<=>' operator calculates the cosine distance (0=identical, 2=opposite)
            cur.execute(
                """
                SELECT uuid, 1 - (embedding <=> %s) AS similarity_score
                FROM images
                ORDER BY embedding <=> %s
                LIMIT 10;
                """,
                (text_embedding, text_embedding)
            )

            results = cur.fetchall()

            for uuid, score in results:
              print(f"UUID: {uuid}, Score: {score}")

            # if result:
            #     best_matching_image, best_match_score = result
            #     print(f"\nBest match found: {best_matching_image}")
            #     print(f"Cosine Similarity Score: {best_match_score:.4f}")
            # else:
            #     print("No results found.")

# --- 5. Main Execution Block ---
if __name__ == "__main__":
    # First, ensure all images are indexed in the database
    # index_images()

    # Then, start the search prompt
    user_query = input("\nEnter your search query: ")
    search_images(user_query)
import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
from PIL import Image

# --- 1. Load Model & Prepare Image List ---
print("Loading CLIP model...")
model = SentenceTransformer('clip-ViT-B-32')

image_names = ['image1.png', 'image2.png', 'image3.png', 'image4.png',
               'image5.png', 'image6.png', 'image7.png', 'image8.png',
               'image9.png', 'image10.png', 'image11.png', 'image12.png',
               'image14.png', 'image15.png']

# --- 2. Database Connection Details ---
# Replace with your actual credentials
db_params = {
    "host": "localhost",
    "port": "5432",
    "database": "mydb",
    "user": "user",
    "password": "password"
}

# --- 3. Indexing Function: Store images and embeddings in DB ---
def index_images():
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            register_vector(conn)
            # Create the table if it doesn't exist
            # The vector(512) corresponds to the CLIP model's output dimension
            cur.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255) UNIQUE,
                    embedding VECTOR(512)
                );
            """)
            print(f"Generating and indexing embeddings for {len(image_names)} images...")

            # Generate embeddings
            image_embeddings = model.encode(
                [Image.open(filepath).convert("RGB") for filepath in image_names],
                convert_to_numpy=True # pgvector works best with numpy arrays
            )

            # Insert or update data in the table
            for filename, embedding in zip(image_names, image_embeddings):
                cur.execute(
                    """
                    INSERT INTO images (filename, embedding) 
                    VALUES (%s, %s)
                    ON CONFLICT (filename) DO UPDATE 
                    SET embedding = EXCLUDED.embedding;
                    """,
                    (filename, embedding)
                )
            print("Indexing complete.")

# --- 4. Search Function: Find the best match in the DB ---
def search_images(text_query):
    with psycopg2.connect(**db_params) as conn:
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
                SELECT filename, 1 - (embedding <=> %s) AS similarity_score
                FROM images
                ORDER BY embedding <=> %s
                LIMIT 1;
                """,
                (text_embedding, text_embedding)
            )

            result = cur.fetchone()

            if result:
                best_matching_image, best_match_score = result
                print(f"\nBest match found: {best_matching_image}")
                print(f"Cosine Similarity Score: {best_match_score:.4f}")
            else:
                print("No results found.")

# --- 5. Main Execution Block ---
if __name__ == "__main__":
    # First, ensure all images are indexed in the database
    # index_images()

    # Then, start the search prompt
    user_query = input("\nEnter your search query: ")
    search_images(user_query)
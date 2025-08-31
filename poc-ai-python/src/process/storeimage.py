import psycopg2
import numpy as np
import requests
import io
import os
import sys

from torch.fx.experimental.unification.unification_tools import get_in

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
from PIL import Image
from torch.nn.functional import embedding

from src.database.database import get_db_connection
from src.database.mysql.mysqldatabase import get_mysql_db_connection

# --- 1. Load Model & Prepare Image List ---
print("Loading CLIP model...")
model = SentenceTransformer('clip-ViT-B-32')

image_names = ['image1.png', 'image2.png', 'image3.png', 'image4.png',
               'image5.png', 'image6.png', 'image7.png', 'image8.png',
               'image9.png', 'image10.png', 'image11.png', 'image12.png',
               'image14.png', 'image15.png']

# def image_to_embedding(image_url):
#     """
#     Converts an image file to an embedding vector using the CLIP model.
#     """
#     try:
#         # 1. Fetch the image data from the URL
#         print(f"Fetching image from: {image_url}")
#         response = requests.get(image_url)
#         # # Raise an exception if the request was unsuccessful
#         # response.raise_for_status()
#
#         # 2. Open the image from the in-memory bytes
#         # response.content contains the raw binary data of the image
#         image_bytes = io.BytesIO(response.content)
#         image = Image.open(image_bytes).convert("RGB")
#
#         # Generate the embedding
#         print(f"Generating embedding for {image_url}...")
#         embedding = model.encode(image, convert_to_numpy=True)
#         return embedding
#
#     except Exception as e:
#         print(f"An error occurred while processing {image_url}: {e}")
#         return None
#
# def store_image(id, embedding):
#     with get_db_connection() as conn:
#         with conn.cursor() as cur:
#             register_vector(conn)
#             cur.execute(
#                 """
#                 INSERT INTO images (filename, embedding)
#                 VALUES (%s, %s)
#                 ON CONFLICT (id) DO UPDATE
#                 SET embedding = EXCLUDED.embedding;
#                 """,
#                 (id, embedding)
#             )
#             print(f"Stored image with ID: {id}")
#             conn.commit()

def store_vectorized_image(uuid, embeddings):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            register_vector(conn)

            cur.execute(
                    """
                    INSERT INTO images (uuid, embedding)
                    VALUES (%s, %s)
                    ON CONFLICT (uuid) DO UPDATE
                    SET embedding = EXCLUDED.embedding;
                    """,
                    (uuid, embeddings)
                )
            conn.commit()

# --- 3. Indexing Function: Store images and embeddings in DB ---
# def index_images():
#     with get_db_connection() as conn:
#         with conn.cursor() as cur:
#             register_vector(conn)
#             # Create the table if it doesn't exist
#             # The vector(512) corresponds to the CLIP model's output dimension
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS images (
#                     id SERIAL PRIMARY KEY,
#                     filename VARCHAR(255) UNIQUE,
#                     embedding VECTOR(512)
#                 );
#             """)
#             print(f"Generating and indexing embeddings for {len(image_names)} images...")
#
#             # Generate embeddings
#             image_embeddings = model.encode(
#                 [Image.open(filepath).convert("RGB") for filepath in image_names],
#                 convert_to_numpy=True # pgvector works best with numpy arrays
#             )
#
#             # Insert or update data in the table
#             for filename, embedding in zip(image_names, image_embeddings):
#                 cur.execute(
#                     """
#                     INSERT INTO images (filename, embedding)
#                     VALUES (%s, %s)
#                     ON CONFLICT (filename) DO UPDATE
#                     SET embedding = EXCLUDED.embedding;
#                     """,
#                     (filename, embedding)
#                 )
#             print("Indexing complete.")

def get_not_vectorized_images():
    """
    Fetches the 'SSHOP_PRODUCTS' column for all images that have not been vectorized.

    Returns:
        A list of product identifiers or an empty list if none are found or an error occurs.
    """
    try:
        with get_mysql_db_connection() as conn:
            # Using dictionary=True makes each row a dictionary {column_name: value}
            with conn.cursor(dictionary=True) as cur:
                query = "SELECT * FROM smartshopper.SSHOP_PRODUCTS WHERE VECTORIZED = 0;"
                cur.execute(query)
                results = cur.fetchall()

                print(f"Found {len(results)} images to vectorize.")

                # for i, row in enumerate(results):
                #     print(f"Row {i + 1}: {row}")
                #     print(row['ID'])

                return results
    except Exception as e:
        print(f"❌ Error while fetching images: {e}")
        return []
    #
    # except mysql.connector.Error as e:
    #     print(f"❌ Database error while fetching images: {e}")
    #     return [] # Return an empty list in case of an error


# # --- 4. Search Function: Find the best match in the DB ---
# def search_images(text_query):
#     with get_db_connection() as conn:
#         # This is crucial to make psycopg2 understand the VECTOR type
#         register_vector(conn)
#
#         with conn.cursor() as cur:
#             print(f"\nSearching for: '{text_query}'")
#
#             # Generate the embedding for the text query
#             text_embedding = model.encode(text_query, convert_to_numpy=True)
#
#             # Perform the similarity search in PostgreSQL
#             # The '<=>' operator calculates the cosine distance (0=identical, 2=opposite)
#             cur.execute(
#                 """
#                 SELECT filename, 1 - (embedding <=> %s) AS similarity_score
#                 FROM images
#                 ORDER BY embedding <=> %s
#                 LIMIT 1;
#                 """,
#                 (text_embedding, text_embedding)
#             )
#
#             result = cur.fetchone()
#
#             if result:
#                 best_matching_image, best_match_score = result
#                 print(f"\nBest match found: {best_matching_image}")
#                 print(f"Cosine Similarity Score: {best_match_score:.4f}")
#             else:
#                 print("No results found.")

# --- 5. Main Execution Block ---
if __name__ == "__main__":
    # First, ensure all images are indexed in the database
    # index_images()

    # get_not_vectorized_images()

    # embedding = image_to_embedding("https://vistaindividual.vtexassets.com/arquivos/ids/304880/53740054_19_1-CAMISA-ML-SLIM-LINHO-GARMENT-DYE.jpg?v=638755760762800000");
    # store_image("xxxx", embedding)

    # # Then, start the search prompt
    # user_query = input("\nEnter your search query: ")
    # search_images(user_query)

    # --- Example Usage ---
    images_to_process = get_not_vectorized_images()
    # if images_to_process:
    #     print("Processing the following product images:", images_to_process)
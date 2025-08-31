import requests
import io
from PIL import Image
from sentence_transformers import SentenceTransformer

def get_embedding_from_url(image_url):
    """
    Downloads an image from a URL, converts it to an embedding,
    and returns the embedding vector.
    """
    model = SentenceTransformer('clip-ViT-B-32')
    try:
        # 1. Fetch the image data from the URL
        print(f"Fetching image from: {image_url}")
        response = requests.get(image_url)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # 2. Open the image from the in-memory bytes
        # response.content contains the raw binary data of the image
        image_bytes = io.BytesIO(response.content)
        image = Image.open(image_bytes).convert("RGB")

        # 3. Generate the embedding
        print("Generating embedding...")
        embedding = model.encode(image, convert_to_numpy=True)
        return embedding

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Main Execution Block ---
if __name__ == "__main__":
    # Load the pre-trained CLIP model
    clip_model = SentenceTransformer('clip-ViT-B-32')

    # Example URL of an image
    url = "https://images.unsplash.com/photo-1554629947-334ff61d85dc" # A mountain landscape

    # Get the embedding
    image_embedding = get_embedding_from_url(url)

    if image_embedding is not None:
        print("\n✅ Embedding generated successfully!")
        # Print the shape and first few values of the embedding vector
        print(f"Embedding shape: {image_embedding.shape}")
        print(f"First 5 values: {image_embedding[:5]}")
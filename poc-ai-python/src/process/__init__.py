from src.process.storeimage import get_not_vectorized_images
from src.process.storeimage import store_vectorized_image
from embeddingbyurl import get_embedding_from_url

results = get_not_vectorized_images()

for image in results:
    print(f"Processing image UUID: {image['ID']} from URL: {image['IMG']}")
    embedding = get_embedding_from_url(image['IMG'])
    if embedding is not None:
        store_vectorized_image(image['ID'], embedding)
        print(f"Stored embedding for image UUID: {image['ID']}")
    else:
        print(f"Failed to generate embedding for image UUID: {image['ID']}")

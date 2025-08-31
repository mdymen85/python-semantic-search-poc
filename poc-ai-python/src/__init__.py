# from sentence_transformers import SentenceTransformer, util
# from PIL import Image
# print("Loading CLIP model...")
# model = SentenceTransformer('clip-ViT-B-32')
# image_names = ['image1.png', 'image2.png', 'image3.png', 'image4.png',
#                'image5.png', 'image6.png', 'image7.png', 'image8.png',
#                'image9.png', 'image10.png', 'image11.png', 'image12.png',
#                'image14.png', 'image15.png']
# print(f"Generating embeddings for {len(image_names)} images...")
# image_embeddings = model.encode([Image.open(filepath).convert("RGB") for filepath in image_names], convert_to_tensor=True)
# text_query = input("Enter your search query: ")
# print(f"\nSearching for: '{text_query}'")
# text_embedding = model.encode(text_query, convert_to_tensor=True)
#
# # query_image = Image.open('searchable4.png').convert("RGB")
# # image_query_embedding = model.encode(query_image, convert_to_tensor=True)
# # print("\nCosine similarity between text query and image query:")
# # cosine_scores = util.cos_sim(image_query_embedding, image_embeddings)
#
# # for cosine_score in cosine_scores[0]:
#     # print(f"{cosine_score:.4f}")
#     # image_index = cosine_scores[0].tolist().index(cosine_score)
#     # print(f"Image: {image_names[image_index]}")
#     # if cosine_score > 0.85:
#     #   print(f"Match found with score: {cosine_score:.4f}")
#     #   image_index = cosine_scores[0].tolist().index(cosine_score)
#     #   print(f"Image: {image_names[image_index]}")
#
# cosine_scores = util.cos_sim(text_embedding, image_embeddings)
# best_match_index = cosine_scores.argmax()
# best_match_score = cosine_scores[0][best_match_index]
# best_matching_image = image_names[best_match_index]
#
# print(f"\nBest match found: {best_matching_image}")
# print(f"Cosine Similarity Score: {best_match_score:.4f}")

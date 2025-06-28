import os
import io
import json
import torch
import open_clip
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from functools import lru_cache

   
@lru_cache(maxsize=1)
def get_model():
    model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
    tokenizer = open_clip.get_tokenizer("ViT-B-32")
    model.eval()
    return model, preprocess, tokenizer

def normalize(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)

def load_catalog():
    with open("catalog.json") as f:
        return json.load(f)

def encode_embeddings():
    model, preprocess, tokenizer = get_model()
    catalog = load_catalog()

    image_features = []
    text_features = []
    valid_catalog = []

    for item in catalog:
        try:
            if 'image_path' in item and os.path.exists(item['image_path']):
                img = Image.open(item['image_path']).convert("RGB")
                img_tensor = preprocess(img).unsqueeze(0)

                text_tensor = tokenizer([item.get("description", "")])
                with torch.no_grad():
                    image_feat = model.encode_image(img_tensor).cpu().numpy()[0].astype(np.float32)
                    text_feat = model.encode_text(text_tensor).cpu().numpy()[0].astype(np.float32)

                image_features.append(image_feat)
                text_features.append(text_feat)
                valid_catalog.append(item)
        except:
            continue

    return normalize(np.stack(image_features)), normalize(np.stack(text_features)), valid_catalog

@lru_cache(maxsize=1)
def get_cached_vectors():
    return encode_embeddings()

def search_by_image(file, top_k=5, alpha=0.5):
    model, preprocess, _ = get_model()
    image_matrix, text_matrix, valid_catalog = get_cached_vectors()

    file.stream.seek(0)
    img = Image.open(io.BytesIO(file.read())).convert("RGB")
    img_tensor = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        query_feat = model.encode_image(img_tensor).cpu().numpy()
    
    query_feat = normalize(query_feat)

    sim_img = cosine_similarity(query_feat, image_matrix)[0]
    sim_txt = cosine_similarity(query_feat, text_matrix)[0]
    combined = alpha * sim_img + (1 - alpha) * sim_txt

    top_indices = combined.argsort()[::-1][:top_k]
    return [valid_catalog[i] for i in top_indices]
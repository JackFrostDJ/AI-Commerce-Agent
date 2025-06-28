import os
import io
import json
import torch
import open_clip
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model
model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
tokenizer = open_clip.get_tokenizer("ViT-B-32")
model.eval()

# Load and process catalog
with open("catalog.json") as f:
    catalog = json.load(f)

image_features = []
text_features = []
valid_catalog = []

for item in catalog:
    try:
        if 'image_path' in item and os.path.exists(item['image_path']):
            img = preprocess(Image.open(item['image_path']).convert("RGB")).unsqueeze(0)
            combined_text = item.get("description", "") + " " + " ".join(item.get("tags", []))
            txt = tokenizer([combined_text])

            with torch.no_grad():
                img_feat = model.encode_image(img).cpu().numpy()[0]
                txt_feat = model.encode_text(txt).cpu().numpy()[0]

            image_features.append(img_feat)
            text_features.append(txt_feat)
            valid_catalog.append(item)
    except Exception as e:
        continue

def normalize(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)

image_matrix = normalize(np.stack(image_features))
text_matrix = normalize(np.stack(text_features))

def search_by_image(file, top_k=5, alpha=0.9):
    file.stream.seek(0)
    img = Image.open(io.BytesIO(file.read())).convert("RGB")
    img_tensor = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        query_img_feat = model.encode_image(img_tensor).cpu().numpy()

    query_img_feat = normalize(query_img_feat)

    sim_img = cosine_similarity(query_img_feat, image_matrix)[0]
    sim_txt = cosine_similarity(query_img_feat, text_matrix)[0]

    combined = alpha * sim_img + (1 - alpha) * sim_txt
    best_idx = combined.argsort()[::-1][:top_k]

    if len(best_idx) == 0 or combined[best_idx[0]] < 0.2:
        return [{"id": -1, "name": "No similar items found", "description": "", "image_path": ""}]
    else:
        return [valid_catalog[i] for i in best_idx]
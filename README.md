# <img src="frontend/public/logo.png" width="20" alt="Logo" /> Comma – Your AI Commerce Agent

Comma is a modern full-stack AI assistant that helps users **search and discover products** via **chat or image upload**. It uses **natural language processing** and **visual similarity search** to recommend relevant catalog items, combining the best of AI and commerce.

---

## Features

- **Chat-based AI Assistant** – Answering product-related queries using LLMs
- **Image-Based Search** – Upload a photo and find similar products
- **Hybrid Search** – Combine chat and image context for accurate recommendations
- **Modern UI** – Responsive, elegant gold-on-dark themed interface
- **Drag & Drop Support** – Attach product images directly into the chat
- **Context-Aware Conversations** – Maintains limited dialogue history
- **Tailwind CSS** styling with branded UI

---

## Tech Stack

| Layer       | Technology                          | Why Chosen                                                                 |
|-------------|--------------------------------------|----------------------------------------------------------------------------|
| **Frontend**| React + Tailwind CSS                | Modern component-based architecture and fast styling via utility classes   |
| **Backend** | Python (Flask)                      | Lightweight and flexible for rapid prototyping and AI model integration    |
| **ML APIs** | HuggingFace Zephyr-7B + BART-MNLI   | For generative response and message classification                        |
| **Image Search** | OpenCLIP + cosine similarity   | For powerful zero-shot image-to-text product matching                      |
| **Deployment** | Vercel (Frontend), Render (Backend) | Clear separation of concerns, scalability, and fast CI/CD integration     |

---

## Project Structure
```
ai-commerce-agent/
├── backend/
│ ├──nltk_data/
│ ├── app.py
│ ├── recommender.py
│ ├── image_search.py
│ ├── catalog.json
│ └── static/images/
│
├── frontend/
│ ├──node_modules/
│ ├── src/
│   ├── App.js
│   ├── index.js
│   └── index.css
│ ├── public/
│   ├── index.html
│   └── logo.png
│ ├── package-lock.json
│ ├── package.json
│ ├── postcss.config.js
│ └── tailwind.config.js
├── requirements.txt
└── README.md
```
---

## Deployment Setup

### Vercel (Frontend)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Env Variable**:  
  `REACT_APP_BACKEND_URL=https://your-render-backend.onrender.com`

### Render (Backend)
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Env Variables**: `HF_API_TOKEN`

---

## Sample Prompts

- "Can you recommend red running shoes under $100?"
- "Here’s a photo of a hoodie I like – show me something similar."
- "Find casual women’s pants in gray."
- "What can you do?"

---

## AI Integration

- **Zephyr-7B** is used via HuggingFace’s `featherless-ai` endpoint for fast, affordable LLM responses.
- **BART-MNLI** classifies each user query into `"chat"` or `"recommendation"` mode.
- **OpenCLIP ViT-B/32** maps uploaded images to embedding space and performs hybrid similarity search against catalog items.

---

## Design Philosophy

- **Monorepo-first** – Shared GitHub repo enables easier development and deployment separation
- **Minimal External Services** – Self-hosted image + catalog search, avoiding expensive APIs
- **Scalable Components** – Both chat and image search are composable, cleanly separated
- **User-Centric UI** – Drag & drop, dynamic previews, and mobile responsiveness

---

## Future Enhancements

- Vector database support (e.g., FAISS or Weaviate) for faster image similarity search
- Stripe integration for cart/checkout functionality
- Multilingual LLM support
- User accounts and persistent chat history

---

## Credits

Developed by Joel Jishu 

Inspired by modern retail AI tools and powered by open-source intelligence.
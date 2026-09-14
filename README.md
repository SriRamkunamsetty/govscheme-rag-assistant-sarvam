# Scheme Sahayak — Government Scheme RAG Assistant

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" /></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" /></a>
  <a href="https://www.sarvam.ai/"><img src="https://img.shields.io/badge/Sarvam_AI-105B_LLM-EA580C?style=for-the-badge" alt="Sarvam AI 105B" /></a>
  <a href="https://www.sarvam.ai/"><img src="https://img.shields.io/badge/Voice_TTS-Bulbul_v3-7928CA?style=for-the-badge" alt="Sarvam Bulbul v3" /></a>
  <img src="https://img.shields.io/badge/Hybrid_RAG-BM25_%2B_TF--IDF-0284C7?style=for-the-badge" alt="Hybrid RAG" />
  <img src="https://img.shields.io/badge/Indic_Languages-11_Supported-16A34A?style=for-the-badge" alt="11 Indic Languages" />
  <a href="https://vercel.com/"><img src="https://img.shields.io/badge/Deploy-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel" /></a>
</p>

Ask a question about an Indian government welfare scheme in any Indian language (Telugu, Hindi, Tamil, Kannada, Bengali, Marathi, Gujarati, Malayalam, Punjabi, Odia) or English, and receive an authoritative answer grounded in real scheme documents — translated back into your preferred language with full source provenance.

Built as part of a Sarvam AI build sprint, combining a production-grade **Hybrid RAG pipeline** (BM25 + TF-IDF with Reciprocal Rank Fusion) with Sarvam AI's **Chat Completions (`sarvam-105b`)**, **Bulbul v3 Text-to-Speech**, and **Translate APIs**.

---

## Architecture & Pipeline

```
Citizen question (any Indic language or English)
        │
        ▼
Sarvam Translate API (auto → en-IN)  ──►  Normalized English query
        │
        ▼
Query Expansion (welfare synonym mapping)
        │
        ▼
Hybrid Retrieval: BM25Okapi (lexical) + TF-IDF n-grams (semantic)
        │
        ▼
Reciprocal Rank Fusion (RRF) Ranking  ──►  Top diversified matching scheme chunks
        │
        ▼
Sarvam Chat Completions (sarvam-105b) ──►  Grounded English answer (strict context)
        │
        ▼
Sarvam Translate API (en-IN → target language, e.g. te-IN, hi-IN, ta-IN)
        │
        ▼
Response JSON: { answer_target_lang, answer_english, sources, detailed_sources }
```

### Why Hybrid Search (BM25 + TF-IDF with RRF)?
BM25 alone is purely lexical and can miss queries that use colloquial synonyms ("doctor/hospital" vs. "secondary hospitalisation cover"). The production pipeline fuses:
1. **BM25Okapi**: Catches exact scheme titles, acronyms, and statutory keywords.
2. **TF-IDF Sublinear N-grams**: Catches semantic phrase variations and character n-grams.
3. **Reciprocal Rank Fusion (RRF)**: Merges both score lists with $k=60$ penalty, ensuring high-recall, diversified, and robust retrieval without the operational overhead of a heavy vector database.

---

## Indexed Government Schemes

The knowledge base covers 12 major central welfare schemes with structured metadata (eligibility, financial benefits, nodal ministry, and application portals):

1. **PM-KISAN** (Income support for landholding farmers: ₹6,000/year DBT)
2. **Ayushman Bharat (PM-JAY)** (Cashless health assurance up to ₹5 Lakh/family/year)
3. **Pradhan Mantri Awas Yojana (PMAY)** (Pucca housing grants and interest subsidies)
4. **MGNREGA** (100 days statutory wage employment guarantee in rural areas)
5. **PM Ujjwala Yojana (PMUY)** (Deposit-free LPG connections & first refill for women)
6. **Sukanya Samriddhi Yojana (SSY)** (Small savings scheme for girl child with 8.2% interest)
7. **PM SVANidhi** (Collateral-free working capital micro-loans for street vendors)
8. **Atal Pension Yojana (APY)** (Guaranteed monthly pension up to ₹5,000/month after 60)
9. **PM Vishwakarma** (Skill training, ₹15,000 toolkit grant & credit for traditional artisans)
10. **Pradhan Mantri Mudra Yojana (PMMY)** (Micro-business loans up to ₹20 Lakh)
11. **Janani Suraksha Yojana (JSY)** (Institutional delivery cash assistance for mothers & ASHAs)
12. **National Social Assistance Programme (NSAP)** (Elderly, widow, and disability pensions)

---

## Setup & Running

### Prerequisites
- Python 3.10+
- (Optional) `SARVAM_API_KEY` for live AI generation and translation.

### 1. Start Backend
```bash
cd backend
pip install -r requirements.txt

# For live AI generation and translation:
export SARVAM_API_KEY="your_sarvam_api_key_here"

# Start the server:
uvicorn main:app --reload --port 8000
```

> **Resilient Demo Mode:** If `SARVAM_API_KEY` is not provided, the backend automatically starts in an intelligent **Mock/Demo Mode**. All Hybrid RRF retrieval, endpoints, and language mappings remain fully functional with curated bilingual responses.

### 2. Open Frontend
Open `frontend/index.html` directly in your browser, or serve it using any static server:
```bash
# Python one-liner to serve frontend
python -m http.server 3000 --directory frontend
```
Navigate to `http://localhost:3000` (or open `frontend/index.html` as a local file).

---

## Security & Reliability Engineering

- **XSS Prevention**: Frontend strictly complies with secure coding guidelines by completely eliminating unsafe DOM methods (`innerHTML`, `outerHTML`). All elements are constructed using `document.createElement`, `textContent`, and `replaceChildren()`.
- **Security Response Headers**: Backend injects `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and `X-XSS-Protection`.
- **Input Validation**: Bounded inputs with Pydantic validation (max 500 characters, non-empty, stripped whitespace).
- **Anti-Hallucination Grounding**: System prompt strictly restricts answers to the provided context, instructing the model to declare lack of context rather than hallucinating eligibility terms.

---

## Multilingual Voice Accessibility

- **Text-to-Speech (TTS) via Sarvam Bulbul:v3**: Every answer card includes an audio playback button (`🔊 Listen / వినండి / सुनिए`) that converts answers into natural spoken audio across all 11 supported Indian languages.
- **Dual-Engine Voice Playback**: Primary audio is generated via Sarvam's Bulbul:v3 model (`POST /tts`), with automatic fallback to the browser-native HTML5 Web Speech API (`window.speechSynthesis`).
- **Speech-to-Text Input (Microphone 🎙️)**: Citizens can speak their questions directly into the input bar using Web Speech Recognition configured to their selected Indic language.

---

## Deploy to Vercel

The project is pre-configured with zero-config Vercel Serverless Python support (`vercel.json`, `api/index.py`, and `public/index.html`).

### Steps to Deploy:
1. **Import to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new) and import your GitHub repository: `SriRamkunamsetty/govscheme-rag-assistant-sarvam`.
   - Vercel automatically detects `vercel.json` and Python requirements.
2. **Set Environment Variables**:
   - In the Vercel project configuration, add:
     - `SARVAM_API_KEY`: Your Sarvam AI API Key (`sk_7dobwl3v_cqg8ysqLjDMQdrLeqdALOwjH`).
3. **Deploy**:
   - Click **Deploy**. Your application will be live at `https://govscheme-rag-assistant-sarvam.vercel.app`.
   - The FastAPI backend runs as a high-performance Serverless Function at `/api/*`, and the frontend is instantly served across global CDN Edge locations.

---

## Tech Stack

- **Backend:** FastAPI, `scikit-learn` (TF-IDF), `rank_bm25` (with pure-Python fallback), `langchain-text-splitters`, Sarvam AI SDK (`bulbul:v3` TTS, `sarvam-105b` LLM, Translate).
- **Frontend:** Single-file HTML5/CSS3/Vanilla JS with native DOM manipulation, Google Fonts (Noto Sans for Telugu, Devanagari, Tamil, Kannada, Bengali), Web Speech API.
- **AI Models:** Sarvam `sarvam-105b` (LLM Generation), Sarvam Translate (Language translation), Sarvam Bulbul:v3 (Text-to-Speech).
- **Deployment:** Vercel (Serverless Python runtime + Edge Network static hosting).

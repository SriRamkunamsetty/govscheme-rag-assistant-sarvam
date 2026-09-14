"""
Government Scheme RAG Assistant — Production Backend (Scheme Sahayak)

Pipeline:
  1. Multilingual Question received (Telugu, Hindi, Tamil, Kannada, English, etc.).
  2. Normalize query to English via Sarvam Translate API (or heuristic detection).
  3. Hybrid Retrieval: Fuses BM25Okapi (lexical) + TF-IDF n-grams (semantic)
     using Reciprocal Rank Fusion (RRF) over the expanded scheme knowledge base.
  4. Grounded Generation: Sarvam-105b LLM generates answer strictly using context.
  5. Language Translation: Translates grounded answer into the user's requested
     target Indic language (defaulting to Telugu or chosen language).
  6. Returns structured response with verified sources, category, and metadata.
"""

import math
import os
import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

# Optional imports with graceful fallbacks
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    class RecursiveCharacterTextSplitter:
        def __init__(self, chunk_size: int = 400, chunk_overlap: int = 50):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap

        def split_text(self, text: str) -> List[str]:
            chunks = []
            start = 0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                chunks.append(text[start:end])
                if end == len(text):
                    break
                start += self.chunk_size - self.chunk_overlap
            return chunks

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    class BM25Okapi:  # type: ignore
        """Pure-Python BM25Okapi implementation with zero native dependencies."""
        def __init__(self, corpus: List[List[str]], k1: float = 1.5, b: float = 0.75):
            self.k1 = k1
            self.b = b
            self.corpus_size = len(corpus)
            self.corpus = corpus
            self.doc_len = [len(doc) for doc in corpus]
            self.avgdl = sum(self.doc_len) / self.corpus_size if self.corpus_size > 0 else 0.0
            self.doc_freqs = [Counter(doc) for doc in corpus]
            self.nd = Counter()
            for df in self.doc_freqs:
                for word in df:
                    self.nd[word] += 1
            self.idf = {}
            for word, freq in self.nd.items():
                self.idf[word] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

        def get_scores(self, query: List[str]) -> List[float]:
            scores = [0.0] * self.corpus_size
            for q in query:
                if q not in self.idf:
                    continue
                q_idf = self.idf[q]
                for idx, df in enumerate(self.doc_freqs):
                    if q not in df:
                        continue
                    tf = df[q]
                    num = tf * (self.k1 + 1.0)
                    denom = tf + self.k1 * (1.0 - self.b + self.b * (self.doc_len[idx] / (self.avgdl or 1.0)))
                    scores[idx] += q_idf * (num / denom)
            return scores

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from documents import SCHEME_DOCS

# ---------------------------------------------------------------------------
# 1. Supported Languages Configuration
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES = {
    "te-IN": {"name": "Telugu", "native": "తెలుగు", "font_class": "te"},
    "hi-IN": {"name": "Hindi", "native": "हिन्दी", "font_class": "hi"},
    "ta-IN": {"name": "Tamil", "native": "தமிழ்", "font_class": "ta"},
    "kn-IN": {"name": "Kannada", "native": "ಕನ್ನಡ", "font_class": "kn"},
    "bn-IN": {"name": "Bengali", "native": "বাংলা", "font_class": "bn"},
    "mr-IN": {"name": "Marathi", "native": "मराठी", "font_class": "mr"},
    "gu-IN": {"name": "Gujarati", "native": "ગુજરાતી", "font_class": "gu"},
    "ml-IN": {"name": "Malayalam", "native": "മലയാളം", "font_class": "ml"},
    "pa-IN": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "font_class": "pa"},
    "od-IN": {"name": "Odia", "native": "ଓଡ଼ିଆ", "font_class": "od"},
    "en-IN": {"name": "English", "native": "English", "font_class": "en"},
}

# ---------------------------------------------------------------------------
# 2. In-Memory Search Indexing: BM25 + TF-IDF (Hybrid Search)
# ---------------------------------------------------------------------------

splitter = RecursiveCharacterTextSplitter(chunk_size=420, chunk_overlap=60)

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "for", "of", "to", "in", "on", "at", "by", "with", "and", "or", "but",
    "if", "so", "as", "it", "its", "this", "that", "these", "those", "there",
    "any", "does", "do", "did", "has", "have", "had", "i", "you", "we",
    "they", "he", "she", "what", "which", "who", "how", "help", "tell",
    "about", "me", "there's", "can", "could", "would", "should", "will",
    "give", "get", "scheme", "schemes", "government", "govt", "yojana",
}

SYNONYM_MAP = {
    "house": "housing pucca awas shelter pmay",
    "housing": "housing pucca awas shelter pmay",
    "home": "housing pucca awas construction pmay",
    "farmer": "agriculture kisan cultivable land crop pmkisan",
    "farmers": "agriculture kisan cultivable land crop pmkisan",
    "farming": "agriculture kisan cultivable land crop pmkisan",
    "hospital": "health treatment hospitalisation medical cashless ayushman pmjay",
    "health": "treatment hospitalisation medical insurance ayushman pmjay",
    "medical": "treatment hospitalisation health medicine ayushman pmjay",
    "doctor": "healthcare hospital clinic treatment ayushman",
    "job": "work employment wages rural manual mgnrega 100 days",
    "jobs": "work employment wages rural manual mgnrega 100 days",
    "work": "employment wage manual labor 100 days mgnrega",
    "employment": "wage manual labor 100 days mgnrega work",
    "gas": "lpg cylinder stove fuel ujjwala cooking pmuy",
    "cooking": "lpg gas cylinder stove fuel ujjwala pmuy",
    "daughter": "girl child sukanya samriddhi education marriage ssy",
    "girl": "child sukanya samriddhi daughter education ssy",
    "girls": "child sukanya samriddhi daughter education ssy",
    "vendor": "street vendor hawker svanidhi loan micro credit urban",
    "vendors": "street vendor hawker svanidhi loan micro credit urban",
    "hawker": "street vendor svanidhi credit loan urban",
    "pension": "social security old age senior citizen atal apy nsap monthly pension",
    "pensions": "social security old age senior citizen atal apy nsap monthly pension",
    "old": "elderly senior citizen pension atal apy nsap ignoaps 60",
    "senior": "elderly old age pension atal apy nsap ignoaps 60",
    "loan": "credit collateral mudra svanidhi interest subsidy micro finance",
    "loans": "credit collateral mudra svanidhi interest subsidy micro finance",
    "business": "enterprise shop startup mudra svanidhi shishu kishore tarun",
    "artisan": "craftsperson vishwakarma toolkit carpenter blacksmith trade artisan",
    "artisans": "craftsperson vishwakarma toolkit carpenter blacksmith trade artisan",
    "pregnant": "maternal janani institutional delivery mother newborn jsy asha",
    "delivery": "maternal pregnant institutional delivery janani suraksha asha jsy",
    "mother": "maternal pregnant institutional delivery janani suraksha jsy",
    "widow": "widow pension nsap ignwps social security assistance",
    "disabled": "disability pension nsap igndps social security assistance",
}


def tokenize(text: str) -> List[str]:
    words = "".join(ch.lower() if ch.isalnum() else " " for ch in text).split()
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def expand_query(query: str) -> str:
    tokens = tokenize(query)
    expanded = list(tokens)
    for token in tokens:
        if token in SYNONYM_MAP:
            expanded.extend(SYNONYM_MAP[token].split())
    return " ".join(expanded)


# Build Knowledge Base Chunks with Metadata Context
chunks: List[str] = []
chunk_metadata: List[Dict[str, str]] = []

for doc in SCHEME_DOCS:
    header = f"[{doc['title']} | Category: {doc['category']} | Ministry: {doc['ministry']}]"
    doc_full_text = (
        f"{header}\n"
        f"Benefits: {doc['benefits']}\n"
        f"Eligibility: {doc['eligibility']}\n"
        f"How to Apply: {doc['application_process']}\n"
        f"Details: {doc['content']}"
    )
    for piece in splitter.split_text(doc_full_text):
        chunks.append(piece)
        chunk_metadata.append({
            "id": doc["id"],
            "title": doc["title"],
            "short_name": doc["short_name"],
            "category": doc["category"],
            "ministry": doc["ministry"],
            "benefits": doc["benefits"],
            "eligibility": doc["eligibility"],
            "application": doc["application_process"],
        })

# Index 1: BM25 Okapi
tokenized_chunks = [tokenize(c) for c in chunks]
bm25_index = BM25Okapi(tokenized_chunks)

# Index 2: TF-IDF Sublinear N-gram Vectorizer
tfidf_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    ngram_range=(1, 2),
    stop_words="english",
)
tfidf_matrix = tfidf_vectorizer.fit_transform(chunks)


def hybrid_retrieve(query: str, top_k: int = 3) -> List[Dict]:
    """
    Combines BM25Okapi and TF-IDF Cosine Similarity using Reciprocal Rank Fusion (RRF).
    RRF Score: sum(1 / (60 + rank_i)) across both retrieval algorithms.
    """
    expanded = expand_query(query)
    query_tokens = tokenize(expanded)
    if not query_tokens:
        query_tokens = tokenize(query)

    # 1. BM25 Scores
    bm25_scores = bm25_index.get_scores(query_tokens)
    bm25_ranked = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)

    # 2. TF-IDF Cosine Similarity
    query_vec = tfidf_vectorizer.transform([expanded if expanded else query])
    tfidf_sims = cosine_similarity(query_vec, tfidf_matrix).flatten()
    tfidf_ranked = sorted(range(len(tfidf_sims)), key=lambda i: tfidf_sims[i], reverse=True)

    # 3. Reciprocal Rank Fusion
    k_rrf = 60.0
    rrf_scores: Dict[int, float] = defaultdict(float)

    for rank, idx in enumerate(bm25_ranked[:20]):
        if bm25_scores[idx] > 0.01:
            rrf_scores[idx] += 1.0 / (k_rrf + rank + 1)

    for rank, idx in enumerate(tfidf_ranked[:20]):
        if tfidf_sims[idx] > 0.01:
            rrf_scores[idx] += 1.0 / (k_rrf + rank + 1)

    # Filter and sort
    final_ranked = sorted(rrf_scores.keys(), key=lambda i: rrf_scores[i], reverse=True)

    results = []
    seen_schemes = set()
    for idx in final_ranked:
        meta = chunk_metadata[idx]
        if meta["id"] in seen_schemes:
            continue
        results.append({
            "id": meta["id"],
            "title": meta["title"],
            "short_name": meta["short_name"],
            "category": meta["category"],
            "ministry": meta["ministry"],
            "benefits": meta["benefits"],
            "eligibility": meta["eligibility"],
            "application": meta["application"],
            "text": chunks[idx],
            "rrf_score": rrf_scores[idx],
        })
        seen_schemes.add(meta["id"])
        if len(results) >= top_k:
            break

    return results


# ---------------------------------------------------------------------------
# 3. Sarvam Client & Intelligent Fallback Engine
# ---------------------------------------------------------------------------

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "").strip()
sarvam_client = None

if SARVAM_API_KEY:
    try:
        from sarvamai import SarvamAI
        sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
    except Exception as exc:
        print(f"[Warning] Failed to initialize SarvamAI client: {exc}. Operating in Mock/Demo mode.")
else:
    print("[Info] SARVAM_API_KEY not set. Backend operating in resilient Mock/Demo mode.")

# Curated bilingual mock answers for standard queries when operating without an API key
DEMO_RESPONSES = {
    "pm-kisan": {
        "te-IN": "అవును — PM-KISAN (ప్రధాన మంత్రి కిసాన్ సమ్మాన్ నిధి) అర్హులైన రైతు కుటుంబాలకు సంవత్సరానికి రూ. 6,000 ఆదాయ సహాయాన్ని అందిస్తుంది. ఈ మొత్తం రూ. 2,000 చొప్పున మూడు సమాన వాయిదాలలో నేరుగా లబ్ధిదారుల బ్యాంక్ ఖాతాల్లోకి జమ అవుతుంది. రైతులు pmkisan.gov.in పోర్టల్ లేదా స్థానిక CSC కేంద్రాల ద్వారా దరఖాస్తు చేసుకోవచ్చు.",
        "hi-IN": "हाँ — पीएम-किसान योजना के तहत पात्र किसान परिवारों को प्रति वर्ष 6,000 रुपये की प्रत्यक्ष वित्तीय सहायता दी जाती है, जो 2,000 रुपये की तीन समान किस्तों में सीधे बैंक खाते में भेजी जाती है। किसान pmkisan.gov.in पोर्टल या कॉमन सर्विस सेंटर (CSC) पर आवेदन कर सकते हैं।",
        "ta-IN": "ஆம் — பிஎம்-கிசான் திட்டத்தின் கீழ் தகுதியுள்ள விவசாய குடும்பங்களுக்கு ஆண்டுக்கு ரூ. 6,000 மூன்று தவணைகளில் நேரடியாக வங்கி கணக்கில் வழங்கப்படுகிறது. விவசாயிகள் pmkisan.gov.in மூலம் விண்ணப்பிக்கலாம்.",
    },
    "pm-jay": {
        "te-IN": "ఆయుష్మాన్ భారత్ (PM-JAY) పథకం ద్వారా ఆర్థికంగా బలహీన కుటుంబాలకు ద్వితీయ, తృతీయ స్థాయి ఆసుపత్రి చికిత్సల కోసం కుటుంబానికి సంవత్సరానికి రూ. 5 లక్షల వరకు ఉచిత నగదు రహిత ఆరోగ్య బీమా లభిస్తుంది. దేశవ్యాప్తంగా ఉన్న ప్రభుత్వ మరియు ప్రైవేట్ ఆసుపత్రులలో నగదు రహిత చికిత్స పొందవచ్చు.",
        "hi-IN": "आयुष्मान भारत (पीएम-जय) योजना आर्थिक रूप से कमजोर परिवारों को माध्यमिक और तृतीयक अस्पताल में भर्ती के लिए प्रति परिवार प्रति वर्ष 5 लाख रुपये तक का कैशलेस स्वास्थ्य बीमा कवर प्रदान करती है। देश भर के सूचीबद्ध सरकारी और निजी अस्पतालों में मुफ्त इलाज मिलता है।",
        "ta-IN": "ஆயுஷ்மான் பாரத் (PM-JAY) திட்டம் ஏழை எளிய குடும்பங்களுக்கு ஆண்டுக்கு ரூ. 5 லட்சம் வரை இலவச மருத்துவக் காப்பீடு வழங்குகிறது. பதிவு செய்யப்பட்ட மருத்துவமனைகளில் பணமில்லா சிகிச்சை பெறலாம்.",
    },
    "pmay": {
        "te-IN": "అవును — ప్రధాన మంత్రి ఆవాస్ యోజన (PMAY) తక్కువ ఆదాయం, ఆర్థికంగా బలహీన వర్గాల ప్రజలకు పక్కా ఇళ్ల నిర్మాణానికి ఆర్థిక సహాయం అందిస్తుంది. గ్రామీణ ప్రాంతాల్లో రూ. 1.20 లక్షల వరకు మరియు పట్టణ ప్రాంతాల్లో గృహ రుణాలపై వడ్డీ రాయితీ (రూ. 2.67 లక్షల వరకు) లభిస్తుంది.",
        "hi-IN": "हाँ — प्रधानमंत्री आवास योजना (PMAY) बेघर और कच्चे मकानों में रहने वाले परिवारों को पक्का मकान बनाने हेतु वित्तीय सहायता देती है। ग्रामीण क्षेत्रों में 1.20 से 1.30 लाख रुपये का सीधा अनुदान और शहरी क्षेत्रों में होम लोन पर ब्याज सब्सिडी प्रदान की जाती है।",
        "ta-IN": "ஆம் — பிரதான் மந்திரி ஆவாஸ் யோஜனா (PMAY) ஏழை குடும்பங்களுக்கு சொந்தமாக கான்கிரீட் வீடு கட்ட நேரடி நிதி உதவியும் வட்டி மானியமும் வழங்குகிறது.",
    },
    "mgnrega": {
        "te-IN": "MGNREGA చట్టం ప్రతి గ్రామీణ కుటుంబానికి సంవత్సరానికి కనీసం 100 రోజుల నైపుణ్యం లేని శారీరక వేతన ఉపాధికి చట్టబద్ధమైన హామీ ఇస్తుంది. దరఖాస్తు చేసిన 15 రోజుల్లోపు పని కల్పించకపోతే నిరుద్యోగ భృతి ఇవ్వబడుతుంది.",
        "hi-IN": "मनरेगा (MGNREGA) ग्रामीण परिवारों के वयस्क सदस्यों को प्रत्येक वित्तीय वर्ष में कम से कम 100 दिनों के अकुशल शारीरिक कार्य की कानूनी गारंटी देता है। काम मांगने के 15 दिनों के भीतर रोजगार न मिलने पर बेरोजगारी भत्ता दिया जाता है।",
        "ta-IN": "மகாத்மா காந்தி ஊரக வேலைவாய்ப்புத் திட்டம் (MGNREGA) கிராமப்புற குடும்பங்களுக்கு ஆண்டுக்கு குறைந்தது 100 நாட்கள் கூலி வேலைக்கான சட்டபூர்வ உத்தரவாதத்தை வழங்குகிறது.",
    },
    "pmuy": {
        "te-IN": "అవును — ప్రధాన మంత్రి ఉజ్వల యోజన (PMUY) పేద కుటుంబాల మహిళలకు ఉచిత డిపాజిట్ రహిత వంట గ్యాస్ (LPG) కనెక్షన్లను అందిస్తుంది. సిలిండర్ సెక్యూరిటీ డిపాజిట్, మొదటి రీఫిల్ మరియు స్టవ్ ఉచితంగా లభిస్తాయి.",
        "hi-IN": "हाँ — प्रधानमंत्री उज्ज्वला योजना (PMUY) के तहत बीपीएल व गरीब परिवारों की महिलाओं को मुफ्त एलपीजी गैस कनेक्शन प्रदान किया जाता है। इसमें पहला सिलेंडर रीफिल और चूल्हा पूरी तरह मुफ्त दिया जाता है।",
        "ta-IN": "ஆம் — பிரதான் மந்திரி உஜ்வாலா யோஜனா மூலம் வறுமைக் கோட்டிற்கு கீழ் உள்ள பெண்களுக்கு இலவச சமையல் எரிவாயு இணைப்பு மற்றும் முதல் சிலிண்டர் இலவசமாக வழங்கப்படுகிறது.",
    },
    "ssy": {
        "te-IN": "సుకున్య సమృద్ధి యోజన అనేది ఆడపిల్లల ఉన్నత విద్య మరియు వివాహ ఖర్చుల కోసం ఉద్దేశించిన ప్రభుత్వ చిన్న పొదుపు పథకం. 10 సంవత్సరాల లోపు ఆడపిల్లల పేరుతో ఖాతా తెరవవచ్చు, ఇది ప్రస్తుతం 8.2% ఆకర్షణీయమైన వడ్డీ రేటును మరియు పూర్తి పన్ను మినహాయింపును అందిస్తుంది.",
        "hi-IN": "सुकन्या समृद्धि योजना बेटियों की उच्च शिक्षा और शादी के लिए एक सरकारी छोटी बचत योजना है। 10 वर्ष तक की बालिकाओं के नाम पर खाता खोला जा सकता है, जिस पर 8.2% की उच्च ब्याज दर और 80C के तहत पूर्ण कर छूट मिलती है।",
        "ta-IN": "சுகன்யா சம்ரிதி யோஜனா என்பது பெண் குழந்தைகளின் எதிர்காலக் கல்வி மற்றும் திருமண செலவுகளுக்காக 10 வயதுக்குட்பட்ட பெண் குழந்தைகளுக்கு துவங்கப்படும் உயர் வட்டி கொண்ட சேமிப்புத் திட்டமாகும்.",
    },
}


# ---------------------------------------------------------------------------
# 4. Security Middleware & FastAPI Application
# ---------------------------------------------------------------------------

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


app = FastAPI(
    title="Scheme Sahayak — Government Scheme RAG Assistant",
    description="Multilingual AI assistant grounded in Indian central government welfare schemes.",
    version="2.0.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)


# ---------------------------------------------------------------------------
# 5. Pydantic Schemas
# ---------------------------------------------------------------------------

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500, description="User question in any Indian language or English")
    target_language_code: Optional[str] = Field("te-IN", description="Target response language code (e.g., te-IN, hi-IN, ta-IN)")


# ---------------------------------------------------------------------------
# 6. REST API Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "Scheme Sahayak (Government Scheme RAG Assistant)",
        "status": "online",
        "mode": "live" if sarvam_client else "demo",
        "version": "2.0.0",
        "total_schemes": len(SCHEME_DOCS),
        "endpoints": ["/schemes", "/languages", "/health", "/ask"],
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "sarvam_api_configured": bool(sarvam_client),
        "total_schemes_indexed": len(SCHEME_DOCS),
        "total_chunks_indexed": len(chunks),
        "retrieval_mode": "Hybrid (BM25 + TF-IDF with Reciprocal Rank Fusion)",
    }


@app.get("/languages")
def list_languages():
    """Returns supported Indic languages for the frontend language selector."""
    return {"languages": SUPPORTED_LANGUAGES}


@app.get("/schemes")
def list_schemes():
    """Returns complete catalog of indexed schemes with categories and metadata."""
    return {
        "total": len(SCHEME_DOCS),
        "schemes": [
            {
                "id": doc["id"],
                "title": doc["title"],
                "short_name": doc["short_name"],
                "category": doc["category"],
                "ministry": doc["ministry"],
                "benefits": doc["benefits"],
                "eligibility": doc["eligibility"],
                "application": doc["application_process"],
            }
            for doc in SCHEME_DOCS
        ],
    }


@app.post("/ask")
def ask(payload: QuestionRequest):
    clean_question = payload.question.strip()
    target_lang = payload.target_language_code or "te-IN"

    if target_lang not in SUPPORTED_LANGUAGES:
        target_lang = "te-IN"

    english_question = clean_question

    # Step 1: Normalize query to English via Sarvam Translation if available
    if sarvam_client:
        try:
            translation = sarvam_client.text.translate(
                input=clean_question,
                source_language_code="auto",
                target_language_code="en-IN",
            )
            english_question = translation.translated_text
        except Exception as exc:
            print(f"[Translate Error] Fallback to original text: {exc}")
            english_question = clean_question

    # Step 2: Hybrid Retrieval (BM25 + TF-IDF with RRF)
    matches = hybrid_retrieve(english_question, top_k=3)

    if not matches:
        answer_en = (
            "I could not find a matching welfare scheme in my knowledge base for your inquiry. "
            "You can ask about PM-KISAN, Ayushman Bharat (PM-JAY), PMAY Housing, MGNREGA, "
            "PM Ujjwala, Sukanya Samriddhi, PM SVANidhi, Atal Pension, PM Vishwakarma, Mudra, or Janani Suraksha."
        )
        answer_target = answer_en
        matched_sources = []
    else:
        context_blocks = []
        for m in matches:
            context_blocks.append(f"[{m['title']} | Ministry: {m['ministry']}]\n{m['text']}")
        context_text = "\n\n".join(context_blocks)

        matched_sources = [
            {
                "id": m["id"],
                "title": m["title"],
                "short_name": m["short_name"],
                "category": m["category"],
                "ministry": m["ministry"],
                "benefits": m["benefits"],
            }
            for m in matches
        ]

        # Step 3: Grounded Answer Generation
        if sarvam_client:
            try:
                completion = sarvam_client.chat.completions(
                    model="sarvam-105b",
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are 'Scheme Sahayak', an authoritative, empathetic assistant answering "
                                "citizen queries about Indian government welfare schemes. "
                                "Answer ONLY using the provided scheme context. Keep answers clear, factual, "
                                "and concise (2-4 sentences). Mention specific benefits or eligibility from "
                                "the context when available. If the provided context does not cover the question, "
                                "explicitly state that you do not have that information instead of guessing."
                            ),
                        },
                        {
                            "role": "user",
                            "content": f"Context:\n{context_text}\n\nQuestion: {english_question}",
                        },
                    ],
                )
                msg = completion.choices[0].message
                answer_en = (msg.content or "").strip()
                if not answer_en and getattr(msg, "reasoning_content", None):
                    answer_en = msg.reasoning_content.strip()
                if not answer_en:
                    top = matches[0]
                    answer_en = f"Under {top['title']}, eligible beneficiaries receive: {top['benefits']}."
            except Exception as exc:
                print(f"[LLM Error] Falling back to synthesized answer: {exc}")
                top = matches[0]
                answer_en = f"Under {top['title']}, eligible beneficiaries receive: {top['benefits']}. Details: {top['text'][:250]}..."
        else:
            # Resilient demo fallback when API key is not configured
            top = matches[0]
            answer_en = (
                f"Under {top['title']} ({top['category']}), eligible beneficiaries receive {top['benefits']} "
                f"Applicants can apply via: {top['application']}."
            )

        # Step 4: Translate grounded answer to user's selected Indic language
        if target_lang == "en-IN":
            answer_target = answer_en
        elif sarvam_client:
            try:
                trans_res = sarvam_client.text.translate(
                    input=answer_en,
                    source_language_code="en-IN",
                    target_language_code=target_lang,
                )
                answer_target = trans_res.translated_text
            except Exception as exc:
                print(f"[Translate Target Error] {exc}")
                top_id = matches[0]["id"]
                answer_target = DEMO_RESPONSES.get(top_id, {}).get(target_lang, answer_en)
        else:
            # Deterministic fallback response in requested language if available
            top_id = matches[0]["id"]
            answer_target = DEMO_RESPONSES.get(top_id, {}).get(target_lang, answer_en)

    return {
        "question": clean_question,
        "question_english": english_question,
        "answer_english": answer_en,
        "answer_target_lang": answer_target,
        # Backwards compatibility fields for original frontend
        "answer_telugu": answer_target if target_lang == "te-IN" else DEMO_RESPONSES.get(matches[0]["id"] if matches else "", {}).get("te-IN", answer_en),
        "target_language_code": target_lang,
        "target_language_name": SUPPORTED_LANGUAGES[target_lang]["name"],
        "sources": [s["title"] for s in matched_sources],
        "detailed_sources": matched_sources,
        "mode": "live" if sarvam_client else "demo",
    }

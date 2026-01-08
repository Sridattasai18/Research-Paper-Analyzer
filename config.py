import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Initialize the new GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "data", "pdfs")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "data", "vectordb")

# Ensure directories exist
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# RAG Settings
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100
TOP_K = 5
EMBEDDING_MODEL = "text-embedding-004"
GENERATIVE_MODEL = "gemini-flash-latest"

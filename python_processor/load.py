import nltk
import whisper
from sentence_transformers import SentenceTransformer

nltk.download("punkt_tab")
model = whisper.load_model("base")
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

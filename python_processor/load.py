import nltk
import whisper
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer

nltk.download("punkt_tab")
model = whisper.load_model("base")
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
model = T5ForConditionalGeneration.from_pretrained("UrukHan/t5-russian-spell")
tokenizer = T5Tokenizer.from_pretrained("UrukHan/t5-russian-spell")

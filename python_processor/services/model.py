import nltk
import numpy as np
import os
from razdel import sentenize
import re
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer

from schemas import Stamp, ExtendedStamp

nltk.download("punkt_tab")


class TextSplitter:
    def __init__(self, threshold=0.3, window_size=3):
        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.threshold = threshold
        self.window_size = window_size

    def calculate_cosine(self, vec1: np.ndarray, vec2: np.ndarray):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def sentenize(self, text: list[ExtendedStamp]) -> list[Stamp]:
        full_text = "".join([i.text for i in text])

        sentences_with_timestamps = []
        for sentence in map(
            lambda x: ExtendedStamp(
                start_sym=x.start, end_sym=x.stop, text=x.text, start=-1, end=-1
            ),
            sentenize(full_text),
        ):
            stamp = Stamp(start=-1, end=-1, text=sentence.text)
            for src_stamp in text:
                if (
                    sentence.start_sym >= src_stamp.start_sym
                    and sentence.start_sym < src_stamp.end_sym
                ):
                    stamp.start = src_stamp.start
                if (
                    sentence.start_sym >= 0
                    and sentence.end_sym <= src_stamp.end_sym
                    and sentence.end_sym > src_stamp.start_sym
                ):
                    stamp.end = src_stamp.end
                    sentences_with_timestamps.append(stamp)
                    break
        return sentences_with_timestamps

    def get_embeddings(self, stamps: list[Stamp]) -> list:
        embeddings = []
        batch_size = 100
        for i in range(0, len(stamps), batch_size):
            batch = stamps[i : i + batch_size]
            batch_embeddings = self.model.encode([stamp.text for stamp in batch])
            embeddings.extend(batch_embeddings)
        return embeddings

    def chunking(self, stamps: list[Stamp], embeddings: list) -> list[list[Stamp]]:
        chunks = []
        current_chunk = [stamps[0]]
        for i in range(1, len(embeddings)):
            similarity = self.calculate_cosine(embeddings[i - 1], embeddings[i])

            start_idx = max(0, i - self.window_size)
            window_similarity = (
                np.mean(
                    [
                        self.calculate_cosine(embeddings[j], embeddings[j + 1])
                        for j in range(start_idx, i)
                    ]
                )
                if i > 0
                else 1.0
            )

            if similarity < (window_similarity - self.threshold):
                chunks.append(current_chunk)
                current_chunk = [stamps[i]]
            else:
                current_chunk.append(stamps[i])
        chunks.append(current_chunk)

        return chunks

    def process_text(self, text: list[ExtendedStamp]) -> list[Stamp]:
        stamps = self.sentenize(text)
        embeddings = self.get_embeddings(stamps)
        chunks = self.chunking(stamps, embeddings)

        new_chunks = list(
            map(
                lambda chunk: Stamp(
                    start=chunk[0].start,
                    end=chunk[-1].end,
                    text=" ".join((j.text for j in chunk)),
                ),
                chunks,
            )
        )

        return new_chunks


class TextProcessor:

    def __init__(
        self, threshold: float = 0.3, window_size: int = 3, model_path="./model"
    ):
        self.splitter = TextSplitter(threshold=threshold, window_size=window_size)
        self.tokenizer = T5Tokenizer.from_pretrained(model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        self.model.eval()

    def process_chunk(self, chunk: Stamp) -> Stamp:
        inputs = self.tokenizer(chunk.text, return_tensors="pt")
        outputs = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=512,
        )
        return Stamp(
            start=chunk.start,
            end=chunk.end,
            text=self.tokenizer.decode(outputs[0], skip_special_tokens=True),
        )

    def process_text(self, text: list[ExtendedStamp]) -> list[Stamp]:
        chunks = self.splitter.process_text(text)
        # processed = []
        # for i in range(len(chunks) - 2):
        #     txt = " ".join(chunks[i : i + 2])
        #     processed.append(self.process_chunk(txt))

        processed = [self.process_chunk(chunk) for chunk in chunks]
        return processed


class SummarizeService:
    def __init__(self, model_path: str):
        self.model_path = model_path
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found in {model_path}")

    def __first_non_whitespace_index(s):
        match = re.search(r"\S", s)
        return match.start() if match else -1

    def format_time(seconds: int) -> str:
        hours = seconds // 3600
        remaining = seconds % 3600
        minutes = remaining // 60
        seconds_remaining = remaining % 60
        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds_remaining:02}"
        else:
            return f"{minutes:02}:{seconds_remaining:02}"

    def format_stamps(stamps: list[Stamp]) -> str:
        return "\n".join(
            map(
                lambda x: f"{SummarizeService.format_time(int(x.start))} - {SummarizeService.format_time(int(x.end))}: {x.text}",  # noqa
                stamps,
            )
        )

    def summarize_video(self, data: dict) -> list[Stamp]:
        stamps: list[ExtendedStamp] = []
        cur_sym = 0
        for i in data["segments"]:
            stamps.append(
                ExtendedStamp(
                    start_sym=SummarizeService.__first_non_whitespace_index(i["text"])
                    + cur_sym,
                    end_sym=cur_sym + len(i["text"]),
                    start=i["start"],
                    end=i["end"],
                    text=i["text"],
                )
            )
            cur_sym += len(i["text"])

        processor = TextProcessor(
            threshold=0.2, window_size=4, model_path=self.model_path
        )

        result = processor.process_text(stamps)
        return result

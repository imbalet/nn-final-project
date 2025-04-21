from fastapi import FastAPI, Request, HTTPException  # Добавлен HTTPException
from fastapi.middleware.cors import CORSMiddleware
import whisper
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_video(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt)

# Получаем поток с разрешением 360p
    stream = yt.streams.filter(res="360p", file_extension="mp4").first()

    if stream:
    # Скачиваем видео с указанием имени файла
        stream.download(filename="video.mp4")
        print("Видео успешно скачано как video.mp4")
    else:
        print("Поток с разрешением 360p не найден")

def transcribe_audio(model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe("video.mp4")
    return result["text"]

@app.post("/process_video")
async def process_video(request: Request):
    try:
        data = await request.json()
        url = data.get("url", "").strip()
        
        if not url:
            raise HTTPException(status_code=400, detail="URL не может быть пустым")
        
        if "youtube.com" not in url and "youtu.be" not in url:
            raise HTTPException(status_code=400, detail="Некорректный URL YouTube")

        print(f"Скачиваем видео: {url}")
        download_video(url)
        
        print("Транскрибируем...")
        transcription = transcribe_audio()
        
        return {"transcription": transcription}
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки видео: {str(e)}")
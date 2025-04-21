from pytubefix import YouTube
from pytubefix.cli import on_progress
import whisper
import os

def download_video(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt)

# Получаем поток с разрешением 360p
    stream = yt.streams.filter(res="360p", file_extension="mp4").first()

    if stream:
        output_path = "backend"
        stream.download(output_path=output_path,
                        filename="video.mp4")
        print("Видео успешно скачано как video.mp4")
    else:
        print("Поток с разрешением 360p не найден")


def transcribe_audio(model_name="base"):
    model = whisper.load_model(model_name)  # 'tiny', 'base', 'small', 'medium', 'large'
    result = model.transcribe("backend/video.mp4")
    
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print("Транскрипция готова! Результат в transcription.txt")
    return result["text"]

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=uHgt8giw1LY"
    
    print("Скачиваем видео...")
    download_video(video_url)
    
    print("Запускаем Whisper...")
    transcribed_text = transcribe_audio(model_name="base") 
    
    print("\nТекст из видео:")
    print(transcribed_text)
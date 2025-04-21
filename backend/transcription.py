#pip install openai-whisper  
#pip install ffmpeg-python  
#pip install yt-dlp

import yt_dlp
import whisper
import os
import ffmpeg

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]',
        'outtmpl': 'video.mp4',
        'merge_output_format': 'mp4',
        'cookiefile': 'cookies.txt',  
        'overwrites': True,
        'keepvideo': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio(model_name="base"):
    model = whisper.load_model(model_name)  # 'tiny', 'base', 'small', 'medium', 'large'
    result = model.transcribe("video.mp4")
    
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
import yt_dlp
import tkinter as tk
from tkinter import simpledialog

def download_youtube_video(video_url, save_path):
    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Configurando a janela pop-up
root = tk.Tk()
root.withdraw()  # Esconde a janela principal

# Solicita a URL do vídeo via pop-up
video_url = simpledialog.askstring("Input", "Digite a URL do vídeo do YouTube:")

# Verifica se o usuário forneceu uma URL
if video_url:
    save_path = r'C:\Users\scara\OneDrive - PRODESP\AURORA\YouTube\vídeos'  # Caminho de salvamento
    download_youtube_video(video_url, save_path)
else:
    print("Nenhuma URL foi fornecida.")

# Fecha a aplicação Tkinter
root.quit()



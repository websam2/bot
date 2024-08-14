import yt_dlp
import tkinter as tk
from tkinter import simpledialog, ttk
import re

def download_youtube_video(video_url, save_path):
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str'])
            percent = float(percent_str.strip('%'))
            progress_var.set(percent)
            root.update_idletasks()

    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',  # Especifica que o vídeo deve ser convertido para MP4
        'progress_hooks': [progress_hook],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Configurando a janela principal
root = tk.Tk()
root.title("Download de Vídeo do YouTube")
root.geometry("400x150")

# Variável que irá armazenar o progresso
progress_var = tk.DoubleVar()

# Barra de progresso
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, padx=20, fill=tk.X)

# Solicita a URL do vídeo via pop-up
video_url = simpledialog.askstring("Input", "Digite a URL do vídeo do YouTube:", parent=root)

# Verifica se o usuário forneceu uma URL
if video_url:
    save_path = r'C:\Users\scara\OneDrive - PRODESP\AURORA\YouTube'
    download_youtube_video(video_url, save_path)
else:
    print("Nenhuma URL foi fornecida.")

# Fecha a aplicação Tkinter
root.quit()





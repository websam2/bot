import yt_dlp
import tkinter as tk
from tkinter import simpledialog, filedialog
import re

def download_youtube_video(video_url, save_path, quality):
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str'])
            percent = float(percent_str.strip('%'))
            progress_label.config(text=f"Progresso: {percent:.1f}%")
            root.update_idletasks()

    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def start_download():
    video_url = simpledialog.askstring("Input", "Digite a URL do vídeo do YouTube:", parent=root)
    if video_url:
        save_path = filedialog.askdirectory(title="Escolha a pasta para salvar o vídeo")
        if save_path:
            progress_label.pack(pady=10)
            label.pack(pady=10)
            download_youtube_video(video_url, save_path, quality_var.get())
        else:
            print("Nenhuma pasta foi selecionada.")
    else:
        print("Nenhuma URL foi fornecida.")
    root.quit()

root = tk.Tk()
root.title("Download de Vídeo do YouTube")
root.geometry("400x300")

quality_var = tk.StringVar(value="1080")

label_quality = tk.Label(root, text="Escolha a resolução:")
label_quality.pack(pady=10)

radio_720p = tk.Radiobutton(root, text="720p", variable=quality_var, value="720")
radio_720p.pack(pady=5)

radio_1080p = tk.Radiobutton(root, text="1080p", variable=quality_var, value="1080")
radio_1080p.pack(pady=5)

start_button = tk.Button(root, text="Iniciar Download", command=start_download)
start_button.pack(pady=20)

progress_label = tk.Label(root, text="Progresso: 0%")

label = tk.Label(root, text="Por favor, aguarde ;)")

root.mainloop()

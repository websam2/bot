from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import re

app = Flask(__name__)

progress = 0
download_path = ''

DOWNLOAD_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    global progress, download_path
    video_url = request.form['video_url']
    quality = request.form['quality']
    format_type = request.form['format']  # Novo parâmetro para o formato
    
    def progress_hook(d):
        global progress
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%')
            clean_percent = re.sub(r'\x1b\[[0-9;]*[mG]', '', percent_str)
            progress = float(clean_percent.strip('%'))

    if format_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }
    else:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(title)s.%(ext)s'),
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        downloaded_files = os.listdir(DOWNLOAD_DIRECTORY)
        if not downloaded_files:
            raise Exception("Nenhum arquivo foi baixado")
        
        downloaded_file = downloaded_files[-1]
        download_path = os.path.join(DOWNLOAD_DIRECTORY, downloaded_file)
        
        print(f"Arquivo baixado: {download_path}")
        
        return jsonify({'success': True, 'message': 'Download concluído', 'filename': downloaded_file})
    except Exception as e:
        print(f"Erro durante o download: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/progress')
def get_progress():
    global progress
    return jsonify({'progress': progress})

@app.route('/get_file')
def get_file():
    global download_path
    print(f"Tentando enviar o arquivo: {download_path}")
    if os.path.exists(download_path):
        return send_file(download_path, as_attachment=True)
    else:
        return jsonify({'error': 'Arquivo não encontrado'}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
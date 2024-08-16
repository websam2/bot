from flask import Flask, render_template, request, jsonify, send_file, redirect
import requests
import os

app = Flask(__name__)

progress = 0
download_path = ''

# URL do servidor proxy no Railway
PROXY_URL = "https://proxy-teste.up.railway.app/proxy_download"

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

    # Envia os dados para o servidor proxy no Railway
    proxy_payload = {
        'video_url': video_url,
        'quality': 'audio' if format_type == 'audio' else quality
    }

    try:
        proxy_response = requests.post(PROXY_URL, json=proxy_payload)
        proxy_data = proxy_response.json()

        # Verifica se a resposta contém sucesso e uma URL de download válida
        if not proxy_data.get('success', False):
            raise Exception(proxy_data.get('error', 'Erro desconhecido'))

        download_url = proxy_data.get('download_url', None)
        title = proxy_data.get('title', 'arquivo_desconhecido')

        # Verifica se a URL de download está presente e válida
        if not download_url:
            raise ValueError("URL de download não encontrada na resposta do proxy.")

        # Opcional: baixar o arquivo na Vercel ou redirecionar para o link
        download_path = os.path.join(DOWNLOAD_DIRECTORY, f"{title}.mp4" if format_type != 'audio' else f"{title}.mp3")

        # Baixa o arquivo diretamente do link fornecido pelo proxy
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(download_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"Arquivo baixado: {download_path}")

        return jsonify({'success': True, 'message': 'Download concluído', 'filename': os.path.basename(download_path)})
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

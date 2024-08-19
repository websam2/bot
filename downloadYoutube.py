from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

# URL do servidor proxy no Railway
PROXY_URL = "https://proxy-teste.up.railway.app/proxy_download"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    quality = request.form['quality']
    format_type = request.form['format']  # Novo parâmetro para o formato

    proxy_payload = {
        'video_url': video_url,
        'quality': 'audio' if format_type == 'audio' else quality
    }

    try:
        # Envia os dados para o servidor proxy no Railway
        proxy_response = requests.post(PROXY_URL, json=proxy_payload)
        proxy_data = proxy_response.json()

        # Verifica se a resposta contém sucesso e uma URL de download válida
        if not proxy_data.get('success', False):
            raise Exception(proxy_data.get('error', 'Erro desconhecido'))

        download_url = proxy_data.get('download_url', None)

        # Verifica se a URL de download está presente e válida
        if not download_url:
            raise ValueError("URL de download não encontrada na resposta do proxy.")

        # Redireciona o usuário para a URL de download
        return redirect(download_url)
    except Exception as e:
        print(f"Erro durante o download: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    import yt_dlp
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id'}), 400
    output_dir = 'downloads'
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
            'ffmpeg_location': 'ffmpeg',
        'quiet': True,
        'noplaylist': True,
    }
    url = f'https://www.youtube.com/watch?v={video_id}'
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', video_id)
            mp3_filename = os.path.join(output_dir, f"{title}.mp3")
            if not os.path.exists(mp3_filename):
                return jsonify({'error': 'No se pudo encontrar el archivo mp3'}), 500
            return send_file(mp3_filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error al iniciar Flask: {e}")

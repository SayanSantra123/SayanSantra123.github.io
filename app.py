"""
SSTV Web Server - Flask Application
Run SSTV encoder/decoder through web interface
"""

from flask import Flask, render_template, request, send_file, jsonify
import os
import base64
from werkzeug.utils import secure_filename
from data_encoder import DataEncoder
from data_decoder import DataDecoder
from crypto_handler import CryptoHandler
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    """Encode file to audio"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        encryption_key = request.form.get('key', None)
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Read file data
        with open(input_path, 'rb') as f:
            file_data = f.read()
        
        # Encrypt if key provided
        if encryption_key and encryption_key.strip():
            crypto = CryptoHandler(encryption_key)
            iv = get_random_bytes(16)
            cipher = AES.new(crypto.key, AES.MODE_CBC, iv)
            padded_data = pad(file_data, AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            final_data = iv + encrypted_data
            encrypted = True
        else:
            final_data = file_data
            encrypted = False
        
        # Generate audio
        encoder = DataEncoder()
        output_filename = f"{os.path.splitext(filename)[0]}.wav"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        encoder.encode(final_data, output_path=output_path)
        
        # Clean up input file
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'encrypted': encrypted,
            'download_url': f'/download/{output_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decode', methods=['POST'])
def decode():
    """Decode audio to file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400
        
        file = request.files['file']
        decryption_key = request.form.get('key', None)
        output_format = request.form.get('format', 'bin')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded audio
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Decode audio
        decoder = DataDecoder()
        decoded_data = decoder.decode(input_path)
        
        # Decrypt if key provided
        if decryption_key and decryption_key.strip():
            crypto = CryptoHandler(decryption_key)
            iv = decoded_data[:16]
            encrypted_data = decoded_data[16:]
            cipher = AES.new(crypto.key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(encrypted_data)
            final_data = unpad(decrypted_padded, AES.block_size)
            decrypted = True
        else:
            final_data = decoded_data
            decrypted = False
        
        # Save decoded file
        output_filename = f"decoded_{os.path.splitext(filename)[0]}.{output_format}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        with open(output_path, 'wb') as f:
            f.write(final_data)
        
        # Clean up input file
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'decrypted': decrypted,
            'download_url': f'/download/{output_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    """Download generated file"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

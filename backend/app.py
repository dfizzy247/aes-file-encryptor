from flask import Flask, request, jsonify, send_file
from .crypto_utils import encrypt_file, decrypt_file, log_event 
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/encrypt', methods=['POST'])
def encrypt_endpoint():
    """Handles file encryption request."""
    file = request.files.get('file')
    password = request.form.get('password')
    output_path = request.form.get('output_path')

    if not file or not password:
        return jsonify({'error': 'Missing file or password'}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    if not output_path:
        output_path = input_path + ".enc"

    try:
        encrypt_file(input_path, password, output_path)
        # Encryption
        log_event("ENCRYPTION", file.filename, "SUCCESS", output_path)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        # On failure, you can pass None or the attempted output path
        log_event("ENCRYPTION", file.filename, f"FAILED - {str(e)}", output_path)
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_endpoint():
    """Handles file decryption request and restores the original extension."""
    file = request.files.get('file')
    password = request.form.get('password')
    output_path = request.form.get('output_path')

    if not file or not password:
        return jsonify({'error': 'Missing file or password'}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    if not output_path:
        output_path = os.path.join(UPLOAD_FOLDER, "decrypted_file")

    try:
        result = decrypt_file(input_path, password, output_path)
        if result:
            # Decryption
            log_event("DECRYPTION", file.filename, "SUCCESS", result)
            # Use the correct filename in the response
            return send_file(
                result,
                as_attachment=True,
                download_name=os.path.basename(result)  # Flask >=2.0
            )
        else:
            log_event("DECRYPTION", file.filename, "FAILED - Incorrect password or corrupted file", output_path)
            return jsonify({'error': 'Decryption failed, incorrect password or corrupted file'}), 400
    except Exception as e:
        log_event("DECRYPTION", file.filename, f"FAILED - {str(e)}", output_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

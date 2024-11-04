from gtts import gTTS
from flask_cors import CORS
from apps import app,model,history
from flask import request,jsonify, send_from_directory
from apps import upload_to_gemini
import os
import re
import json

# Enable CORS for all routes
CORS(app, resources={
    r"/pictures": {"origins": "http://localhost:5173"},
    r"/data/*": {"origins": "http://localhost:5173"}
})
def detect_language(text):
    """Function to detect if the text is French or English."""
    if re.search(r'[àâçéèêëîôû]', text): 
        return 'fr'
    else:
        return 'en'

"""
@app.route('/count-signatures', methods=['POST'])
def count_signatures_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    print(request.files)
    
    file = request.files['file']
    file_path = os.path.join('data', file.filename)
    file.save(file_path)

    #Send to gemini
    gemini_file = upload_to_gemini(file_path, mime_type="image/jpeg")

    #append history
    history.append({
         "role": "user",
        "parts": [
            gemini_file
        ],
    })

    #call model chat session
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message("Compter les signatures dans le fichier")

    # Appeler la fonction de comptage
    #count = count_signatures(file_path)
    return jsonify({'file_path': file_path, 'signature_count': 'count', 'model_response': response.text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
"""

@app.route('/pictures', methods=['POST'])
def pictures_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    print(request.files)
    
    file = request.files['file']
    file_path = os.path.join('data', file.filename)
    file.save(file_path)

    #Send to gemini
    gemini_file = upload_to_gemini(file_path, mime_type="image/jpeg")

    #append history
    history.append({
         "role": "user",
        "parts": [
            gemini_file
        ],
    })

    #call model chat session
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message("Quel image se trouve dans cette image?")

    #Define response_text after obtaining the response
    response_text = response.text

    response_dict = json.loads(response_text)  # Parse the JSON response
    words_to_read = []
    if isinstance(response_dict, dict):
        for key, value in response_dict.items():
            for key, value in response_dict.items():
                # Handle string values
                    if isinstance(value, str):
                        words_to_read.append(value)
                # Handle list values
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, str):
                                words_to_read.append(item)
                            elif isinstance(item, dict):
                                # Assuming the dict may contain a 'text' key or similar
                                if 'text' in item:
                                    words_to_read.append(item['text'])
                        else:
                            # If you want to log or handle dicts without 'text' key
                            print("Skipping dict without 'text' key:", item)

    words_string = ', '.join(words_to_read)

    #Determine the language of the response
    language = detect_language( words_string)
    print(f'Detected language: {language}')  # Affiche la langue détectée
    print(f'Words to read: {words_string}')   # Affiche le texte à lire

    #Get audio
    audio_file_path = os.path.join('data', f'response_{language}.mp3')

    #Use a conditional to generate audio only if there is text
    if words_string.strip():  # Check if the string is not empty
        tts = gTTS(text=words_string, lang=language)
        tts.save(audio_file_path)
        print("Audio file created successfully:", audio_file_path)
    else:
        print("No text available for audio generation.")

    return jsonify({
        'file_path': file_path,
        'pictures': 'pictures',
        'model_response': words_string,
        'audio_file_path': audio_file_path,
        'audio_file_url': f'http://127.0.0.1:5000/data/response_{language}.mp3'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/data/<path:filename>', methods=['GET'])
def serve_audio(filename):
    file_path = os.path.join('data', filename)
    print(f"Trying to serve audio from: {file_path}")
    if os.path.exists(file_path):
        return send_from_directory('data', filename)
    else:
        return jsonify({"error": "File not found"}), 404
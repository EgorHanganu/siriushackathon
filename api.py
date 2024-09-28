from flask import Flask, request, jsonify
import socket
import config
import re
import time
import pypdf
import openai
import json
import os
from spire.doc import *
from spire.doc.common import *

app = Flask(__name__)

EXTENSIONS = ["doc", "docx", "pdf"]

def get_404(reason: str):
    return {"reason": reason, "code": 404}, 404

os.makedirs(config.OUTPUT_FOLDER_PATH, exist_ok=True)

def require_api_key(f): # TEMPORARY SECURITY FUNCTION FOR DEMO PURPOSES
    def wrapped_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key and api_key == config.INTERNAL_API_KEY:
            return f(*args, **kwargs)
        response = jsonify({"error": "Unauthorized", "message": "Invalid or missing API key"})
        response.status_code = 401
        return response
    wrapped_function.__name__ = f.__name__ 
    return wrapped_function

@app.route('/upload', methods=['POST'])
@require_api_key
def upload_file():
    if 'file' not in request.files:
        return get_404("No file part in the request")
    
    file = request.files['file']
   
    if not file.filename:
        return get_404("No selected file")
    
    filename = file.filename.strip().lower()
    matches = re.findall(r'[^.]+$', filename) 

    if not matches:
        return get_404("Unsupported extension.")
    
    if not file:
        return get_404("Unexpected error.")
    
    ai_response = str()
    extension = matches[0]
    filename_tmp = config.OUTPUT_FOLDER_PATH + "/" + str(int(time.time() * 100)) + "." + extension
    file.save(filename_tmp)

    if extension in ("docx", "doc"):
        document = Document()
        document.LoadFromFile(filename_tmp)
        text = re.sub(r'^.*?\r', '', document.GetText(), count=1).strip()

    if extension == "pdf":
        text = str()
        reader = pypdf.PdfReader(filename_tmp)
        for page in reader.pages:
            text += page.extract_text().replace(" -", "-") + "\n"
    
    if text:
        client = openai.Client(api_key=config.OPENAI_API_KEY)
        for i in range(3):
            
            choices = client.chat.completions.create(model="gpt-4-turbo",
                                        messages=[{"role": "user", "content": text + config.AI_PROMPT}]).choices
            if choices:
                try:
                    ai_response = json.loads(choices[0].message.content)
                    break
                except json.decoder.JSONDecodeError:
                    pass
                except:
                    return get_404("Unexpected error. Try again.")

    os.remove(filename_tmp)
    return {"result": ai_response}

if __name__ == '__main__':
    app.run(host=socket.gethostbyname(socket.gethostname()), port=54128, debug=True)
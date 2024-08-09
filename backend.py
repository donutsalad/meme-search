from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pickle
from transformers import AutoTokenizer, SiglipTextModel
from sentence_transformers import util
import os
import signal
import subprocess

index_file = "complete_memes.imgidx"

app = Flask(__name__)
CORS(app)  # this will enable CORS for all routes

print("Loading indexed data")
with open(index_file, 'rb') as indexed:
    saved_data = pickle.load(indexed)

print("Loaded indexed data...\nLoading Neural Networks")

model = SiglipTextModel.from_pretrained("google/siglip-base-patch16-224")
tokenizer = AutoTokenizer.from_pretrained("google/siglip-base-patch16-224")

def cosine_to_confidence(cosine_similarity):
    """Converts cosine similarity into a more user-friendly confidence score"""
    cosine_similarity = max(0, cosine_similarity)  # Ensure non-negative
    if cosine_similarity > 0.1:
        return 100 * (cosine_similarity ** 0.1)
    else:
        return 100 * (cosine_similarity ** 0.2)

def get_top_results(query, top_n=25):
    inputs = tokenizer(query, padding="max_length", return_tensors="pt")
    outputs = model(**inputs)
    pooled_output = outputs.pooler_output

    similarities = []
    for img in saved_data:
        similarity = util.pytorch_cos_sim(pooled_output, img["tensor"][0])
        confidence = cosine_to_confidence(similarity.item())
        similarities.append({"filepath": img["filepath"], "confidence": confidence})

    results = sorted(similarities, key=lambda x: x["confidence"], reverse=True)
    return results[:top_n]

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    top_n = data.get('top_n', 25)  # default to 25 if not provided
    results = get_top_results(query, top_n)
    return jsonify({"results": results})

@app.route('/image')
def get_image():
    filepath = request.args.get('filepath')
    return send_file(filepath, mimetype='image/jpeg')

def kill_process_on_port(port):
    """Kill process running on a given port."""
    result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
    if result.stdout:
        pid = result.stdout.split('\n')[1].split()[1]  # Extract PID from the output
        os.kill(int(pid), signal.SIGKILL)
        
def start_react_app():
    """Starts the React app using subprocess"""
    if os.environ.get("FLASK_RUN_FROM_CLI") != "true":  # Only start if not running from Flask CLI
        kill_process_on_port(3000)  # Kill any process on port 3000
        react_app_path = './meme_search'
        subprocess.Popen(['npm', 'start'], cwd=react_app_path)

if __name__ == "__main__":
    start_react_app()  # Start the React app
    app.run(debug=True)
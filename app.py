# ----------------------------------------------------------------WORKING

# import os
# import torch
# import cv2
# import numpy as np
# from flask import Flask, render_template, request, jsonify, send_from_directory
# from ViolenceDetectionModel import ViolenceDetectionModel
# from torchvision import transforms

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # Load Model
# MODEL = 'violence_detection_model.pth'
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = ViolenceDetectionModel().to(device)
# model.load_state_dict(torch.load(MODEL, map_location=device))
# model.eval()

# # Define Transform
# transform = transforms.Compose([
#     transforms.ToPILImage(),
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.5], std=[0.5])
# ])

# def extract_frames(video_path, sequence_length=30):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         raise FileNotFoundError(f"Error opening video file: {video_path}")

#     frames = []
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     frame_interval = max(1, total_frames // sequence_length)

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if len(frames) % frame_interval == 0:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame = transform(frame)
#             frames.append(frame)
#         if len(frames) >= sequence_length:
#             break

#     cap.release()

#     # Pad if frames are less than sequence_length
#     while len(frames) < sequence_length:
#         frames.append(frames[-1])

#     return torch.stack(frames).unsqueeze(0).to(device)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'})
#     if not file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
#         return jsonify({'error': 'Invalid file format. Only .mp4, .avi, or .mov allowed.'})

#     filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#     file.save(filename)
#     return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

# @app.route('/video/<filename>')
# def video_file(filename):
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     if not os.path.isfile(filepath):
#         return jsonify({'error': 'Video not found'}), 404
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     filename = data.get('filename')
#     if not filename:
#         return jsonify({'error': 'Filename not provided'}), 400

#     video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     if not os.path.isfile(video_path):
#         return jsonify({'error': 'Video not found'}), 404

#     try:
#         frames = extract_frames(video_path)
#         with torch.no_grad():
#             output = model(frames)
#             prediction = "Fight" if output.item() > 0.5 else "No Fight"
#         return jsonify({'prediction': prediction})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
































# --------------------------------------------------- WORKING ( NOW SUPPORT avi/mp4)


import os
import torch
import cv2
import subprocess
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory
from ViolenceDetectionModel import ViolenceDetectionModel
from torchvision import transforms

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load Model
MODEL = 'violence_detection_model.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ViolenceDetectionModel().to(device)
model.load_state_dict(torch.load(MODEL, map_location=device))
model.eval()

# Define Transform
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

def convert_avi_to_mp4(avi_path):
    """Converts an AVI file to MP4 format."""
    mp4_path = avi_path.rsplit('.', 1)[0] + ".mp4"
    
    command = [
        "ffmpeg", "-i", avi_path, "-c:v", "libx264", "-preset", "fast", 
        "-crf", "22", "-c:a", "aac", "-b:a", "128k", mp4_path, "-y"
    ]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(avi_path)  # Remove the original AVI file after conversion
        return mp4_path
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        return None

def extract_frames(video_path, sequence_length=30):
    """Extracts frames from a video for model inference."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Error opening video file: {video_path}")

    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(1, total_frames // sequence_length)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if len(frames) % frame_interval == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = transform(frame)
            frames.append(frame)
        if len(frames) >= sequence_length:
            break

    cap.release()

    # Pad if frames are less than sequence_length
    while len(frames) < sequence_length:
        frames.append(frames[-1])

    return torch.stack(frames).unsqueeze(0).to(device)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles video uploads and converts AVI to MP4 if needed."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        return jsonify({'error': 'Invalid file format. Only .mp4, .avi, or .mov allowed.'})

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Convert AVI to MP4 if needed
    if filename.lower().endswith('.avi'):
        converted_path = convert_avi_to_mp4(filename)
        if not converted_path:
            return jsonify({'error': 'Failed to convert AVI to MP4'})
        filename = converted_path  # Update filename to the converted MP4

    return jsonify({'message': 'File uploaded successfully', 'filename': os.path.basename(filename)})

@app.route('/video/<filename>')
def video_file(filename):
    """Serves the uploaded videos."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(filepath):
        return jsonify({'error': 'Video not found'}), 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/predict', methods=['POST'])
def predict():
    """Handles violence detection prediction."""
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'Filename not provided'}), 400

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(video_path):
        return jsonify({'error': 'Video not found'}), 404

    try:
        frames = extract_frames(video_path)
        with torch.no_grad():
            output = model(frames)
            prediction = "Fight" if output.item() > 0.5 else "No Fight"
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

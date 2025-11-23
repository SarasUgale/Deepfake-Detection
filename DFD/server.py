from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import torch
from torch import nn
from torchvision import models, transforms
import numpy as np
import cv2
import face_recognition
import warnings
warnings.filterwarnings("ignore")

UPLOAD_FOLDER = 'Celeb-DF-v2'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Model(nn.Module):
    def __init__(self, num_classes, latent_dim=2048, lstm_layers=1, hidden_dim=2048, bidirectional=False):
        super(Model, self).__init__()
        model = models.resnext50_32x4d(pretrained=True)
        self.model = nn.Sequential(*list(model.children())[:-2])
        self.lstm = nn.LSTM(latent_dim, hidden_dim, lstm_layers, bidirectional)
        self.relu = nn.LeakyReLU()
        self.dp = nn.Dropout(0.4)
        self.linear1 = nn.Linear(2048, num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        batch_size, seq_length, c, h, w = x.shape
        x = x.view(batch_size * seq_length, c, h, w)
        fmap = self.model(x)
        x = self.avgpool(fmap)
        x = x.view(batch_size, seq_length, 2048)
        x_lstm, _ = self.lstm(x, None)
        return fmap, self.dp(self.linear1(x_lstm[:, -1, :]))

sm = nn.Softmax(dim=1)

class ValidationDataset(torch.utils.data.Dataset):
    def __init__(self, video_names, sequence_length=60, transform=None):
        self.video_names = video_names
        self.transform = transform
        self.count = sequence_length

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, idx):
        video_path = self.video_names[idx]
        frames = []
        a = int(100 / self.count)
        for i, frame in enumerate(self.frame_extract(video_path)):
            faces = face_recognition.face_locations(frame)
            try:
                top, right, bottom, left = faces[0]
                frame = frame[top:bottom, left:right, :]
            except IndexError:
                pass
            if self.transform:
                frame = self.transform(frame)
            frames.append(frame)
            if len(frames) == self.count:
                break
        frames = torch.stack(frames)
        frames = frames[:self.count]
        return frames.unsqueeze(0)

    def frame_extract(self, path):
        vidObj = cv2.VideoCapture(path)
        success = True
        while success:
            success, image = vidObj.read()
            if success:
                yield image

def predict(model, img):
    fmap, logits = model(img)
    logits = sm(logits)
    _, prediction = torch.max(logits, 1)
    confidence = logits[:, int(prediction.item())].item() * 100
    return int(prediction.item()), confidence

def detectFakeVideo(videoPath):
    im_size = 112
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    train_transforms = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((im_size, im_size)), 
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])

    video_dataset = ValidationDataset([videoPath], sequence_length=20, transform=train_transforms)
    model = Model(2)
    model.load_state_dict(torch.load('model/df_model.pt', map_location=torch.device('cpu')))
    model.eval()

    prediction = predict(model, video_dataset[0])
    return prediction

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'GET':
        return render_template('detect.html')

    if request.method == 'POST':
        video = request.files.get('video')
        if not video:
            return jsonify({'error': 'No video file uploaded'}), 400

        filename = secure_filename(video.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video.save(save_path)

        output_label, confidence = detectFakeVideo(save_path)
        os.remove(save_path)

        result = {
            'output': 'REAL' if output_label == 1 else 'FAKE',
            'confidence': confidence
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(result)

        return render_template('detect.html', data=result)

if __name__ == '__main__':
    app.run(port=3000, debug=True)

# Deepfake-Detection
🕵️‍♂️ Deepfake Detection System
AI-Powered Video Deepfake Classification with Flask (ResNeXt + LSTM)

This project is an end-to-end Deepfake Video Detection System that allows users to upload or drag-and-drop a video and receive a prediction (REAL or FAKE) along with a confidence score.
It uses ResNeXt (CNN) for spatial feature extraction and LSTM (RNN) for temporal sequence analysis of video frames.

🚀 Features

🎥 Drag & Drop Video Upload

🎛 Live Video Preview Before Upload

⚡ AJAX-based Detection (No page reload)

🧠 AI Model (ResNeXt + LSTM) for Deepfake detection

👤 Face Detection using face_recognition for better accuracy

📊 Confidence score output

🎨 Modern UI with animations, neon theme, and responsive layout

🔥 Flask backend with real-time file handling

🧠 Algorithms & Technologies Used
1. ResNeXt (Deep CNN)

•Extracts spatial features from each video frame

•Captures textures, edges, lighting inconsistencies

•Based on grouped convolutions & cardinality

•Great for detecting visual artifacts in deepfakes


2. LSTM (Long Short-Term Memory Network)

•Processes frames in sequence

•Detects unnatural facial movements (eye blinking, head jerks, lip sync issues)

•Good for temporal deepfake detection


3. Face Detection — face_recognition

•Detects and crops faces from frames

•Ensures the model focuses only on the important region

📂 Project Structure
```
Deepfake-Detection/
│── templates/
│      ├── base.html
│      ├── home.html
│      ├── detect.html
│
│── static/
│      ├── script.js
│      ├── style.css
│
│── model/
│      ├── df_model.pt   (Your trained model)
│
│── uploads/             (Auto-created for video uploads)
│
│── server.py / app.py   (Flask backend)
│── requirements.txt
│── README.md
```

🛠 Installation & Setup
1. Clone the repository
git clone https://github.com/yourusername/Deepfake-Detection.git
cd Deepfake-Detection

2. Install dependencies
pip install -r requirements.txt

3. Run the Flask server
python server.py

4. Open in browser
http://127.0.0.1:5000

🎯 How It Works (Pipeline)

•User uploads a video (drag & drop or button).

•Backend extracts frames using OpenCV.

•Face region is detected using face_recognition.

•Frames are passed through ResNeXt → extract spatial features.

•Sequence of frame features passed into LSTM → analyze motion patterns.

•Output layer predicts REAL or FAKE with confidence.

•Result is shown in a neon-styled UI panel.

📌 Why This Project?

Deepfakes represent one of the biggest threats in:

❗ Misinformation

❗ Political propaganda

❗ Identity fraud

❗ Cybersecurity

This system helps identify manipulated videos using AI and deep learning, making digital spaces safer.


🙌 Authors

Saras Ugale

⭐ If you found this helpful

Give the repository a star ⭐ on GitHub!

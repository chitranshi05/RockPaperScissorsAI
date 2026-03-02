# 🎮 Rock Paper Scissors AI

A real-time Rock Paper Scissors game powered by Computer Vision using OpenCV and MediaPipe.

This application detects hand gestures through a webcam and plays against the computer with a countdown system, score tracking, and structured UI.

---

## 🚀 Features

- ✋ Real-time hand gesture recognition
- ⏳ 3-second countdown before each round
- 🧠 Computer move revealed after countdown
- 🏆 First-to-5 win system
- 🔄 Reset functionality
- 🎨 Clean side-panel game UI
- 📊 Live score tracking

---

## 🛠 Tech Stack

- Python 3.11
- OpenCV
- MediaPipe
- NumPy
- Git & GitHub

---

## 🎯 How It Works

1. Webcam captures live video feed.
2. MediaPipe detects 21 hand landmarks.
3. Finger positions are analyzed to classify gestures:
   - ✊ Rock  
   - ✋ Paper  
   - ✌ Scissors  
4. After the countdown, the computer generates a random move.
5. Winner logic compares both moves.
6. Score updates dynamically on the UI panel.

---

## 🎮 Controls

| Key   | Action          |
|-------|-----------------|
| SPACE | Start new round |
| R     | Reset game      |
| ESC   | Exit game       |

---

## 📂 Project Structure

RockPaperScissorsAI/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

git clone https://github.com/YOUR_USERNAME/RockPaperScissorsAI.git
cd RockPaperScissorsAI

### 2️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate

### 3️⃣ Install Dependencies

pip install -r requirements.txt

### 4️⃣ Run the Project

python main.py

---

## 🧠 Learning Outcomes

- Real-time computer vision processing
- Hand landmark detection using MediaPipe
- Gesture classification logic
- Game state management
- UI design with OpenCV
- Version control using Git

---

## 💼 Resume Description

Developed a real-time AI-powered Rock-Paper-Scissors game using OpenCV and MediaPipe, implementing gesture recognition, countdown-based gameplay logic, and dynamic score tracking in a structured UI environment.

---

## 👩‍💻 Author

Chitranshi Singh  
B.Tech CSE (AI/ML)
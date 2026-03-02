# 🎮 Rock Paper Scissors AI

A real-time Rock Paper Scissors game powered by Computer Vision using OpenCV and MediaPipe.

This project detects hand gestures via webcam and plays Rock-Paper-Scissors against the computer with a countdown system, score tracking, and interactive UI.

---

## 🚀 Features

- ✋ Real-time hand gesture recognition
- ⏳ 3-second countdown before each round
- 🧠 Computer move revealed after countdown
- 🏆 First to 5 wins system
- 🔄 Reset functionality
- 🎨 Clean side-panel UI
- 📊 Live score tracking

---

## 🛠 Tech Stack

- Python 3.11
- OpenCV
- MediaPipe
- NumPy

---

## 🎯 How It Works

1. Webcam captures live video feed.
2. MediaPipe detects 21 hand landmarks.
3. Finger positions are analyzed to classify:
   - ✊ Rock
   - ✋ Paper
   - ✌ Scissors
4. After countdown, computer generates a random move.
5. Winner logic compares gestures.
6. Score updates in real-time.

---

## 🎮 Controls

| Key | Action |
|------|--------|
| SPACE | Start round |
| R | Reset game |
| ESC | Exit game |

---

## 📂 Project Structure

# 🎮 Rock Paper Scissors AR

A real-time Rock Paper Scissors game that uses **hand gesture recognition** through your webcam to play against the computer.

Built with **OpenCV** and **MediaPipe** for hand tracking and gesture detection.

---

## 🚀 Features

- Real-time hand gesture detection via webcam
- Recognizes Rock, Paper, and Scissors using finger tracking
- 3-second countdown before each round
- Score tracking (first to 5 wins)
- Reset and exit controls

---

## 🛠 Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

---

## 📦 Setup

### Requirements

- Python 3.8+
- A working webcam

### Installation

```bash
git clone https://github.com/ssgamingop/RockPaperScissorsAR.git
cd RockPaperScissorsAR
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## 🎮 Controls

| Key   | Action              |
|-------|---------------------|
| SPACE | Start a new round   |
| R     | Reset the game      |
| ESC   | Exit the program    |

---

## 🤚 How It Works

The game uses MediaPipe's hand landmark detection to track 21 points on your hand in real time. It determines which fingers are extended by comparing landmark positions:

- **Rock** → All fingers closed (0-1 fingers up)
- **Paper** → All fingers open (4-5 fingers up)
- **Scissors** → Only index and middle fingers extended

The thumb is detected separately using x-axis comparison since it bends sideways unlike the other fingers.

---

## 📂 Project Structure

```
RockPaperScissorsAR/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

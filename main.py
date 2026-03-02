import cv2
import mediapipe as mp
import numpy as np
import random
import time

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Game variables
choices = ["Rock", "Paper", "Scissors"]
player_score = 0
computer_score = 0

round_active = False
countdown_start = 0
countdown_duration = 3

gesture = "Unknown"
computer_choice = ""
result = ""

def get_gesture(handLms):
    fingers = []
    fingers.append(1 if handLms.landmark[8].y < handLms.landmark[6].y else 0)
    fingers.append(1 if handLms.landmark[12].y < handLms.landmark[10].y else 0)
    fingers.append(1 if handLms.landmark[16].y < handLms.landmark[14].y else 0)
    fingers.append(1 if handLms.landmark[20].y < handLms.landmark[18].y else 0)

    if fingers == [0,0,0,0]:
        return "Rock"
    elif fingers == [1,1,1,1]:
        return "Paper"
    elif fingers == [1,1,0,0]:
        return "Scissors"
    else:
        return "Unknown"

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (800, 600))

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Create white UI panel
    ui_panel = 255 * np.ones((600, 400, 3), dtype=np.uint8)
    img = np.hstack((frame, ui_panel))

    current_time = time.time()

    # Countdown Logic
    if round_active:
        elapsed = current_time - countdown_start
        remaining = countdown_duration - int(elapsed)

        if remaining > 0:
            cv2.circle(img, (400,300), 100, (0,0,255), -1)
            cv2.putText(img, str(remaining), (370,330),
                        cv2.FONT_HERSHEY_SIMPLEX, 3,
                        (255,255,255), 6)
        else:
            # Detect player gesture
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(img[:, :800], handLms, mp_hands.HAND_CONNECTIONS)
                    gesture = get_gesture(handLms)

            # Generate computer move AFTER countdown
            computer_choice = random.choice(choices)

            if gesture != "Unknown":
                if gesture == computer_choice:
                    result = "Draw"
                elif (gesture == "Rock" and computer_choice == "Scissors") or \
                     (gesture == "Scissors" and computer_choice == "Paper") or \
                     (gesture == "Paper" and computer_choice == "Rock"):
                    result = "You Win!"
                    player_score += 1
                else:
                    result = "Computer Wins!"
                    computer_score += 1
            else:
                result = "Invalid Move"

            round_active = False

    # Draw UI Boxes
    cv2.rectangle(img, (820, 50), (1180, 150), (200,200,200), 2)
    cv2.rectangle(img, (820, 180), (1180, 280), (200,200,200), 2)
    cv2.rectangle(img, (820, 310), (1180, 410), (200,200,200), 2)
    cv2.rectangle(img, (820, 440), (1180, 540), (200,200,200), 2)

    # Player Move
    cv2.putText(img, "YOUR MOVE", (880, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0,0,0), 2)

    cv2.putText(img, gesture, (900, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,150,0), 3)

    # Computer Move (only after round)
    cv2.putText(img, "COMPUTER", (880, 210),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0,0,0), 2)

    if not round_active:
        cv2.putText(img, computer_choice, (900, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (150,0,0), 3)

    # Result
    cv2.putText(img, "RESULT", (920, 340),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0,0,0), 2)

    cv2.putText(img, result, (860, 380),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,0,200), 3)

    # Score
    cv2.putText(img, "SCORE", (920, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0,0,0), 2)

    cv2.putText(img, f"{player_score}  -  {computer_score}", (920, 510),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,0,0), 3)

    # Game Winner
    if player_score == 5:
        cv2.putText(img, "YOU WON THE GAME!", (150,300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (0,255,0), 4)
    elif computer_score == 5:
        cv2.putText(img, "COMPUTER WON THE GAME!", (80,300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (0,0,255), 4)

    # Instructions
    cv2.putText(img, "SPACE = Play  |  R = Reset  |  ESC = Exit",
                (200,570), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (100,100,100), 2)

    cv2.imshow("Rock Paper Scissors AI", img)

    key = cv2.waitKey(1)

    if key == 32 and not round_active:
        if player_score < 5 and computer_score < 5:
            round_active = True
            countdown_start = time.time()
            gesture = "Unknown"
            result = ""
            computer_choice = ""

    if key == ord('r'):
        player_score = 0
        computer_score = 0
        gesture = "Unknown"
        computer_choice = ""
        result = ""

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
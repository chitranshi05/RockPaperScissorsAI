import cv2
import mediapipe as mp
import random
import time

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

choices = ["Rock", "Paper", "Scissors"]

player_score = 0
computer_score = 0

round_active = False
countdown_start = 0
countdown_duration = 3
result = ""
computer_choice = ""
gesture = "Unknown"

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
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    current_time = time.time()

    if round_active:
        elapsed = current_time - countdown_start
        remaining = countdown_duration - int(elapsed)

        if remaining > 0:
            cv2.putText(img, str(remaining), (300,250),
                        cv2.FONT_HERSHEY_SIMPLEX, 4,
                        (0,0,255), 6)
        else:
            # Countdown finished — now generate computer move ONCE
            computer_choice = random.choice(choices)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
                    gesture = get_gesture(handLms)

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

    # Display information
    cv2.putText(img, f"Your Move: {gesture}", (30,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,255,0), 2)

    # Show computer choice ONLY after round ends
    if not round_active and computer_choice != "":
        cv2.putText(img, f"Computer: {computer_choice}", (30,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255,0,0), 2)

    cv2.putText(img, f"Result: {result}", (30,150),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,0,255), 2)

    cv2.putText(img, f"Score: You {player_score} - {computer_score} Computer",
                (30,200), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255,255,0), 2)

    cv2.putText(img, "Press SPACE to Play | R to Reset | ESC to Exit",
                (30,450), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (200,200,200), 2)

    if player_score == 5:
        cv2.putText(img, "YOU WON THE GAME!", (150,300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (0,255,0), 4)
    elif computer_score == 5:
        cv2.putText(img, "COMPUTER WON THE GAME!", (80,300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (0,0,255), 4)

    cv2.imshow("Rock Paper Scissors AI", img)

    key = cv2.waitKey(1)

    if key == 32 and not round_active:
        if player_score < 5 and computer_score < 5:
            round_active = True
            countdown_start = time.time()
            gesture = "Unknown"
            result = ""
            computer_choice = ""  # Hide previous choice

    if key == ord('r'):
        player_score = 0
        computer_score = 0
        result = ""
        gesture = "Unknown"
        computer_choice = ""

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
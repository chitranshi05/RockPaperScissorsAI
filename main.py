import cv2
import mediapipe as mp
import numpy as np
import random
import time

# -----------------------------
# Initialize webcam
# -----------------------------
cap = cv2.VideoCapture(0)

# -----------------------------
# Initialize MediaPipe Hands
# -----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

# -----------------------------
# Game variables
# -----------------------------
moves = ["Rock", "Paper", "Scissors"]

player_score = 0
computer_score = 0

round_started = False
start_time = 0
countdown_time = 3

player_move = "Unknown"
computer_move = ""
game_result = ""


# -----------------------------
# Function to detect gesture
# -----------------------------
def detect_gesture(hand):
    
    fingers = []

    # Check if fingers are up
    fingers.append(1 if hand.landmark[8].y < hand.landmark[6].y else 0)   # index
    fingers.append(1 if hand.landmark[12].y < hand.landmark[10].y else 0) # middle
    fingers.append(1 if hand.landmark[16].y < hand.landmark[14].y else 0) # ring
    fingers.append(1 if hand.landmark[20].y < hand.landmark[18].y else 0) # pinky

    # Decide gesture
    if fingers == [0,0,0,0]:
        return "Rock"

    elif fingers == [1,1,1,1]:
        return "Paper"

    elif fingers == [1,1,0,0]:
        return "Scissors"

    else:
        return "Unknown"


# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, frame = cap.read()

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (800,600))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Create side UI panel
    panel = 255 * np.ones((600,400,3), dtype=np.uint8)

    screen = np.hstack((frame, panel))

    current_time = time.time()

    # -----------------------------
    # Countdown Logic
    # -----------------------------
    if round_started:

        elapsed = current_time - start_time
        remaining = countdown_time - int(elapsed)

        if remaining > 0:

            cv2.circle(screen, (400,300), 100, (0,0,255), -1)

            cv2.putText(screen, str(remaining), (370,330),
                        cv2.FONT_HERSHEY_SIMPLEX, 3,
                        (255,255,255), 6)

        else:

            # Detect player hand
            if results.multi_hand_landmarks:

                for hand in results.multi_hand_landmarks:

                    draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                    player_move = detect_gesture(hand)

            # Computer random move
            computer_move = random.choice(moves)

            # Decide winner
            if player_move == computer_move:

                game_result = "Draw"

            elif (player_move == "Rock" and computer_move == "Scissors") or \
                 (player_move == "Paper" and computer_move == "Rock") or \
                 (player_move == "Scissors" and computer_move == "Paper"):

                game_result = "You Win"
                player_score += 1

            else:

                game_result = "Computer Wins"
                computer_score += 1

            round_started = False


    # -----------------------------
    # Draw UI boxes
    # -----------------------------
    cv2.rectangle(screen,(820,50),(1180,150),(200,200,200),2)
    cv2.rectangle(screen,(820,180),(1180,280),(200,200,200),2)
    cv2.rectangle(screen,(820,310),(1180,410),(200,200,200),2)
    cv2.rectangle(screen,(820,440),(1180,540),(200,200,200),2)


    # Player move
    cv2.putText(screen,"YOUR MOVE",(880,80),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)

    cv2.putText(screen,player_move,(900,120),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,150,0),3)


    # Computer move
    cv2.putText(screen,"COMPUTER",(880,210),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)

    if not round_started:
        cv2.putText(screen,computer_move,(900,250),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(150,0,0),3)


    # Result
    cv2.putText(screen,"RESULT",(920,340),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)

    cv2.putText(screen,game_result,(860,380),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,200),3)


    # Score
    cv2.putText(screen,"SCORE",(920,470),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)

    cv2.putText(screen,f"{player_score} - {computer_score}",
                (920,510),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3)


    # Game instructions
    cv2.putText(screen,"SPACE = Play | R = Reset | ESC = Exit",
                (200,570),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,(100,100,100),2)


    cv2.imshow("Rock Paper Scissors AI",screen)


    key = cv2.waitKey(1)

    # Start round
    if key == 32 and not round_started:

        round_started = True
        start_time = time.time()

        player_move = "Unknown"
        computer_move = ""
        game_result = ""


    # Reset game
    if key == ord('r'):

        player_score = 0
        computer_score = 0
        player_move = "Unknown"
        computer_move = ""
        game_result = ""


    # Exit game
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()
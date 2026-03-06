import cv2
import mediapipe as mp
import numpy as np
import random
import time

CAMERA_WIDTH = 800
CAMERA_HEIGHT = 600
PANEL_WIDTH = 400
PANEL_X_START = CAMERA_WIDTH + 20
COUNTDOWN_SECONDS = 3
WIN_SCORE = 5

CHOICES = ["Rock", "Paper", "Scissors"]


def get_gesture(hand_landmarks):
    fingers = []

    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    if hand_landmarks.landmark[17].x < hand_landmarks.landmark[5].x:
        fingers.append(1 if thumb_tip.x > thumb_ip.x else 0)
    else:
        fingers.append(1 if thumb_tip.x < thumb_ip.x else 0)

    fingers.append(1 if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y else 0)
    fingers.append(1 if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y else 0)
    fingers.append(1 if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y else 0)
    fingers.append(1 if hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y else 0)

    total = sum(fingers)

    if total <= 1:
        return "Rock"
    elif total >= 4:
        return "Paper"
    elif fingers[1] == 1 and fingers[2] == 1 and total == 2:
        return "Scissors"
    else:
        return "Unknown"


class RockPaperScissorsGame:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.player_score = 0
        self.computer_score = 0
        self.round_active = False
        self.round_decided = False
        self.countdown_start = 0
        self.gesture = "Unknown"
        self.computer_choice = ""
        self.result = ""

    def reset(self):
        self.player_score = 0
        self.computer_score = 0
        self.gesture = "Unknown"
        self.computer_choice = ""
        self.result = ""
        self.round_active = False
        self.round_decided = False

    def start_round(self):
        if self.player_score < WIN_SCORE and self.computer_score < WIN_SCORE:
            self.round_active = True
            self.round_decided = False
            self.countdown_start = time.time()
            self.gesture = "Unknown"
            self.result = ""
            self.computer_choice = ""

    def evaluate_round(self):
        self.computer_choice = random.choice(CHOICES)

        if self.gesture == "Unknown":
            self.result = "Invalid Move"
            return

        if self.gesture == self.computer_choice:
            self.result = "Draw"
        elif (self.gesture == "Rock" and self.computer_choice == "Scissors") or \
             (self.gesture == "Scissors" and self.computer_choice == "Paper") or \
             (self.gesture == "Paper" and self.computer_choice == "Rock"):
            self.result = "You Win!"
            self.player_score += 1
        else:
            self.result = "Computer Wins!"
            self.computer_score += 1

    def draw_ui(self, img):
        cv2.rectangle(img, (PANEL_X_START, 50), (PANEL_X_START + 360, 150), (200, 200, 200), 2)
        cv2.rectangle(img, (PANEL_X_START, 180), (PANEL_X_START + 360, 280), (200, 200, 200), 2)
        cv2.rectangle(img, (PANEL_X_START, 310), (PANEL_X_START + 360, 410), (200, 200, 200), 2)
        cv2.rectangle(img, (PANEL_X_START, 440), (PANEL_X_START + 360, 540), (200, 200, 200), 2)

        cv2.putText(img, "YOUR MOVE", (PANEL_X_START + 60, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(img, self.gesture, (PANEL_X_START + 80, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 0), 3)

        cv2.putText(img, "COMPUTER", (PANEL_X_START + 60, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        if self.round_decided:
            cv2.putText(img, self.computer_choice, (PANEL_X_START + 80, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 0, 0), 3)

        cv2.putText(img, "RESULT", (PANEL_X_START + 100, 340),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(img, self.result, (PANEL_X_START + 40, 380),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 3)

        cv2.putText(img, "SCORE", (PANEL_X_START + 100, 470),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(img, f"{self.player_score}  -  {self.computer_score}",
                    (PANEL_X_START + 100, 510),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

        if self.player_score == WIN_SCORE:
            cv2.putText(img, "YOU WON THE GAME!", (150, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
        elif self.computer_score == WIN_SCORE:
            cv2.putText(img, "COMPUTER WON THE GAME!", (80, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

        cv2.putText(img, "SPACE = Play  |  R = Reset  |  ESC = Exit",
                    (200, 570), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (100, 100, 100), 2)

    def run(self):
        if not self.cap.isOpened():
            print("Error: Could not open camera")
            return

        try:
            while True:
                success, frame = self.cap.read()
                if not success:
                    break

                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))

                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(img_rgb)

                ui_panel = 255 * np.ones((CAMERA_HEIGHT, PANEL_WIDTH, 3), dtype=np.uint8)
                img = np.hstack((frame, ui_panel))

                current_time = time.time()

                if self.round_active and not self.round_decided:
                    elapsed = current_time - self.countdown_start
                    remaining = COUNTDOWN_SECONDS - int(elapsed)

                    if remaining > 0:
                        cv2.circle(img, (CAMERA_WIDTH // 2, CAMERA_HEIGHT // 2),
                                   100, (0, 0, 255), -1)
                        cv2.putText(img, str(remaining),
                                    (CAMERA_WIDTH // 2 - 30, CAMERA_HEIGHT // 2 + 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 3,
                                    (255, 255, 255), 6)
                    else:
                        if results.multi_hand_landmarks:
                            for hand_lms in results.multi_hand_landmarks:
                                self.mp_draw.draw_landmarks(
                                    img[:, :CAMERA_WIDTH], hand_lms,
                                    self.mp_hands.HAND_CONNECTIONS
                                )
                                self.gesture = get_gesture(hand_lms)

                        self.evaluate_round()
                        self.round_decided = True

                self.draw_ui(img)
                cv2.imshow("Rock Paper Scissors AI", img)

                key = cv2.waitKey(1)

                if key == 32 and not self.round_active:
                    self.start_round()
                elif key == ord('r'):
                    self.reset()
                elif key == 27:
                    break
        finally:
            self.cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()
import cv2
import mediapipe as mp
import numpy as np
import random
import time
import math

CAMERA_WIDTH = 800
CAMERA_HEIGHT = 600
PANEL_WIDTH = 400
COUNTDOWN_SECONDS = 3
WIN_SCORE = 5

CHOICES = ["Rock", "Paper", "Scissors"]

COLOR_BG = (30, 30, 30)
COLOR_CARD = (50, 50, 50)
COLOR_CARD_BORDER = (80, 80, 80)
COLOR_TITLE = (180, 180, 180)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (100, 220, 100)
COLOR_RED = (80, 80, 255)
COLOR_YELLOW = (60, 220, 220)
COLOR_BLUE = (220, 150, 50)
COLOR_ACCENT = (255, 120, 50)
COLOR_MUTED = (120, 120, 120)
COLOR_PLAYER = (100, 220, 150)
COLOR_COMPUTER = (120, 150, 255)

GESTURE_SYMBOLS = {
    "Rock": "O",
    "Paper": "=",
    "Scissors": "X",
    "Unknown": "?",
    "": "-"
}


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


def draw_rounded_rect(img, pt1, pt2, color, thickness, radius=15):
    x1, y1 = pt1
    x2, y2 = pt2

    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

    cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
    cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)


def draw_filled_rounded_rect(img, pt1, pt2, fill_color, border_color, radius=15):
    overlay = img.copy()
    x1, y1 = pt1
    x2, y2 = pt2

    cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), fill_color, -1)
    cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), fill_color, -1)
    cv2.circle(overlay, (x1 + radius, y1 + radius), radius, fill_color, -1)
    cv2.circle(overlay, (x2 - radius, y1 + radius), radius, fill_color, -1)
    cv2.circle(overlay, (x1 + radius, y2 - radius), radius, fill_color, -1)
    cv2.circle(overlay, (x2 - radius, y2 - radius), radius, fill_color, -1)

    cv2.addWeighted(overlay, 0.85, img, 0.15, 0, img)
    draw_rounded_rect(img, pt1, pt2, border_color, 2, radius)


def draw_gesture_icon(img, gesture, center_x, center_y, size=30, color=COLOR_WHITE):
    if gesture == "Rock":
        cv2.circle(img, (center_x, center_y), size, color, 3)
    elif gesture == "Paper":
        half = size
        cv2.rectangle(img, (center_x - half, center_y - half),
                      (center_x + half, center_y + half), color, 3)
    elif gesture == "Scissors":
        offset = size
        cv2.line(img, (center_x - offset, center_y - offset),
                 (center_x + offset, center_y + offset), color, 3)
        cv2.line(img, (center_x + offset, center_y - offset),
                 (center_x - offset, center_y + offset), color, 3)


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
        self.hand_draw_spec = self.mp_draw.DrawingSpec(color=(0, 255, 200), thickness=2, circle_radius=2)
        self.conn_draw_spec = self.mp_draw.DrawingSpec(color=(0, 200, 150), thickness=2)

        self.player_score = 0
        self.computer_score = 0
        self.round_active = False
        self.round_decided = False
        self.countdown_start = 0
        self.gesture = "Unknown"
        self.computer_choice = ""
        self.result = ""
        self.round_number = 0

    def reset(self):
        self.player_score = 0
        self.computer_score = 0
        self.gesture = "Unknown"
        self.computer_choice = ""
        self.result = ""
        self.round_active = False
        self.round_decided = False
        self.round_number = 0

    def start_round(self):
        if self.player_score < WIN_SCORE and self.computer_score < WIN_SCORE:
            self.round_active = True
            self.round_decided = False
            self.countdown_start = time.time()
            self.gesture = "Unknown"
            self.result = ""
            self.computer_choice = ""
            self.round_number += 1

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

    def draw_countdown(self, img, remaining, elapsed):
        cx, cy = CAMERA_WIDTH // 2, CAMERA_HEIGHT // 2
        fraction = (elapsed % 1.0)
        pulse = int(80 + 30 * math.sin(fraction * math.pi * 2))

        cv2.circle(img, (cx, cy), pulse + 20, (0, 0, 80), -1)
        cv2.circle(img, (cx, cy), pulse, (0, 0, 200), -1)

        end_angle = int(360 * (1 - fraction))
        cv2.ellipse(img, (cx, cy), (pulse + 5, pulse + 5),
                    -90, 0, end_angle, COLOR_ACCENT, 4)

        cv2.putText(img, str(remaining), (cx - 25, cy + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, COLOR_WHITE, 5)

    def draw_ui(self, img):
        px = CAMERA_WIDTH
        panel = img[:, px:]
        panel[:] = COLOR_BG

        cv2.putText(img, "ROCK PAPER SCISSORS", (px + 40, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_ACCENT, 2)

        if self.round_number > 0:
            cv2.putText(img, f"Round {self.round_number}", (px + 310, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_MUTED, 1)

        draw_filled_rounded_rect(img, (px + 15, 50), (px + 385, 140), COLOR_CARD, COLOR_CARD_BORDER)
        cv2.putText(img, "YOU", (px + 30, 78),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TITLE, 1)
        cv2.putText(img, self.gesture, (px + 30, 118),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_PLAYER, 2)
        if self.gesture and self.gesture != "Unknown":
            draw_gesture_icon(img, self.gesture, px + 340, 95, 25, COLOR_PLAYER)

        draw_filled_rounded_rect(img, (px + 15, 155), (px + 385, 245), COLOR_CARD, COLOR_CARD_BORDER)
        cv2.putText(img, "COMPUTER", (px + 30, 183),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TITLE, 1)
        if self.round_decided:
            cv2.putText(img, self.computer_choice, (px + 30, 223),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_COMPUTER, 2)
            if self.computer_choice:
                draw_gesture_icon(img, self.computer_choice, px + 340, 200, 25, COLOR_COMPUTER)
        elif self.round_active:
            cv2.putText(img, "...", (px + 30, 223),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_MUTED, 2)

        draw_filled_rounded_rect(img, (px + 15, 260), (px + 385, 345), COLOR_CARD, COLOR_CARD_BORDER)
        cv2.putText(img, "RESULT", (px + 30, 288),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TITLE, 1)

        result_color = COLOR_MUTED
        if "Win!" in self.result:
            result_color = COLOR_GREEN
        elif "Computer" in self.result:
            result_color = COLOR_RED
        elif self.result == "Draw":
            result_color = COLOR_YELLOW
        elif self.result == "Invalid Move":
            result_color = COLOR_RED

        cv2.putText(img, self.result, (px + 30, 328),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, result_color, 2)

        draw_filled_rounded_rect(img, (px + 15, 360), (px + 385, 470), COLOR_CARD, COLOR_CARD_BORDER)
        cv2.putText(img, "SCORE", (px + 30, 390),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TITLE, 1)

        bar_y = 420
        bar_h = 30
        bar_width = 340
        total_played = self.player_score + self.computer_score
        if total_played > 0:
            player_w = int(bar_width * self.player_score / max(total_played, 1))
            cv2.rectangle(img, (px + 25, bar_y), (px + 25 + player_w, bar_y + bar_h), COLOR_GREEN, -1)
            cv2.rectangle(img, (px + 25 + player_w, bar_y), (px + 25 + bar_width, bar_y + bar_h), COLOR_RED, -1)
        else:
            cv2.rectangle(img, (px + 25, bar_y), (px + 25 + bar_width, bar_y + bar_h), COLOR_CARD_BORDER, -1)

        cv2.putText(img, str(self.player_score), (px + 25, bar_y + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 2)
        cv2.putText(img, str(self.computer_score),
                    (px + 25 + bar_width - 20, bar_y + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 2)
        cv2.putText(img, "vs", (px + 25 + bar_width // 2 - 10, bar_y + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1)

        if self.player_score == WIN_SCORE or self.computer_score == WIN_SCORE:
            overlay = img.copy()
            cv2.rectangle(overlay, (0, 200), (CAMERA_WIDTH, 400), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

            if self.player_score == WIN_SCORE:
                text = "YOU WON THE GAME!"
                color = COLOR_GREEN
            else:
                text = "COMPUTER WON!"
                color = COLOR_RED

            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 4)[0]
            text_x = (CAMERA_WIDTH - text_size[0]) // 2
            cv2.putText(img, text, (text_x, 315),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 4)

            cv2.putText(img, "Press R to play again", (CAMERA_WIDTH // 2 - 130, 360),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_MUTED, 2)

        game_over = self.player_score == WIN_SCORE or self.computer_score == WIN_SCORE
        if not self.round_active and not game_over:
            hint = "Press SPACE to play"
        elif game_over:
            hint = "R = New Game  |  ESC = Quit"
        else:
            hint = "Show your hand!"

        cv2.putText(img, hint, (px + 30, 500),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_MUTED, 1)

        cv2.putText(img, "SPACE = Play  |  R = Reset  |  ESC = Exit",
                    (px + 20, 560), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (80, 80, 80), 1)

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

                ui_panel = np.zeros((CAMERA_HEIGHT, PANEL_WIDTH, 3), dtype=np.uint8)
                img = np.hstack((frame, ui_panel))

                if results.multi_hand_landmarks:
                    for hand_lms in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            img[:, :CAMERA_WIDTH], hand_lms,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.hand_draw_spec,
                            self.conn_draw_spec
                        )

                current_time = time.time()

                if self.round_active and not self.round_decided:
                    elapsed = current_time - self.countdown_start
                    remaining = COUNTDOWN_SECONDS - int(elapsed)

                    if remaining > 0:
                        self.draw_countdown(img, remaining, elapsed)
                    else:
                        if results.multi_hand_landmarks:
                            for hand_lms in results.multi_hand_landmarks:
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
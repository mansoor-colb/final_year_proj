import cv2
import numpy as np
import pyautogui
import mediapipe as mp

selected_color = None
tracking_mode = "hand"  # Default tracking mode

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


def mouse_callback(event, x, y, flags, param):
    global selected_color
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_color = frame[y, x]
        print("Selected Color:", selected_color)


def detect_color(frame, target_color):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_bound = np.array(target_color - np.array([10, 50, 50]))
    upper_bound = np.array(target_color + np.array([10, 50, 50]))

    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    return result


def get_mouse_position(frame, target_color, screen_width, screen_height):
    print((target_color))
    contours, _ = cv2.findContours(
        detect_color(frame, target_color)[:, :, 0],
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    print(contours)
    if contours:
        print("uu")
        max_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(max_contour)

        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])

            scaled_x = int(cx * screen_width / frame.shape[1])
            scaled_y = int(cy * screen_height / frame.shape[0])
            print(scaled_y,scaled_y)
            return scaled_x, scaled_y

    return None


def detect_hand(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Assuming only one hand is detected
        index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]

        height, width, _ = frame.shape

        index_finger_x = int(index_finger.x * width)
        index_finger_y = int(index_finger.y * height)

        ring_finger_x = int(ring_finger.x * width)
        ring_finger_y = int(ring_finger.y * height)

        distance = np.sqrt((index_finger_x - ring_finger_x) ** 2 + (index_finger_y - ring_finger_y) ** 2)
        print("di",distance)
        if distance < 500:  # Adjust this threshold as needed
            return "click"

        return index_finger_x, index_finger_y

    return None


def main():
    global frame, tracking_mode, selected_color

    cap = cv2.VideoCapture(0h)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    screen_width = 1920  # Set your desired screen width
    screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * (screen_width / cap.get(cv2.CAP_PROP_FRAME_WIDTH)))

    cv2.namedWindow("Color Selection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Color Selection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("Color Selection", mouse_callback)

    print("Color Selection Phase. Click on a color to track.")
    while selected_color is None:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screen_width, screen_height))
        cv2.imshow("Color Selection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # cv2.namedWindow("Object Detection", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("Object Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    print("Press 'h' for hand detection, 'l' for laser tracking, and 'q' to quit.")
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screen_width, screen_height))

        if tracking_mode == "hand":
            hand_result = detect_hand(frame)
            if hand_result == "click":
                pyautogui.click()
            elif isinstance(hand_result, tuple):
                cv2.circle(frame, hand_result, 10, (0, 255, 0), -1)
                pyautogui.moveTo(hand_result[0], hand_result[1])

        elif tracking_mode == "laser":
            mouse_position = get_mouse_position(frame, selected_color, screen_width, screen_height)
            if mouse_position:
                pyautogui.moveTo(mouse_position[0], mouse_position[1])

        cv2.imshow("Object Detection", frame)

        key = cv2.waitKey(10)  # Adjust waitKey value for desired frame rate
        if key == ord('h'):
            tracking_mode = "hand"
            print("Switched to hand detection mode.")
        elif key == ord('l'):
            tracking_mode = "laser"
            print("Switched to laser tracking mode.")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

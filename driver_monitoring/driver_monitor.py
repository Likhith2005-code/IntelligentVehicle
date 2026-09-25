import cv2
import mediapipe as mp
import math
import time

EYE_CLOSED_THRESHOLD = 0.21
EYE_CLOSED_TIME = 1.5

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    raise SystemExit

def distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )

def eye_aspect_ratio(landmarks, eye_points, width, height):
    points = []
    for index in eye_points:
        x = int(landmarks[index].x * width)
        y = int(landmarks[index].y * height)
        points.append((x, y))

    vertical_1 = distance(points[1], points[5])
    vertical_2 = distance(points[2], points[4])
    horizontal = distance(points[0], points[3])

    if horizontal == 0:
        return 0

    return (vertical_1 + vertical_2) / (2.0 * horizontal)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

eyes_closed_start = None
drowsiness = False
distraction = False

while True:
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read webcam.")
        break

    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    driver_status = "NO FACE"

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        left_ear = eye_aspect_ratio(
            face_landmarks.landmark, LEFT_EYE, width, height
        )
        right_ear = eye_aspect_ratio(
            face_landmarks.landmark, RIGHT_EYE, width, height
        )
        average_ear = (left_ear + right_ear) / 2.0

        if average_ear < EYE_CLOSED_THRESHOLD:
            if eyes_closed_start is None:
                eyes_closed_start = time.time()

            closed_duration = time.time() - eyes_closed_start

            if closed_duration >= EYE_CLOSED_TIME:
                drowsiness = True
        else:
            eyes_closed_start = None
            drowsiness = False

        nose = face_landmarks.landmark[1]
        nose_x = nose.x

        if nose_x < 0.40 or nose_x > 0.60:
            distraction = True
        else:
            distraction = False

        if drowsiness:
            driver_status = "DROWSINESS DETECTED"
        elif distraction:
            driver_status = "DRIVER DISTRACTED"
        else:
            driver_status = "ATTENTIVE"

        for point in face_landmarks.landmark:
            x = int(point.x * width)
            y = int(point.y * height)
            cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

    cv2.rectangle(frame, (10, 10), (500, 145), (0, 0, 0), -1)

    cv2.putText(
        frame, "DRIVER MONITORING SYSTEM", (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
    )
    cv2.putText(
        frame, f"Status: {driver_status}", (25, 75),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
    )
    cv2.putText(
        frame, f"Drowsiness: {'HIGH' if drowsiness else 'LOW'}", (25, 105),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
    )
    cv2.putText(
        frame, f"Distraction: {'HIGH' if distraction else 'LOW'}", (25, 130),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
    )

    cv2.imshow("Intelligent Heavy Vehicle - Driver Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
face_mesh.close()

print("Driver monitoring stopped.")

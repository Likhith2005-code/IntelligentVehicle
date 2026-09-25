import cv2
from ultralytics import YOLO
import time

# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

MODEL_NAME = "yolo11n.pt"
CONFIDENCE = 0.40

# Objects relevant to our heavy-vehicle road monitoring
TARGET_CLASSES = {
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "bus",
    "truck"
}

# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------

print("Loading YOLO model...")

model = YOLO(MODEL_NAME)

print("YOLO model loaded.")


# ---------------------------------------------------------
# CAMERA
# ---------------------------------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    raise SystemExit


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read webcam.")
        break

    # Run object detection
    results = model(
        frame,
        conf=CONFIDENCE,
        verbose=False
    )

    detected_objects = []

    # Draw detections
    annotated_frame = frame.copy()

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            if class_name not in TARGET_CLASSES:
                continue

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            detected_objects.append(class_name)

            label = f"{class_name} {confidence:.2f}"

            cv2.rectangle(
                annotated_frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                2
            )

            cv2.putText(
                annotated_frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

    # -----------------------------------------------------
    # COUNT OBJECTS
    # -----------------------------------------------------

    object_counts = {}

    for obj in detected_objects:
        object_counts[obj] = object_counts.get(obj, 0) + 1

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    cv2.rectangle(
        annotated_frame,
        (10, 10),
        (430, 155),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        annotated_frame,
        "ROAD MONITORING SYSTEM",
        (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    y = 70

    if object_counts:

        for name, count in object_counts.items():

            text = f"{name}: {count}"

            cv2.putText(
                annotated_frame,
                text,
                (25, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            y += 25

    else:

        cv2.putText(
            annotated_frame,
            "No target objects detected",
            (25, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

    cv2.imshow(
        "Intelligent Heavy Vehicle - Road Monitoring",
        annotated_frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ---------------------------------------------------------
# CLEANUP
# ---------------------------------------------------------

cap.release()
cv2.destroyAllWindows()

print("Road monitoring stopped.")

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
stop_sign_cascade = cv2.CascadeClassifier("stop_sign.xml")

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    stop_sign = stop_sign_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in stop_sign:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]

    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
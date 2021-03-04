import cv2
cap = cv2.VideoCapture(0)

while True:
    # Capturing the live frame
    ret, img = cap.read()

    cv2.imshow("video",img)
    cv2.waitKey(1)
cap.release()
cv.destroyAllWindows()
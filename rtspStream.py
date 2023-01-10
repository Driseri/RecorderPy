import cv2
import time

time1 = time.perf_counter()

vcap = cv2.VideoCapture(0)
# vcap = cv2.VideoCapture("Мужчина.avi")
frame_width = int(vcap.get(3))
frame_height = int(vcap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_size = (frame_width,frame_height)
fps = vcap.get(cv2.CAP_PROP_FPS)
print(fps)
out = cv2.VideoWriter('output1.avi', fourcc, fps, frame_size)

while(1):
    time2 = time.perf_counter()
    ret, frame = vcap.read()
    out.write(frame)
    if time2-time1>20:
        break

vcap.release()

# After we release our webcam, we also release the output
out.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()
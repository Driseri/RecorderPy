import cv2
import time

# time1 = time.perf_counter()
# #'rtsp://172.18.191.72:554/Streaming/Channels/1'
# try:
#     cap = cv2.VideoCapture('rtsp://172.18.191.84:554/live/0/MAIN')
# except:
#     print('\n\n\n\nНе подключился к камере\n\n\n\n')
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# frame_size = (frame_width,frame_height)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fps = 35
# out = cv2.VideoWriter('output.', cv2.VideoWriter_fourcc('M','J','P','G'),fps, frame_size)
#
# while(cap.isOpened()):
#     time2 = time.perf_counter()
#     ret, frame = cap.read()
#     if ret == True and (time2-time1) < 2:
#         # write the flipped frame
#         out.write(frame)
#
#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break
#
# # Release everything if job is finished
# cap.release()
# out.release()
# cv2.destroyAllWindows()


vcap = cv2.VideoCapture("rtsp://172.18.191.85:554/Streaming/Channels/1")

while(1):

    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)
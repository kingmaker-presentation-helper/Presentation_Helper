from time import time
import cv2
import mediapipe as mp
from module import detectPose

mp_pose = mp.solutions.pose

# 이미지 포즈 추출

# pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

# mp_drawing = mp.solutions.drawing_utils

# sample = cv2.imread('./example/pose1.jpg')

# results = pose.process(cv2.cvtColor(sample, cv2.COLOR_BGR2RGB))

# img_hei, img_wid, _ = sample.shape

# img_copy = sample.copy()

# if results.pose_landmarks:
#     mp_drawing.draw_landmarks(image=img_copy, landmark_list=results.pose_landmarks,
#                               connections=mp_pose.POSE_CONNECTIONS)
#     fig = plt.figure(figsize=[10,10])
#     plt.title("output")
#     plt.axis('off')
#     plt.imshow(img_copy[:,:,::-1])
#     plt.show()

pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.3, model_complexity=1)

video = cv2.VideoCapture('./example/steve2.mp4')
time1=0
while video.isOpened():
    ok, frame = video.read()

    if not ok:
        break

    # frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    frame = cv2.resize(frame, (int(frame_width * (640/frame_height)), 640))
    frame, _ = detectPose(frame, pose_video, display=False)

    time2=time()

    if (time2 - time1) > 0:
        frames_per_second = 1.0/(time2 - time1)

        cv2.putText(frame, 'FPS: {}'.format(int(frames_per_second)), (10,30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
        time1 = time2
        cv2.imshow('Pose Detection', frame)
        k = cv2.waitKey(1) & 0xFF

        if (k==27):# When ESC is pressed
            break

video.release()
cv2.destroyAllWindows()
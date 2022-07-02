import cv2
vidcap = cv2.VideoCapture('basket2.mp4')
count = 0
success = True
while success:
  success,image = vidcap.read()
  name = "frames/frame" + str(count)+ ".png"
  print(name)
  cv2.imwrite(name, image)     # save frame as JPEG file
  if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
  count += 1
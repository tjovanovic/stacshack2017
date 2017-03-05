from goprohero import GoProHero
import cv2
camera = GoProHero(password='goprohero')
while True:
    frame = camera.image()
    cv2.imwrite("live.jpg", frame)

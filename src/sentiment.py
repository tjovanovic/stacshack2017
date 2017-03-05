#import httplib, urllib, base64
#from goprohero import GoProHero
#import cv2
import json
import time
#camera = GoProHero(password='goprohero')
#camera.command('record', 'on')
def sentiment():
    # cap = cv2.VideoCapture(0)
    # if cap.isOpened():
    #     for i in range(30):
    #         cap.read()
    #     ret, frame = cap.read()
    #     cv2.imwrite("sentiment.jpg",frame)

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'b74d4c6803b74cfba668b4916e4b346b',
    }

    # params = urllib.urlencode({
    #     # Request parameters
    #     'url': 'https://3c4df835.ngrok.io/image'
    # })
    # conn = httplib.responses('westus.api.cognitive.microsoft.com')
    # conn.request("POST", "/emotion/v1.0/recognize?%s" % params, "{body}", headers)
    # response = conn.getresponse()
    # data = response.read()
    # print(data)
    # conn.close()
    return True


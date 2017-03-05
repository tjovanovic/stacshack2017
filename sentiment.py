import httplib, urllib, base64
#from goprohero import GoProHero
import cv2
import time
#camera = GoProHero(password='goprohero')
#camera.command('record', 'on')
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    time.sleep(2)
    cv2.imwrite("sentiment.jpg",frame)

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '3a3f60e57930448cbfd2bb62bedeb399',
}

params = urllib.urlencode({
    # Request parameters
    'visualFeatures': 'Categories',
    'details': 'http://9c6363f7.ngrok.io/get_image',
    'language': 'en',
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
import cv2
import requests
import numpy as np
from threading import Thread

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """
    def __init__(self, url):
        self.url = url
        print("accessing "+url)
        self.getFrame()
        print("completed one frame")
        self.stopped = False

    def getFrame(self):
        self.r = requests.get(self.url, stream=True)
        if (self.r.status_code == 200):
            self.bytes = bytes()
            for chunk in self.r.iter_content(chunk_size=1024):
                self.bytes += chunk
                a = self.bytes.find(b'\xff\xd8')
                b = self.bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = self.bytes[a:b + 2]
                    self.bytes = self.bytes[b + 2:]
                    i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    # print(i)
                    # (self.grabbed, self.frame) = (i
                    self.grabbed = 1
                    self.frame = i
                    # cv2.imshow('i', i)
                    # if cv2.waitKey(1) == 27:
                    #   exit(0)
                    break
    def start(self):
        Thread(target=self.get, args=   ()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                self.getFrame()
                (self.grabbed, self.frame)

    def stop(self):
        self.stopped = True
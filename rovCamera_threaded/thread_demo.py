import argparse
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def noThreading(source=0):
    """Grab and show video frames without multithreading."""

    cap = cv2.VideoCapture(source)
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()

def threadVideoGet(source=0, source2=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Main thread shows video frames.
    """
    sourceCount = 1
    video_getter = VideoGet(source).start()
    if source2!=0:
        print("Source 2: "+source2)
        video_getter2 = VideoGet(source2).start()
        sourceCount = 2

    #cps = CountsPerSec().start()
    #print("video_getter.frame "+str(video_getter.frame))
    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            if sourceCount == 2:
                video_getter2.stop()
            break

        frame = video_getter.frame
        #frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        if sourceCount == 2:
            frame = video_getter2.frame
            cv2.imshow("Video2", frame)


        #cps.increment()

def threadVideoShow(source=0):
    """
    Dedicated thread for showing video frames with VideoShow object.
    Main thread grabs video frames.
    """

    cap = cv2.VideoCapture(source)
    (grabbed, frame) = cap.read()
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or video_shower.stopped:
            video_shower.stop()
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=0,
        help="Path to video file or integer representing webcam index"
            + " (default 0).")
    ap.add_argument("--source2", "-s2", default=0,
        help="Path to video file or integer representing webcam index"
            + " (default 0).")
    ap.add_argument("--thread", "-t", default="none",
        help="Threading mode: get (video read in its own thread),"
            + " show (video show in its own thread), both"
            + " (video read and video show in their own threads),"
            + " none (default--no multithreading)")
    args = vars(ap.parse_args())
    if args["thread"] == "both":
        threadBoth(args["source"], args["source2"])
    elif args["thread"] == "get":
        print("args: " + str(args))
        print("running videoGet")
        threadVideoGet(args["source"], args["source2"])
    elif args["thread"] == "show":
        threadVideoShow(args["source"])
    else:
        noThreading(args["source"])

if __name__ == "__main__":
    main()
    #http://root:Hkis1234@10.39.15.5/axis-cgi/mjpg/video.cgi

#to run the program, type this in the terminal
#/usr/local/bin/python3.7 thread_demo.py -s 'http://10.39.12.153:8081/?action=stream.jpg' -t=get -s2 'http://10.39.12.153:8082/?action=stream.jpg'
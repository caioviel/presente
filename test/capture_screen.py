import video.avconv as avconv
import time


def getLinuxCap():
        cap = avconv.AVConverter(["-y",
                              "-rtbufsize",  "1500M",
                              "-f",
                              "x11grab",
                              "-s",
                              "1920x1080",
                              "-draw_mouse",
                              "1",
                              "-i",
                              ":0.0",
                              "-f",
                              "pulse",
                              "-i",
                              "default",
                              "-ac",
                              "2",
                              "-c:a",
                              "libvo_aacenc",
                              "-c:v",
                              "libx264",
                              "-qscale",
                              "0.1",
                              "/home/caioviel/Desktop/capturedfile.mp4"], True)
        return cap

def getWindowsCap():
        cap = avconv.AVConverter(["-y",
                              "-f",
                              "gdigrab",
                              "-framerate",

                              "25",
                              "-i",
                              "desktop",
                              "C://Users//Caio/Desktop//teste.mp4"], True)
        return cap

def main():
    cap = getWindowsCap()
    
    
    cap.start()
    time.sleep(10)
    cap.stop(True)


if __name__ == "__main__":
    main()

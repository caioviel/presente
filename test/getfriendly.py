__author__ = 'Caio'


def main():
    cap = avconv.AVConverter(["-y",
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


    cap.start()
    time.sleep(15)
    cap.stop(True)


if __name__ == "__main__":
    main()
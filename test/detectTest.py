import transitiondetection
import uuid
import datetime
import json
import os
import video.avconv as avconv


basepath = "/home/caioviel/Desktop/"
project = "MariaAdelina"
videofile = os.path.join(basepath, project, "videos/screen.mp4")
tempvideofile = os.path.join(basepath, project, "videos/temp.mp4")
imagespath = os.path.join(basepath, project, "images")
videoParams = ["-i", videofile,
               "-qscale", "0",
               "-y",
                tempvideofile]
jsonfile = os.path.join(basepath, project, "presente_json.js")

conv = avconv.AVConverter(videoParams, True)
conv.start()
conv.wait_finish()

detector = transitiondetection.TransitionDetector()
duration, pois = detector.detect_transitions(tempvideofile, imagespath)
json_object = \
            {
                "id": str(uuid.uuid4()),
                "autorName": "Maria Adelina Silva Brito",
                "autorEmail": "masbrit@icmc.usp.br",
                "date": datetime.datetime.now().isoformat(),
                "duration": duration,
                "pointsOfInterest": []
            }

json_pois = json_object["pointsOfInterest"]
for begin, end, filename in pois:
    jpoi = {"type": "SLIDE_TRANSITION", "begin": begin, "end": end, "slideImage": filename}
    json_pois.append(jpoi)


json_str = json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))
myFile = open(jsonfile, 'w+')
myFile.write("var captureSession = " + json_str + ";")

os.remove(tempvideofile)
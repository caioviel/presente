# -*- coding: utf-8 -*-


from subprocess import Popen, PIPE, STDOUT

sub = Popen("c:\\ffmpeg\\bin\\ffmpeg  -list_devices true -f dshow -i dummy", stdout=PIPE, stdin=PIPE, stderr=STDOUT,shell=True)

i = 0
while sub.poll() is None:
    line = sub.stdout.readline()
    line_lower = line.lower()
    has = False
    for name in ["webcam", "camera", "cam", u"câmera", u"câmara"]:
        if name in line_lower:
            has = True
            break

    if has:
        device_name = line[line.find('\"')+1 : line.rfind('\"')]
        print device_name

    line = sub.stdout.readline()
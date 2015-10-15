#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from ui_FormCapture import Ui_FormCapture
import os
import datetime
from datetime import datetime


import platform
if platform.system() == "Windows":
    IS_WINDOWS = True
    IS_LINUX = False
else:
    IS_WINDOWS = True
    IS_LINUX = False


class FormCapture(QtGui.QWidget):
    def __init__(self,  monitor_size=None, real_path=None, 
                 project_dir=None, username=None, parent=None):
        
        super(FormCapture, self).__init__(parent)
        self.directory = None
        self.monitor_size = monitor_size
        self.real_path = real_path
        self.project_dir = project_dir
        self.username = username
        
        self.ui = Ui_FormCapture()
        self.ui.setupUi(self)
        self.init_ui()
        self.bind_events()
        self.create_project()

        
        self.marks = []
        
    def create_project(self):
        found_files = os.listdir(self.project_dir)
        
        candidate_index = 1
        candidate_id = 'myProject1'
        while found_files.count(candidate_id) > 0:
            candidate_index += 1
            candidate_id = 'myProject' + str(candidate_index)
            
        self.directory = os.path.join(self.project_dir, candidate_id)
        #os.makedirs(self.directory)
        
        files_path = os.path.join(self.real_path, 'html5player')
        
        import shutil
        shutil.copytree(files_path, self.directory)

        os.makedirs( os.path.join(self.directory, "videos"))


        import model
        self.project = model.AnnotationProject(candidate_id, candidate_id, None, None, 
                                               datetime.now(), self.username, 
                                               self.directory, None)
        
        self.save_json_project()
        
        
        
    def save_json_project(self):
        self.project.last_modification = datetime.now()
        project_path = os.path.join(unicode(self.directory), 'project.json')
        json_object = self.project.to_json()
        myfile = open(project_path, "w")
        
        import json
        myfile.write(json.dumps(json_object, indent=4, sort_keys=True))
    
        
        
    def init_ui(self):
        self.setMaximumSize(self.size())
        self.setMinimumSize(self.size())
        
        self.ui.ckb_webcam.setChecked(True)
        self.video_devices = self.get_video_devices()
        self.audio_devices = self.get_audio_devices()
        self.ui.cmb_webcam_video.addItems(self.video_devices.keys())
        self.ui.cmb_webcam_audio.addItems(self.audio_devices.keys())

        self.ui.ckb_screen.setChecked(True)
        self.ui.rdb_fullscreen.setChecked(True)
        self.ui.txt_height.setText(str(self.monitor_size.height()))
        self.ui.txt_width.setText(str(self.monitor_size.width()))
        self.ui.txt_x.setText("0")
        self.ui.txt_y.setText("0")
        self.ui.cmb_screen_audio.addItem(u"Nenhum")
        self.ui.cmb_screen_audio.addItem(u"Pulse")
        self.ui.cmb_screen_audio.addItems(self.audio_devices.keys())
        self.ui.txt_height.setEnabled(False)
        self.ui.txt_width.setEnabled(False)
        self.ui.txt_x.setEnabled(False)
        self.ui.txt_y.setEnabled(False)
        
        self.ui.btn_drop.setEnabled(False)
        self.ui.btn_example.setEnabled(False)
        self.ui.btn_important.setEnabled(False)
        self.ui.btn_other.setEnabled(False)
        self.ui.btn_save.setEnabled(False)
        self.ui.btn_stop.setEnabled(False)
        
    def ckb_webcam_changed(self, state):
        if self.ui.ckb_webcam.isChecked():
            self.ui.btn_start.setEnabled(True)
            self.ui.cmb_webcam_audio.setEnabled(True)
            self.ui.cmb_webcam_video.setEnabled(True)
        else:
            self.ui.cmb_webcam_audio.setEnabled(False)
            self.ui.cmb_webcam_video.setEnabled(False)
            
            if not self.ui.ckb_screen.isChecked():
                self.ui.btn_start.setEnabled(False)
        
        
    def ckb_screen_changed(self, state):
        if self.ui.ckb_screen.isChecked():
            self.ui.btn_start.setEnabled(True)
            self.ui.rdb_fullscreen.setEnabled(True)
            self.ui.rdb_partial.setEnabled(True)
            self.ui.cmb_screen_audio.setEnabled(True)
            
            if self.ui.rdb_partial.isChecked():
                self.ui.txt_height.setEnabled(True)
                self.ui.txt_width.setEnabled(True)
                self.ui.txt_x.setEnabled(True)
                self.ui.txt_y.setEnabled(True)
                
        else:
            self.ui.rdb_fullscreen.setEnabled(False)
            self.ui.rdb_partial.setEnabled(False)
            self.ui.cmb_screen_audio.setEnabled(False)
            
            if not self.ui.rdb_partial.isChecked():
                self.ui.txt_height.setEnabled(False)
                self.ui.txt_width.setEnabled(False)
                self.ui.txt_x.setEnabled(False)
                self.ui.txt_y.setEnabled(False)
                
                
            if not self.ui.ckb_webcam.isChecked():
                self.ui.btn_start.setEnabled(False)
                
    def rdb_fullscreen_changed(self, state):
        if self.ui.rdb_fullscreen.isChecked():
            self.ui.txt_height.setText(str(self.monitor_size.height()))
            self.ui.txt_width.setText(str(self.monitor_size.width()))
            self.ui.txt_x.setText("0")
            self.ui.txt_y.setText("0")
            self.ui.txt_height.setEnabled(False)
            self.ui.txt_width.setEnabled(False)
            self.ui.txt_x.setEnabled(False)
            self.ui.txt_y.setEnabled(False)
    
    def rdb_partial_changed(self, state):
        if self.ui.rdb_partial.isChecked():
            self.ui.txt_height.setEnabled(True)
            self.ui.txt_width.setEnabled(True)
            self.ui.txt_x.setEnabled(True)
            self.ui.txt_y.setEnabled(True)
            
            
    def start_recording(self):
        self.start_recording_time = datetime.now()
        self.marks = []
        
        if self.ui.ckb_webcam.isChecked():
            self.start_recording_webcam()
            
        if self.ui.ckb_screen.isChecked():
            self.start_recording_screen()
            
        self.ui.frame.setEnabled(False)
        self.ui.frame_2.setEnabled(False)
        
        self.ui.btn_start.setEnabled(False)
        self.ui.btn_important.setEnabled(True)
        self.ui.btn_other.setEnabled(True)
        self.ui.btn_example.setEnabled(True)
        self.ui.btn_stop.setEnabled(True)
            
            
    def start_recording_webcam(self):
        import video.avconv as avconv
        import cv2

        device_path = self.video_devices[self.ui.cmb_webcam_video.currentText()]

        if IS_LINUX:
            device_number = int(device_path[10:])
        else:
            device_number = self.ui.cmb_webcam_video.currentIndex()
        print device_number

        cap = cv2.VideoCapture(device_number)
        width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        cap.release()

        arg = ["-y"]
        if IS_LINUX:
            #Video
            arg.append('-s')
            arg.append(str(width) + "x" + str(height))
            arg.append('-f')
            arg.append('video4linux2')
            arg.append('-i')
            arg.append(device_path)

            #Audio
            arg.append('-f')
            arg.append('alsa')
            arg.append('-i')
            arg.append(self.audio_devices[self.ui.cmb_webcam_audio.currentText()])


            #Codec
            arg.append('-c:a')
            arg.append('libvo_aacenc')
            arg.append('-c:v')
            arg.append('libx264')
            arg.append('-qscale')
            arg.append('0.1')
        else:
            #Video
            #arg.append('-s')
            #arg.append(str(width) + "x" + str(height))
            arg.append('-f')
            arg.append('dshow')
            arg.append('-i')
            #arg.append("video=\"" + device_path + "\":audio=\"" + self.audio_devices[self.ui.cmb_webcam_audio.currentText()] + "\"")
            arg.append("video=" + device_path + ":audio=" + self.audio_devices[self.ui.cmb_webcam_audio.currentText()])

            #Codec
            arg.append('-c:a')
            arg.append('libvo_aacenc')
            arg.append('-c:v')
            arg.append('libx264')
            arg.append('-qscale')
            arg.append('0.1')
        
        self.cam_file = os.path.join(self.directory, "videos", "webcam.mp4")
        arg.append(self.cam_file)
        
        self.camrec = avconv.AVConverter(arg, True)
        self.camrec.start()
    
    def start_recording_screen(self):
        import video.avconv as avconv
        
        arg = ["-y"]

        if IS_LINUX:
            #Video
            arg.append('-f')
            arg.append('x11grab')
            arg.append('-s')
            arg.append(str(self.ui.txt_width.text()) + "x" + str(self.ui.txt_height.text()))
            arg.append("-draw_mouse")
            arg.append("1")
            if self.ui.rdb_partial.isChecked():
                arg.append("-show_region")
                arg.append("1")
            arg.append('-i')
            arg.append(":0.0+" + str(self.ui.txt_x.text()) + "," + str(self.ui.txt_y.text())  )

            #Audio
            audio = self.ui.cmb_screen_audio.currentText()
            if audio != "Nenhum":
                if audio == "Pulse":
                    arg.append("-f")
                    arg.append("pulse")
                    arg.append("-i")
                    arg.append("default")
                else:
                    arg.append('-f')
                    arg.append('alsa')
                    arg.append('-i')
                    arg.append(self.audio_devices[self.ui.cmb_webcam_audio.currentText()])
        else:
            #Video
            arg.append('-f')
            arg.append('gdigrab')
            arg.append('-framerate')
            arg.append("25")
            arg.append('-video_size')
            arg.append(str(self.ui.txt_width.text()) + "x" + str(self.ui.txt_height.text()))
            arg.append("-draw_mouse")
            arg.append("1")
            if self.ui.rdb_partial.isChecked():
                arg.append("-show_region")
                arg.append("1")
                arg.append("-offset_x")
                arg.append(str(self.ui.txt_x.text()))
                arg.append("-offset_y")
                arg.append(str(self.ui.txt_y.text()))
            arg.append('-i')
            arg.append('desktop')
        
        
        #Codec
        arg.append('-c:a')
        arg.append('libvo_aacenc')
        arg.append('-c:v')
        arg.append('libx264')
        arg.append('-qscale')
        arg.append('0.1')
        arg.append('-f')
        arg.append('mp4')
        
        
        self.screen_file = os.path.join(self.directory, "videos", "screen.mp4")
        arg.append(self.screen_file)
        
        self.screenrec = avconv.AVConverter(arg, True)
        self.screenrec.start()

    def stop_recording(self):
        import time
        time.sleep(5)

        if self.ui.ckb_webcam.isChecked():
            self.camrec.stop()
            
        if self.ui.ckb_screen.isChecked():
            self.screenrec.stop()
            
        self.end_recording_time = datetime.now()
        
        self.ui.btn_stop.setEnabled(False)
        self.ui.btn_important.setEnabled(False)
        self.ui.btn_other.setEnabled(False)
        self.ui.btn_example.setEnabled(False)
        
        self.ui.btn_save.setEnabled(True)
        self.ui.btn_drop.setEnabled(True)


        msgBox = QtGui.QMessageBox()
        msgBox.setText(u"Gravação encerrada.")
        msgBox.setInformativeText(u"Deseja visualizar o resoltado?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
        ret = msgBox.exec_()

        if ret == QtGui.QMessageBox.Yes:
            self.open_broser()

    def open_broser(self):
        import webbrowser
        webbrowser.open(os.path.join(self.directory, "index.html"), new=1, autoraise=True)
        
        
    def mark_important(self):
        self.marks.append( ("IMPORTANT", datetime.now()))
    
    def mark_example(self):
        self.marks.append( ("EXAMPLE", datetime.now()))
    
    def mark_other(self):
        self.marks.append( ("OTHER", datetime.now()))
        
        
    def drop_recording(self):
        self.ui.frame.setEnabled(True)
        self.ui.frame_2.setEnabled(True)
        self.ui.btn_start.setEnabled(True)
        self.ui.btn_drop.setEnabled(False)
        self.ui.btn_example.setEnabled(False)
        self.ui.btn_important.setEnabled(False)
        self.ui.btn_other.setEnabled(False)
        self.ui.btn_save.setEnabled(False)
        self.ui.btn_stop.setEnabled(False)
        
    def save_recording(self):
        self.setEnabled(False)
        
        import model
        self.project.main_media = self.screen_file
        self.project.secondary_media = self.cam_file
        
        index = 1
        for mark in self.marks:
            timestamp = mark[1] - self.start_recording_time
            ann = model.Annotation("mark_" + str(index), mark[0])
            ann.annotation_time = QtCore.QTime(0,0,0).addSecs(timestamp.total_seconds())
            self.project.add_annotation(ann)
            
        if self.ui.ckb_screen.isChecked():
            from transitiondetection import TransitionDetector
            detector = TransitionDetector()
            pois = detector.detect_transitions(self.screen_file)
            
            index = 1
            for begin_time, _ in pois:
                ann = model.Annotation("slide_" + str(index), "SLIDE_TRANSITION")
                ann.annotation_time = QtCore.QTime(0,0,0).addSecs(begin_time)
                self.project.add_annotation(ann)
                
            
        self.save_json_project()
        
        self.setEnabled(True)
        QtGui.QMessageBox.information(self, "Project-mm-2015", "Processamento Finalizado!")
            
            
        
        
 
    def bind_events(self):
        self.ui.btn_start.clicked.connect(self.start_recording)
        self.ui.btn_stop.clicked.connect(self.stop_recording)
        self.ui.btn_drop.clicked.connect(self.drop_recording)
        self.ui.btn_save.clicked.connect(self.save_recording)
        
        self.ui.btn_important.clicked.connect(self.mark_important)
        self.ui.btn_other.clicked.connect(self.mark_example)
        self.ui.btn_example.clicked.connect(self.mark_other)
        
        self.ui.ckb_screen.stateChanged.connect(self.ckb_screen_changed)
        self.ui.ckb_webcam.stateChanged.connect(self.ckb_webcam_changed)
        self.ui.rdb_fullscreen.toggled.connect(self.rdb_fullscreen_changed)
        self.ui.rdb_partial.toggled.connect(self.rdb_partial_changed)
        
        
    def get_video_devices(self):
        video_devices = {}
        if IS_LINUX:
            f = os.popen("v4l2-ctl --list-devices")
            line = f.readline()
            while line != "":
                if "(" in line:
                    device_name = line[: line.find("(")-1]
                    print device_name
                    line = f.readline()
                    while line != "" and "(" not in line:
                        if "/" in line:
                            device_path = line[line.find("/"): len(line)-1]
                            print device_path
                            video_devices[device_name] = device_path
                        line = f.readline()
                    continue

                line = f.readline()
        else:
            from subprocess import Popen, PIPE, STDOUT
            sub = Popen("c:\\ffmpeg\\bin\\ffmpeg  -list_devices true -f dshow -i dummy", stdout=PIPE, stdin=PIPE, stderr=STDOUT,shell=True)
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
                    video_devices[device_name] = device_name
            
        return video_devices
    
    def get_audio_devices(self):
        audio_devices = {}

        if IS_LINUX:
            f = os.popen("arecord -l")

            line = f.readline()
            while line != "":
                if "card" in line:
                    card_number = line[line.find("card ") + 5 : line.find(":")]
                    device_number = line[line.find("device ") + 7: line.rfind(":")]
                    device_name = line[line.find("[") +1: line.find("]")]
                    audio_devices[device_name] = "hw:" + card_number + "," + device_number

                line = f.readline()
        else:
            from subprocess import Popen, PIPE, STDOUT
            sub = Popen("c:\\ffmpeg\\bin\\ffmpeg  -list_devices true -f dshow -i dummy", stdout=PIPE, stdin=PIPE, stderr=STDOUT,shell=True)
            while sub.poll() is None:
                line = sub.stdout.readline()
                line_lower = line.lower()
                has = False
                for name in ["microfone", "microphone", "mic"]:
                    if name in line_lower:
                        has = True
                        break

                if has:
                    device_name = line[line.find('\"')+1 : line.rfind('\"')]
                    print device_name
                    audio_devices[device_name] = device_name

        return audio_devices
        
        
                

        
def main():
    import sys
    app = QtGui.QApplication(sys.argv)   
    monitor_size = app.desktop().screenGeometry() 
    fc = FormCapture(monitor_size=monitor_size)
    fc.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
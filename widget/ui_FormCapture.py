# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/FormCapture.ui'
#
# Created: Mon Apr 27 10:28:13 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FormCapture(object):
    def setupUi(self, FormCapture):
        FormCapture.setObjectName("FormCapture")
        FormCapture.resize(690, 189)
        self.btn_start = QtGui.QPushButton(FormCapture)
        self.btn_start.setGeometry(QtCore.QRect(10, 140, 101, 41))
        self.btn_start.setObjectName("btn_start")
        self.frame = QtGui.QFrame(FormCapture)
        self.frame.setGeometry(QtCore.QRect(10, 10, 181, 121))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.ckb_webcam = QtGui.QCheckBox(self.frame)
        self.ckb_webcam.setGeometry(QtCore.QRect(10, 10, 101, 22))
        self.ckb_webcam.setObjectName("ckb_webcam")
        self.cmb_webcam_video = QtGui.QComboBox(self.frame)
        self.cmb_webcam_video.setGeometry(QtCore.QRect(57, 40, 111, 27))
        self.cmb_webcam_video.setObjectName("cmb_webcam_video")
        self.cmb_webcam_audio = QtGui.QComboBox(self.frame)
        self.cmb_webcam_audio.setGeometry(QtCore.QRect(57, 80, 111, 27))
        self.cmb_webcam_audio.setObjectName("cmb_webcam_audio")
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 40, 66, 31))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 66, 31))
        self.label_2.setObjectName("label_2")
        self.frame_2 = QtGui.QFrame(FormCapture)
        self.frame_2.setGeometry(QtCore.QRect(200, 10, 311, 121))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.ckb_screen = QtGui.QCheckBox(self.frame_2)
        self.ckb_screen.setGeometry(QtCore.QRect(10, 10, 97, 22))
        self.ckb_screen.setObjectName("ckb_screen")
        self.cmb_screen_audio = QtGui.QComboBox(self.frame_2)
        self.cmb_screen_audio.setGeometry(QtCore.QRect(60, 80, 111, 27))
        self.cmb_screen_audio.setObjectName("cmb_screen_audio")
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 66, 31))
        self.label_3.setObjectName("label_3")
        self.rdb_fullscreen = QtGui.QRadioButton(self.frame_2)
        self.rdb_fullscreen.setGeometry(QtCore.QRect(10, 40, 116, 22))
        self.rdb_fullscreen.setObjectName("rdb_fullscreen")
        self.rdb_partial = QtGui.QRadioButton(self.frame_2)
        self.rdb_partial.setGeometry(QtCore.QRect(90, 40, 116, 22))
        self.rdb_partial.setObjectName("rdb_partial")
        self.txt_height = QtGui.QLineEdit(self.frame_2)
        self.txt_height.setGeometry(QtCore.QRect(250, 30, 51, 27))
        self.txt_height.setObjectName("txt_height")
        self.txt_x = QtGui.QLineEdit(self.frame_2)
        self.txt_x.setGeometry(QtCore.QRect(180, 80, 51, 27))
        self.txt_x.setObjectName("txt_x")
        self.txt_width = QtGui.QLineEdit(self.frame_2)
        self.txt_width.setGeometry(QtCore.QRect(180, 30, 51, 27))
        self.txt_width.setObjectName("txt_width")
        self.txt_y = QtGui.QLineEdit(self.frame_2)
        self.txt_y.setGeometry(QtCore.QRect(250, 80, 51, 27))
        self.txt_y.setObjectName("txt_y")
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(180, 10, 66, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(250, 10, 51, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(200, 60, 21, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtGui.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(270, 60, 41, 17))
        self.label_7.setObjectName("label_7")
        self.frame_3 = QtGui.QFrame(FormCapture)
        self.frame_3.setGeometry(QtCore.QRect(520, 10, 161, 121))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.btn_example = QtGui.QPushButton(self.frame_3)
        self.btn_example.setGeometry(QtCore.QRect(10, 46, 141, 31))
        self.btn_example.setObjectName("btn_example")
        self.btn_other = QtGui.QPushButton(self.frame_3)
        self.btn_other.setGeometry(QtCore.QRect(10, 10, 141, 31))
        self.btn_other.setObjectName("btn_other")
        self.btn_stop = QtGui.QPushButton(FormCapture)
        self.btn_stop.setGeometry(QtCore.QRect(120, 140, 101, 41))
        self.btn_stop.setObjectName("btn_stop")
        self.btn_drop = QtGui.QPushButton(FormCapture)
        self.btn_drop.setGeometry(QtCore.QRect(470, 140, 101, 41))
        self.btn_drop.setObjectName("btn_drop")
        self.btn_save = QtGui.QPushButton(FormCapture)
        self.btn_save.setGeometry(QtCore.QRect(580, 140, 101, 41))
        self.btn_save.setObjectName("btn_save")
        self.btn_important = QtGui.QPushButton(FormCapture)
        self.btn_important.setGeometry(QtCore.QRect(530, 90, 141, 31))
        self.btn_important.setObjectName("btn_important")

        self.retranslateUi(FormCapture)
        QtCore.QMetaObject.connectSlotsByName(FormCapture)

    def retranslateUi(self, FormCapture):
        FormCapture.setWindowTitle(QtGui.QApplication.translate("FormCapture", "Iniciar Gravação", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_start.setText(QtGui.QApplication.translate("FormCapture", "Iniciar\n"
"Gravação", None, QtGui.QApplication.UnicodeUTF8))
        self.ckb_webcam.setText(QtGui.QApplication.translate("FormCapture", "WebCam", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormCapture", "Vídeo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FormCapture", "Áudio", None, QtGui.QApplication.UnicodeUTF8))
        self.ckb_screen.setText(QtGui.QApplication.translate("FormCapture", "Tela", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FormCapture", "Áudio", None, QtGui.QApplication.UnicodeUTF8))
        self.rdb_fullscreen.setText(QtGui.QApplication.translate("FormCapture", "Inteira", None, QtGui.QApplication.UnicodeUTF8))
        self.rdb_partial.setText(QtGui.QApplication.translate("FormCapture", "Parcial", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FormCapture", "Largura", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("FormCapture", "Altura", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("FormCapture", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("FormCapture", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_example.setText(QtGui.QApplication.translate("FormCapture", "Marcar Exemplo", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_other.setText(QtGui.QApplication.translate("FormCapture", "Marcar", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_stop.setText(QtGui.QApplication.translate("FormCapture", "Encerar\n"
"Gravação", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_drop.setText(QtGui.QApplication.translate("FormCapture", "Descartar\n"
"Gravação", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_save.setText(QtGui.QApplication.translate("FormCapture", "Processar\n"
"e Encerar", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_important.setText(QtGui.QApplication.translate("FormCapture", "Marcar Importannte", None, QtGui.QApplication.UnicodeUTF8))


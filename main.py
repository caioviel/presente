#!/usr/bin/env python
# -*- coding: utf-8 -*-

PROJECTS_DIRECTORY = "MyPresenteCapture"

from PySide import QtGui
from widget.FormCapture import FormCapture
import os
import sys
import getpass
import logging


import platform
if platform.system() == "Windows":
    IS_WINDOWS = True
    IS_LINUX = False
else:
    IS_WINDOWS = True
    IS_LINUX = False

logger = logging.getLogger('presente')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s - %(name)s: %(message)s'))
logger.addHandler(handler)

real_path, _ = os.path.split(os.path.realpath(__file__))
home_directory = os.getenv('USERPROFILE') or os.getenv('HOME')
username = getpass.getuser()


def create_project_directory():
    directory_to_create = os.path.join(home_directory, PROJECTS_DIRECTORY)
    
    if not os.path.exists(directory_to_create):
        os.mkdir(directory_to_create)
    elif not os.path.isdir(directory_to_create):
        print 'There is a file named ' + PROJECTS_DIRECTORY + ' into your home folder. Impossible to continue.'
        sys.exit(1)
        
    return directory_to_create
                    
if __name__ == "__main__":
    
    project_dir = create_project_directory()
      
    app = QtGui.QApplication(sys.argv)
    widget = FormCapture(app.desktop().screenGeometry(),
                         real_path, 
                         project_dir,
                         username)
    widget.show()
    
    ret = app.exec_()
    
    del widget
    del app
    sys.exit(ret)
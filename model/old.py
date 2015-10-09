#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide import QtCore

def invert_type_maps(original):
    inverted = {}
    for key, value in original.items():
        inverted[value] = key
            
    return inverted

class AnnotationProject(object):
    @staticmethod
    def parse_json(self, project):
        pass
    
    def to_json(self):
        annotations = []
        json_object = {'AnnotationProject' : {
                                              "id" : self.id,
                                              "name" : self.name,
                                              "main_media" : self.main_media,
                                              "description" : self.description,
                                              "annotations" : annotations}}
        for ann in self.annotations:
            self.annotations.append(ann.to_json())
            
        return json_object
                       
        
    
    
    def __init__(self, mid, name, main_media=None, description=None, last_modification=None, username=None):
        self.id = mid
        self.name = name
        self.main_media = main_media
        self.description = description
        self.last_modification = last_modification
        self.username = username
        
        self.annotations = []
    
    def remove_annotation(self, annotation):
        if not isinstance(annotation, Annotation):
            raise TypeError('The argument annotation must be an instance of Annotation.')
        
        #Its a new annotation
        try:
            self.annotations.remove(annotation)
        except:
            return False
        return True    
        
        
    def add_annotation(self, annotation):
        #if not isinstance(annotation, Annotation):
        #    raise TypeError('The argument annotation must be an instance of Annotation.')
        
        #Its a new annotation
        if annotation not in self.annotations:
            self.annotations.append(annotation)
        else:
            raise Exception('This annotation is already inserted.')            

class VideoStream(object):
    def __init__(self, media_source):
        self.media_source = media_source
        self.__openned = False
        self.__fps = None
        self.__width = None
        self.__height = None
        self.__duration = None
        
    def open(self):
        pass
    
    @property
    def fps(self):
        return self.__fps
    
    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
    
    @property
    def duration(self):
        return self.__duration
    
class Annotation(object):
    AUDIO = 0
    VIDEO = 1
    IMAGE = 2
    PLAIN_TEXT = 3
    HTML = 4
    
    type_to_str = {VIDEO : 'VIDEO',
                   PLAIN_TEXT : 'PLAIN_TEXT',
                   HTML : 'HTML',
                   AUDIO : 'AUDIO',
                   IMAGE : 'IMAGE'}
    
    str_to_type = invert_type_maps(type_to_str)
    
    def __init__(self, mid, content_type=AUDIO, timestamp=QtCore.QTime(), 
                 name="Generic Annotation", mtype="Annotation"):
        
        self.__id = mid
        self.__content_type = Annotation.AUDIO
        self.__timestamp = QtCore.QTime()
        self.__name = name
        self.__type = mtype
        
    @property
    def timestamp(self):
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, value):
        if not isinstance(value, QtCore.QTime):
            raise ValueError('The argument is a invalid timestamp')
        
        self.__timestamp = value
        
    @property
    def content_type(self):
        return self.__content_type
    
    @content_type.setter
    def content_type(self, value):
        if not Annotation.type_to_str.has_key(value):
            raise ValueError('The argument is a invalid Annotation type')
        
        self.__content_type = value
        
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    def get_files(self):
        raise NotImplemented("Please implement this method")
    
    def code_json(self):
        raise NotImplemented("Please implement this method")
    
    @property
    def type(self):
        return self.__type
    


        

def test():
    from plugins import PluginsManager
    from model.serialization import ProjectSerializator
    
    plugins_manager = PluginsManager()
    plugins_manager.load_file('../plugins.xml')
    project = AnnotationProject('area51', 'Meu nome', 'video.mp4', 
                                 'Teste do Serializator 5', None, 'Kamila')
    
    annotation_class = plugins_manager.get_annotation_class('InformationAnnotation')
    annotation = annotation_class('anotation1')
    project.add_annotation(annotation)
    
    serializator = ProjectSerializator(plugins_manager)
    serializator.dump_file(project, 'project.json')

    
    
    
       
    
    

if __name__ == "__main__":
    test()
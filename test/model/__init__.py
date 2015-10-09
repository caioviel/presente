#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os
from PyQt4 import QtGui, QtCore
#from PySide import QtCore


def adjust_path(old_path, directory):
    if "\\" in old_path:
        import ntpath
        _, filename = ntpath.split(old_path)
    else:
        _, filename = os.path.split(old_path)
        
    print filename
    
    return os.path.join(directory, "medias", filename)


class AnnotationProject(object):
    def __init__(self, mid, name, main_media=None, description=None, last_modification=None, username=None, directory=None):
        self.id = mid
        self.name = name
        self.main_media = main_media
        self.description = description
        self.last_modification = last_modification
        self.username = username
        self.directory = directory
        self.annotations = []
        
    @staticmethod
    def parse_json(json_object, directory=None):
        project =  AnnotationProject(json_object['AnnotationProject']['id'],
                                         json_object['AnnotationProject']['name'],
                                         json_object['AnnotationProject']['main_media'],
                                         json_object['AnnotationProject']['description'])
        
        
        if directory is not None and project.main_media is not None:
            project.main_media = adjust_path(project.main_media, directory)
        
        for json_ann in json_object['AnnotationProject']['annotations']:
            project.add_annotation(Annotation.parse_json(json_ann, directory))
            
        return project
    
    def to_json(self):
        json_annotations = []
        json_object = {'AnnotationProject' : {
                                              "id" : self.id,
                                              "name" : self.name,
                                              "main_media" : self.main_media,
                                              "description" : self.description,
                                              "annotations" : json_annotations}}
        for ann in self.annotations:
            print ann
            json_annotations.append(ann.to_json())
            
        return json_object
        
    def generate_annotation_id(self):
        if len(self.annotations) > 0:
            return self.annotations[len(self.annotations)-1].id + 1
        else:
            return 1
    
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
        if not isinstance(annotation, Annotation):
            raise TypeError('The argument annotation must be an instance of Annotation.')
        
        #Its a new annotation
        if annotation not in self.annotations:
            self.annotations.append(annotation)
        else:
            raise Exception('This annotation is already inserted.') 
        
class Annotation(object):
    def __init__(self, myid, description=None, timestamp=None):
        self.id = myid
        self.timestamp = timestamp
        self.description = description
        self.annotation_time = None
        self.interaction = None
        
    @staticmethod
    def parse_json(json_object, directory=None):
        ann =  Annotation(json_object['Annotation']['id'],
                              json_object['Annotation']['description'])
        
        
        ann.annotation_time = QtCore.QTime.fromString(json_object['Annotation']['annotation_time'])
        if json_object['Annotation'].has_key('interaction'):
            ann.interaction = Interaction.parse_json(json_object['Annotation']['interaction'], directory)
        
        return ann
    
    def to_json(self):
        json_object = {'Annotation' : {
                                              "id" : self.id,
                                              "annotation_time" : unicode(self.annotation_time.toString()),
                                              "description" : unicode(self.description)}}
        
        if self.interaction is not None:
            json_object['Annotation']['interaction'] = self.interaction.to_json()
            
        return json_object
    
    @property
    def type(self):
        if self.interaction is None:
            return "Annotation"
        else:
            return self.interaction.type
        
        
    @property
    def pt_type(self):
        if self.interaction is None:
            return u"Anotação"
        else:
            return self.interaction.pt_type
        
        
class Media(object):
    AUDIO = 1
    VIDEO = 2
    IMAGE = 3
    TEXT = 4
    SLIDES = 5 
    
    def __init__(self, myid, filename, showtime, mtype=IMAGE):
        self.id = myid
        self.filename = filename
        self.type = mtype
        self.url = None
        
        #time configurations
        self.showtime = showtime
        self.begintime = None
        self.duration = None
        
    @staticmethod
    def parse_json(json_object, directory=None):
        mtype = json_object['Media']['type']
        media = None
        if mtype == 'AUDIO':
            media = Audio.parse_json(json_object)
        elif mtype == 'VIDEO':
            media = Video.parse_json(json_object)
        elif mtype == 'IMAGE':
            media = Image.parse_json(json_object)
        elif mtype == 'TEXT':
            media = Text.parse_json(json_object)
        elif mtype == 'SLIDES':
            media = Slides.parse_json(json_object)
        
        if directory is not None and media.filename is not None:
            media.filename = adjust_path(media.filename, directory)
            
        if "\\" in media.id:
            import ntpath
            _, media.id = ntpath.split(media.id)
        else:
            _, media.id = os.path.split(media.id)
            
            
        return media
    
    def to_json(self):
        pass
        
CONTENT_TYPES = {Media.AUDIO : u'Áudio (*.wav *.mp3 *.ogg *.oga)',
                 Media.VIDEO : u'Vídeo (*.avi *.mp4 *.ogg *.webm *.mpeg)',
                 Media.IMAGE : u'Imagens (*.png *.jpg *.ico *.gif)',
                 Media.TEXT : u'Texto (*.txt *.html *.htm)',
                 Media.SLIDES : u''}

class Bondaries(object):
    def __init__(self, top=-1, left=-1, width=-1, height=-1):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.screen_width = -1
        self.screen_height =  -1
        
    @staticmethod
    def parse_json(json_object):
        bound = Bondaries()
        
        bound.top = json_object['Boundaries']['top']
        bound.left = json_object['Boundaries']['left']
        bound.width = json_object['Boundaries']['width']
        bound.height = json_object['Boundaries']['height']
        bound.screen_width = json_object['Boundaries']['screen_width']
        bound.screen_height = json_object['Boundaries']['screen_height']
        
        return bound
    
    def to_json(self):
        json_object = {'Boundaries' : {'top' : self.top,
                                      'left' : self.left,
                                      'width' : self.width,
                                      'height' : self.height,
                                      'screen_width' : self.screen_width,
                                      'screen_height' : self.screen_height}}
        return json_object
        
    def __str__(self):
        return str((self.left, self.top, self.width, self.height))
        
        
class Audio(Media):
    def __init__(self, myid, filename, showtime):
        super(Audio, self).__init__(myid, filename, 
                                    showtime, Media.AUDIO)
        
        self.main_video_volume = None
        self.media_volume = None
        
    @staticmethod
    def parse_json(json_object):
        myid = json_object['Media']['id']
        filename = json_object['Media']['filename']
        showtime = json_object['Media']['showtime']
        audio = Audio(myid, filename, showtime)
        
        if json_object['Media'].has_key('duration'):
            audio.duration = json_object['Media']['duration']
     
        if json_object['Media'].has_key('begintime'):
            audio.begintime = json_object['Media']['begintime']
            
        if json_object['Media'].has_key('media_volume'):
            audio.media_volume = json_object['Media']['media_volume']
            
        if json_object['Media'].has_key('main_video_volume'):
            audio.main_video_volume = json_object['Media']['main_video_volume']
            
        if json_object['Media'].has_key('url'):
            audio.url = json_object['Media']['url']
            
        return audio
    
    def to_json(self):
        json_object = {'Media' : {'type' : 'AUDIO',
                                  'id' : self.id,
                                  'filename' : self.filename,
                                  'showtime' : self.showtime}}
        
        if self.duration is not None:
            json_object['Media']['duration'] = self.duration
            
        if self.begintime is not None:
            json_object['Media']['begintime'] = self.begintime
            
        if self.media_volume is not None:
            json_object['Media']['media_volume'] = self.media_volume
            
        if self.main_video_volume is not None:
            json_object['Media']['main_video_volume'] = self.main_video_volume
            
        if self.url is not None:
            json_object['Media']['url'] = self.url
            
        return json_object
        
class Video(Media):
    def __init__(self, myid, filename, showtime):
        super(Video, self).__init__(myid, filename, 
                                    showtime, Media.VIDEO)
        
        self.bondaries = None
        self.resize_main_video = None
        self.main_video_volume = None
        self.media_volume = None
        
    @staticmethod
    def parse_json(json_object):
        myid = json_object['Media']['id']
        filename = json_object['Media']['filename']
        showtime = json_object['Media']['showtime']
        video = Video(myid, filename, showtime)
        
        if json_object['Media'].has_key('duration'):
            video.duration = json_object['Media']['duration']
     
        if json_object['Media'].has_key('begintime'):
            video.begintime = json_object['Media']['begintime']
            
        if json_object['Media'].has_key('media_volume'):
            video.media_volume = json_object['Media']['media_volume']
            
        if json_object['Media'].has_key('main_video_volume'):
            video.main_video_volume = json_object['Media']['main_video_volume']
            
        if json_object['Media'].has_key('bondaries'):
            video.bondaries = Bondaries.parse_json(json_object['Media']['bondaries'])
            
        if json_object['Media'].has_key('resize_main_video'):
            video.resize_main_video = Bondaries.parse_json(json_object['Media']['resize_main_video'])
            
        if json_object['Media'].has_key('url'):
            video.url = json_object['Media']['url']
            
        return video
    
    def to_json(self):
        json_object = {'Media' : {'type' : 'VIDEO',
                                  'id' : self.id,
                                  'filename' : self.filename,
                                  'showtime' : self.showtime}}
        
        if self.duration is not None:
            json_object['Media']['duration'] = self.duration
            
        if self.begintime is not None:
            json_object['Media']['begintime'] = self.begintime
            
        if self.media_volume is not None:
            json_object['Media']['media_volume'] = self.media_volume
            
        if self.main_video_volume is not None:
            json_object['Media']['main_video_volume'] = self.main_video_volume
            
        if self.bondaries is not None:
            json_object['Media']['bondaries'] = self.bondaries.to_json()
            
        if self.resize_main_video is not None:
            json_object['Media']['resize_main_video'] = self.resize_main_video.to_json()
            
        if self.url is not None:
            json_object['Media']['url'] = self.url
            
        return json_object
            
class Image(Media):
    def __init__(self, myid, filename, showtime, duration=5):
        super(Image, self).__init__(myid, filename, 
                                    showtime, Media.IMAGE)
        
        self.duration = duration
        self.bondaries = None
        self.resize_main_video = None
        
    @staticmethod
    def parse_json(json_object):
        myid = json_object['Media']['id']
        filename = json_object['Media']['filename']
        showtime = json_object['Media']['showtime']
        image = Image(myid, filename, showtime)
        
        if json_object['Media'].has_key('duration'):
            image.duration = json_object['Media']['duration']
     
        if json_object['Media'].has_key('begintime'):
            image.begintime = json_object['Media']['begintime']
            
        if json_object['Media'].has_key('bondaries'):
            image.bondaries = Bondaries.parse_json(json_object['Media']['bondaries'])
            
        if json_object['Media'].has_key('resize_main_video'):
            image.resize_main_video = Bondaries.parse_json(json_object['Media']['resize_main_video'])
            
        if json_object['Media'].has_key('url'):
            image.url = json_object['Media']['url']
            
        return image
    
    def to_json(self):
        json_object = {'Media' : {'type' : 'IMAGE',
                                  'id' : self.id,
                                  'filename' : self.filename,
                                  'showtime' : self.showtime}}
        
        if self.duration is not None:
            json_object['Media']['duration'] = self.duration
            
        if self.begintime is not None:
            json_object['Media']['begintime'] = self.begintime
            
            
        if self.bondaries is not None:
            json_object['Media']['bondaries'] = self.bondaries.to_json()
            
        if self.resize_main_video is not None:
            json_object['Media']['resize_main_video'] = self.resize_main_video.to_json()
            
        if self.url is not None:
            json_object['Media']['url'] = self.url
            
        return json_object


class Text(Media):
    ALIGN_LEFT = 0
    ALIGN_CENTER = 1
    ALIGN_RIGHT = 2

    def __init__(self, myid, filename, showtime, duration=5):
        super(Text, self).__init__(myid, filename, showtime, Media.TEXT)
        
        self.duration = duration
        self.bondaries = None
        self.resize_main_video = None
        self.text = None
        self.font = None
        self.fontSize = None
        self.bold = None
        self.italic = None
        self.underlined = None
        self.font_color = None
        self.bg_color = None
        self.bg_transparency = False
        self.alignment = None
        
    @staticmethod
    def parse_json(json_object):
        myid = json_object['Media']['id']
        filename = json_object['Media']['filename']
        showtime = json_object['Media']['showtime']
        text = Text(myid, filename, showtime)
        
        if json_object['Media'].has_key('duration'):
            text.duration = json_object['Media']['duration']
     
        if json_object['Media'].has_key('begintime'):
            text.begintime = json_object['Media']['begintime']
            
        if json_object['Media'].has_key('bondaries'):
            text.bondaries = Bondaries.parse_json(json_object['Media']['bondaries'])
            
        if json_object['Media'].has_key('resize_main_video'):
            text.resize_main_video = Bondaries.parse_json(json_object['Media']['resize_main_video'])
            
        #Text specifics
        if json_object['Media'].has_key('text'):
            text.text = json_object['Media']['text']
        
        if json_object['Media'].has_key('font'):
            text.font = json_object['Media']['font']
            
        if json_object['Media'].has_key('fontSize'):
            text.fontSize = json_object['Media']['fontSize']
            
        if json_object['Media'].has_key('bold'):
            text.bold = json_object['Media']['bold']
            
        if json_object['Media'].has_key('italic'):
            text.italic = json_object['Media']['italic']
            
        if json_object['Media'].has_key('underlined'):
            text.underlined = json_object['Media']['underlined']
            
        if json_object['Media'].has_key('bg_transparency'):
            text.bg_transparency = json_object['Media']['bg_transparency']
        
        if json_object['Media'].has_key('font_color'):
            text.font_color = QtGui.QColor(json_object['Media']['font_color'][0],
                                            json_object['Media']['font_color'][1],
                                            json_object['Media']['font_color'][2],
                                            json_object['Media']['font_color'][3])
            
        if json_object['Media'].has_key('bg_color'):
            text.bg_color = QtGui.QColor(json_object['Media']['bg_color'][0],
                                            json_object['Media']['bg_color'][1],
                                            json_object['Media']['bg_color'][2],
                                            json_object['Media']['bg_color'][3])
            
        if json_object['Media'].has_key('alignment'):
            align_str = json_object['Media']['alignment']
            if align_str == 'ALIGN_LEFT':
                text.alignment = Text.ALIGN_LEFT
            elif align_str == 'ALIGN_RIGHT':
                text.alignment = Text.ALIGN_RIGHT
            elif align_str == 'ALIGN_CENTER':
                text.alignment = Text.ALIGN_CENTER
                
        if json_object['Media'].has_key('url'):
            text.url = json_object['Media']['url']
            
            
        return text
    
    def to_json(self):
        json_object = {'Media' : {'type' : 'TEXT',
                                  'id' : self.id,
                                  'filename' : self.filename,
                                  'showtime' : self.showtime}}
        
        if self.duration is not None:
            json_object['Media']['duration'] = self.duration
            
        if self.begintime is not None:
            json_object['Media']['begintime'] = self.begintime
            
        if self.bondaries is not None:
            json_object['Media']['bondaries'] = self.bondaries.to_json()
            
        if self.resize_main_video is not None:
            json_object['Media']['resize_main_video'] = self.resize_main_video.to_json()
        
        if self.duration is not None:
            json_object['Media']['text'] = unicode(self.text)
            
        if self.font is not None:
            json_object['Media']['font'] = unicode(self.font)
            
        if self.fontSize is not None:
            json_object['Media']['fontSize'] = self.fontSize
            
        if self.bold is not None:
            json_object['Media']['bold'] = self.bold
            
        if self.italic is not None:
            json_object['Media']['italic'] = self.italic
            
        if self.underlined is not None:
            json_object['Media']['underlined'] = self.underlined
            
        if self.bg_transparency is not None:
            json_object['Media']['bg_transparency'] = self.bg_transparency
            
        if self.alignment is not None:
            if self.alignment == Text.ALIGN_CENTER:
                json_object['Media']['alignment'] = 'ALIGN_CENTER'
            elif self.alignment == Text.ALIGN_LEFT:
                json_object['Media']['alignment'] = 'ALIGN_LEFT'
            elif self.alignment == Text.ALIGN_RIGHT:
                json_object['Media']['alignment'] = 'ALIGN_RIGHT'
                
        if self.font_color is not None:
            json_object['Media']['font_color'] = [self.font_color.red(),
                                                  self.font_color.green(),
                                                  self.font_color.blue(),
                                                  self.font_color.alpha()]
            
        if self.bg_color is not None:
            json_object['Media']['bg_color'] = [self.bg_color.red(),
                                                self.bg_color.green(),
                                                self.bg_color.blue(),
                                                self.bg_color.alpha()]
            
        if self.url is not None:
            json_object['Media']['url'] = self.url
            
        return json_object
        
        
class Slides(Media):
    def __init__(self, myid, filename, showtime):
        super(Slides, self).__init__(myid, filename, 
                                     showtime, Media.SLIDES)
        
        self.slides = []
        self.transition_time = 2
        self.auto_transition = True
        self.resize_main_video = None
    
    def add_slide(self, image, position=None):
        if not isinstance(image, Image):
            raise TypeError('The argument image must be an instance of Image.')
        
        if position is None:
            self.slides.append(image)
        else:
            self.slides.insert(position, image)
        
class Icon(object):
    INFO = 1
    VIOLENCE = 2
    SEXUAL = 3
    YES = 4
    NO = 5
    
    TOP_LEFT = 6
    TOP_RIGHT = 7
    BOT_LEFT = 8
    BOT_RIGHT = 9
    PERSONALIZED = 10
    
    
    def __init__(self, image=None, relative_time=None, duration_time=None):
        self.image = image
        self.relative_time = relative_time
        self.duration_time = duration_time
        self.bondaries = None
        self.position = None
        
    @staticmethod
    def parse_json(json_object, directory=None):
        icon = Icon()
        image = json_object['Icon']['image']
        if image == 'INFO':
            icon.image = Icon.INFO
        elif image == 'VIOLENCE':
            icon.image = Icon.VIOLENCE
        elif image == 'SEXUAL':
            icon.image = Icon.SEXUAL
        elif image == 'YES':
            icon.image = Icon.YES
        elif image == 'NO':
            icon.image = Icon.NO
        else:
            icon.image = adjust_path(image, directory)
        
        if json_object['Icon'].has_key('relative_time'):
            icon.relative_time = json_object['Icon']['relative_time']
            
        if json_object['Icon'].has_key('duration_time'):
            icon.duration_time = json_object['Icon']['duration_time']
            
        if json_object['Icon'].has_key('bondaries'):
            icon.bondaries = Bondaries.parse_json(json_object['Icon']['bondaries'])
            
        if json_object['Icon'].has_key('position'):
            position = json_object['Icon']['position']
            if position == "TOP_LEFT":
                icon.position = Icon.TOP_LEFT
            elif position == 'TOP_RIGHT':
                icon.position = Icon.TOP_RIGHT
            elif position == 'BOT_LEFT':
                icon.position = Icon.BOT_LEFT
            elif position == 'BOT_RIGHT':
                icon.position = Icon.BOT_RIGHT
            elif position == 'PERSONALIZED':
                icon.position = Icon.PERSONALIZED
                
        return icon
    
    def to_json(self):
        json_oject = {'Icon' : {}}
        if self.image == Icon.VIOLENCE:
            json_oject['Icon']['image'] = 'VIOLENCE'
        elif self.image == Icon.SEXUAL:
            json_oject['Icon']['image'] = 'SEXUAL'
        elif self.image == Icon.YES:
            json_oject['Icon']['image'] = 'YES'
        elif self.image == Icon.NO:
            json_oject['Icon']['image'] = 'NO'
        elif self.image == Icon.INFO:
            json_oject['Icon']['image'] = 'INFO'
        else:
            json_oject['Icon']['image'] = self.image
            
        if self.relative_time is not None:
            json_oject['Icon']['relative_time'] = self.relative_time
            
        if self.duration_time is not None:
            json_oject['Icon']['duration_time'] = self.duration_time
            
        if self.bondaries is not None:
            json_oject['Icon']['bondaries'] = self.bondaries.to_json()
            
        if self.position is not None:
            if self.position == Icon.TOP_LEFT:
                json_oject['Icon']['position'] = 'TOP_LEFT'
            elif self.position == Icon.TOP_RIGHT:
                json_oject['Icon']['position'] = 'TOP_RIGHT'
            elif self.position == Icon.BOT_LEFT:
                json_oject['Icon']['position'] = 'BOT_LEFT'
            elif self.position == Icon.BOT_RIGHT:
                json_oject['Icon']['position'] = 'BOT_RIGHT'
            elif self.position == Icon.PERSONALIZED:
                json_oject['Icon']['position'] = 'PERSONALIZED'
            
        return json_oject
        

class Interaction(object):
    def __init__(self):
        pass
    
    @staticmethod
    def parse_json(json_object, directory):
        if json_object.has_key('ShowContent'):
            return ShowContent.parse_json(json_object, directory)
        elif json_object.has_key('Skip'):
            return Skip.parse_json(json_object)
        elif json_object.has_key('Replay'):
            return Replay.parse_json(json_object)
        #elif json_object.has_key('Poll'):
        #    return Poll.parse_json(json_object)
    
    def to_json(self):
        pass

class ShowContent(Interaction):
    SHOW_CONTENT = 0
    SKIP = 1
    BACK_5 = 2
    BACK_TO = 3
    
    def __init__(self):
        super(ShowContent, self).__init__()
        self.contents = []
        self.icon = None
        self.compulsory = False
        self.interactive = False
        self.pause_main_video = False
        self.allow_end_content = True
        self.tv = True
        self.mobile = False
        self.interaction_type = ShowContent.SHOW_CONTENT
        self.skip_point = None
        self.back_point = None
        self.back_limite = None
        self.sound_alert = None
        self.viber_alert = False
        self.button = "GREEN"
        
    @staticmethod
    def parse_json(json_object, directory):
        sc = ShowContent()
        sc.compulsory = json_object['ShowContent']['compulsory']
        sc.interactive = json_object['ShowContent']['interactive']
        sc.pause_main_video = json_object['ShowContent']['pause_main_video']
        sc.allow_end_content = json_object['ShowContent']['allow_end_content']
        sc.tv = json_object['ShowContent']['tv']
        sc.viber_alert = json_object['ShowContent']['viber_alert']
        sc.mobile = json_object['ShowContent']['mobile']
        inttype =  json_object['ShowContent']['interaction_type']
        
        if inttype == 'SHOW_CONTENT':
            sc.interaction_type = ShowContent.SHOW_CONTENT
        elif inttype == 'SKIP':
            sc.interaction_type = ShowContent.SKIP
        elif inttype == 'BACK_5':
            sc.interaction_type = ShowContent.BACK_5
        elif inttype == 'BACK_TO':
            sc.interaction_type = ShowContent.BACK_TO
            
            
        if json_object['ShowContent'].has_key('sound_alert'):
            sc.sound_alert = adjust_path(json_object['ShowContent']['sound_alert'], directory)
            
        if json_object['ShowContent'].has_key('skip_point'):
            sc.skip_point = json_object['ShowContent']['skip_point']
            
        if json_object['ShowContent'].has_key('back_point'):
            sc.back_point = json_object['ShowContent']['back_point']
            
        if json_object['ShowContent'].has_key('back_limite'):
            sc.back_limite = json_object['ShowContent']['back_limite']
            
        if json_object['ShowContent'].has_key('button'):
            sc.button = json_object['ShowContent']['button']
        
        
        if json_object['ShowContent'].has_key('icon'):
            sc.icon = Icon.parse_json(json_object['ShowContent']['icon'], directory)
            
        if json_object['ShowContent'].has_key('contents'):
            for content in json_object['ShowContent']['contents']:
                sc.add_content(Media.parse_json(content, directory))
        
        return sc
    
    def to_json(self):
        json_object = {'ShowContent' : {'compulsory' : self.compulsory,
                                        'pause_main_video' : self.pause_main_video,
                                        'allow_end_content' : self.allow_end_content,
                                        'tv' : self.tv,
                                        'mobile' : self.mobile,
                                        'interactive' : self.interactive,
                                        'viber_alert' : self.viber_alert
                                        }}
        if self.icon is not None:
            json_object['ShowContent']['icon'] = self.icon.to_json()
            
        if self.sound_alert is not None:
            json_object['ShowContent']['sound_alert'] = self.sound_alert
            
            
        json_object['ShowContent']['contents'] = []
        for content in self.contents:
            json_object['ShowContent']['contents'].append(content.to_json())
            
            
        if self.interaction_type == ShowContent.SHOW_CONTENT:
            json_object['ShowContent']['interaction_type'] = 'SHOW_CONTENT'
        elif self.interaction_type == ShowContent.SKIP:
            json_object['ShowContent']['interaction_type'] = 'SKIP'
        elif self.interaction_type == ShowContent.BACK_5:
            json_object['ShowContent']['interaction_type'] = 'BACK_5'
        elif self.interaction_type == ShowContent.BACK_TO:
            json_object['ShowContent']['interaction_type'] = 'BACK_TO'

    
        if self.skip_point is not None:
            json_object['ShowContent']['skip_point'] = self.skip_point
            
        if self.back_limite is not None:
            json_object['ShowContent']['back_limite'] = self.back_limite
            
        if self.back_point is not None:
            json_object['ShowContent']['back_point'] = self.back_point
            
        if self.button is not None:
            json_object['ShowContent']['button'] = self.button
            
        return json_object
        
    def add_content(self, content):
        if not isinstance(content, Media):
            raise TypeError('The argument content must be an instance of Media.')
        
        if content not in self.contents:
            self.contents.append(content)
        else:
            raise Exception('This content is already inserted.')
        
    def remove_content(self, content):
        if not isinstance(content, Media):
            raise TypeError('The argument content must be an instance of Media.')
        
        self.contents.remove(content)
        
    @property
    def type(self):
        return "Content"
        
        
    @property
    def pt_type(self):
        return u"Conteúdo"

                        
class Skip(ShowContent):
    @property
    def type(self):
        return "Skip"
        
        
    @property
    def pt_type(self):
        return u"Pular"

'''class Poll(Interaction):
    @property
    def type(self):
        return "Poll"
        
    @property
    def pt_type(self):
        return u"Enquete"'''

class Replay(ShowContent):
    @property
    def type(self):
        return "Replay"
        
    @property
    def pt_type(self):
        return u"Retroceder"
    


def test():
    pass

if __name__ == "__main__":
    test()
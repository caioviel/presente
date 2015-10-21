import cv2.cv as cv
import cv2

class ImageMatcher():
    def __init__(self, num):
        self.last = None
        self.resize_num = num
        if num == 0:
            self.resize_num = 1
    def resize(self, frame):
        img = cv.GetMat(frame)        
        for _ in range(self.resize_num):
            w, h = cv.GetSize(img)
            small = cv.CreateMat((h + 1) / 2, (w + 1) / 2, img.type)
            cv.PyrDown(img, small)
            img = cv.CreateMat((h + 1) / 2, (w + 1) / 2, img.type)        
            cv.Copy(small, img)
        return small
    
    @staticmethod
    def compareImage(src, dst):
        W, H = cv.GetSize(src)
        w, h = cv.GetSize(dst)
        width = W - w + 1
        height = H - h + 1
    
        if (width > 0) and (height > 0):
            result = cv.CreateImage((width, height), 32, 1)
            cv.MatchTemplate(src, dst, result, cv.CV_TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv.MinMaxLoc(result)
            return max_val
        else: #TODO: raise exception (src size need to be >= dst)
            return -1
      
    def compare(self, img):
        small = self.resize(img)
        result = 0
        if self.last:
            result = self.compareImage(small, self.last)
            if result < 0.999 or result == 1:
                self.last = small
        else:
            self.last = small
        return result


class TransitionDetector():
    def __init__(self, reduction_factor=1, leap_step=10, similarity_threshold=0.99, minimun_spacing=3, minimun_duration=0):
        self.reduction_factor = reduction_factor
        self.leap_step = leap_step
        self.similarity_threshold = similarity_threshold
        self.minimun_spacing = minimun_spacing #Seconds
        self.minimun_duration = minimun_duration
        
    def frame_to_time(self, frame):
        return frame / self._fps

    def detect_transitions(self, filename, imagepath):
        
        capturer = cv.CaptureFromFile(filename)
        self._fps = cv.GetCaptureProperty(capturer , cv.CV_CAP_PROP_FPS)
        detector = ImageMatcher(self.reduction_factor)
        nFrames = cv.GetCaptureProperty(capturer , cv.CV_CAP_PROP_FRAME_COUNT)
        
        print self._fps, nFrames    
        #Fist we will check for all transitions in the video
        frame_number = 0
        transitions_detected = []
        while True:
            img = cv.QueryFrame(capturer)
            if (img == None):
                break;

            #We will ignore some frames during the recognition process
            if frame_number % self.leap_step == 0:
                print 'Frame: %d/%d' % (frame_number, nFrames)
                similarity = detector.compare(img)
                if (similarity < self.similarity_threshold):
                    #logger.info('Transition found at frame %d in time %f', frame_number, float(frame_number)/self._fps)
                    transitions_detected.append((frame_number, similarity))
            frame_number += 1

        #Now we will agroup the transitions in order to detected the points of interest
        #Transitions which occurs too near should be combined in a single point of interest
        print transitions_detected
    
        begin_poi_frame = 0
        last_transition_frame = 0 #Use this number to assure the first transition
        frame_mininum_spacing = self._fps * self.minimun_spacing

        points_of_interest = []
        capturer = cv.CaptureFromFile(filename)
        frameIndex = 0
        img = None
        poiIndex = 0
        for current_frame, similarity in transitions_detected:
            #This frame is spaced enough to figure as a point of interest
            #logger.info('current_frame: %s, last_transition_frame: %s, frame_mininum_spacing: %s', \
            #                 current_frame, last_transition_frame, frame_mininum_spacing)
            if current_frame - last_transition_frame > frame_mininum_spacing:
                #Is this point of interest compound of more than one transition?
                begin_time = self.frame_to_time(begin_poi_frame)
                end_time = self.frame_to_time(last_transition_frame)
                #logger.info('end_time: %s, begin_time: %s, minimun_duration: %s', \
                #             end_time, begin_time, self.minimun_duration)
                
                if end_time - begin_time >= self.minimun_duration:
                    myname = "slide_transition_" + str(poiIndex) + ".png"
                    while frameIndex < begin_poi_frame + 5:
                        import os
                        img = cv.QueryFrame(capturer)
                        frameIndex += 1
                        if img is None:
                            break
                    print "Generating image: ", myname
                    cv.SaveImage(os.path.join(imagepath, myname), img)

                    poi = (begin_time, end_time, myname)
                    #logger.info('Adding Poi')
                    points_of_interest.append(poi)
                    begin_poi_frame = current_frame
                    poiIndex += 1
            else:
                pass
            last_transition_frame = current_frame
        
        #For last frame
        end_time = self.frame_to_time(last_transition_frame)
        begin_time = self.frame_to_time(begin_poi_frame)

        if end_time - begin_time >= self.minimun_duration:
            myname = "slide_transition_" + str(poiIndex) + ".png"
            while frameIndex < begin_poi_frame + 2:
                import os
                img = cv.QueryFrame(capturer)
                frameIndex += 1
                if img is None:
                    break
            print "Generating image: ", frameIndex
            cv.SaveImage(os.path.join(imagepath, myname), img)

            poi = (self.frame_to_time(begin_poi_frame), \
                   self.frame_to_time(last_transition_frame), \
                   myname)
            points_of_interest.append(poi)

        return nFrames/self._fps, points_of_interest
    
def main():
    detector = TransitionDetector()
    print detector.detect_transitions("/home/caioviel/Desktop/screen.mp4")
    
if __name__ == "__main__":
    main()
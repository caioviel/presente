__author__ = 'caioviel'


from threading import Thread, Event, Semaphore
import subprocess as sp
import os
import logging

import platform
if platform.system() == "Windows":
    IS_WINDOWS = True
    IS_LINUX = False
else:
    IS_WINDOWS = False
    IS_LINUX = True

class AVConverter (Thread):
    CONVERTER_NAME = 'avconv'
    FFMPEG_PATH = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

    def __init__(self, params, verbose=False):
        Thread.__init__(self)
        self.params = params
        self.verbose = verbose

        if IS_WINDOWS:
            self.CONVERTER_NAME = os.path.join(self.FFMPEG_PATH, "ffmpeg")

        self.__subprocess = None
        self.__forced_stop = False
        self.err_mng = None
        self.__process_running = False
        self.__end_mutex = Semaphore()
        self.__exit_status = 0
        self.__avconv_finished = Event()
        self.__avconv_finished.clear()

    def run(self):
        cmd = [self.CONVERTER_NAME] + self.params
        logging.warning('Transcoding Command: ' + str(cmd))
        try:
            self.__process_running = True
            if self.verbose:
                if IS_LINUX:
                    self.__subprocess = sp.Popen(cmd)
                else:
                    self.__subprocess = sp.Popen(cmd, creationflags=sp.CREATE_NEW_PROCESS_GROUP)
            else:
                if IS_LINUX:
                    self.__subprocess = sp.Popen(cmd, stderr=sp.PIPE,
                                             stdout=sp.PIPE)
                else:
                    self.__subprocess = sp.Popen(cmd, stderr=sp.PIPE,
                                             stdout=sp.PIPE, creationflags=sp.CREATE_NEW_PROCESS_GROUP)
        except:
            logging.exception("Error on starting Transcoding Process")

        logging.debug("Threading Waiting for avconv die.")
        self.__subprocess.communicate()
        logging.debug("avconv died.")

        self.__end_mutex.acquire()
        self.__process_running = False
        self.__exit_status = self.__subprocess.returncode
        self.__end_mutex.release()

        self.__avconv_finished.set()

        logging.debug("Transcoding return code: %s", str(self.__exit_status))

        if not self.__forced_stop and self.__exit_status < 0:
            #Get the error message from pipe
            out_file = self._subprocess.stderr
            if out_file != None:
                line = out_file.readline()
                previous_line = line
                while line:
                    previous_line = line
                    line = out_file.readline()
                    previous_line = previous_line[:len(previous_line)-1]

                #error = err.Error(err.Error.RECORDING, [previous_line], 'avconv instance stooped abruptly')
                #if self.err_mng == None:
                    logging.error('avconv instance stopped abruptly')
                else:
                    pass
                #self.err_mng.report(error)

    def wait_finish(self):
        logging.debug("AVConverter.wait_finish()")
        try:
            self.__avconv_finished.wait()
        except KeyboardInterrupt:
            logging.debug("KeyBoard Interrupt)")

    def stop(self, waiting=False):
        logging.debug("AVConverter.stop()")
        self.__end_mutex.acquire()
        if self.__process_running:
            import signal
            self.__forced_stop = True
            try:
                if IS_WINDOWS:
                    #import pywin32
                    import os
                    os.kill(self.__subprocess.pid, signal.CTRL_BREAK_EVENT)
                    #pywin32.GenerateConsoleCtrlEvent(pywin32.CTRL_BREAK_EVENT, pgroupid)
                else:
                    self.__subprocess.send_signal(signal.SIGTERM)
                #self._subprocess.wait()
            except:
                logging.exception("Error killing the recording process")
        self.__end_mutex.release()

        if waiting:
            self.wait_finish()


def test():
    conv = AVConverter(["-i",
                        "/home/erick/Desktop/test_video/modulo1_slides.mpeg",
                        "-vcodec", "libx264", "-y",
                        "/home/erick/Desktop/test_video/teste.mp4"], True)
    conv.start()
    conv.wait_finish()

if __name__ == "__main__":
    test()
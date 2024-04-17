from picamera2 import MappedArray, Picamera2, Preview
from libcamera import controls
from picamera2.encoders import H264Encoder, Quality

from fc_camera_server.utils import generate_filename, convert_videos

class CameraHandler:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.configure(
            self.cam.create_video_configuration(main={"size": (1920, 1080),"format": "RGB888"},
                                                  lores={"size": (1920, 1080),"format": "YUV420"})
            # self.cam.create_preview_configuration({"size": (1024, 768)})
            # self.cam.create_preview_configuration({"size": (1440, 1080)})
        )
        self.mode = "lores"
        self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous, "FrameRate": 20})
        self.recording = False
        self.encoder = H264Encoder(10000000)
        

    def start(self):
        self.cam.start()
        self.recording = True

    def stop(self):
        # self.cam.stop()
        self.recording = False
    def start_recording(self):
        self.cam.start_recording(self.encoder, generate_filename(".h264"),name=self.mode, quality=Quality.MEDIUM)
        print("Recording started")
    def stop_recording(self):
        self.cam.stop_recording()
        print("Recording paused")
    def convert_vids(self):
        convert_videos("recs/20240416")

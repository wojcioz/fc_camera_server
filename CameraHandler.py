from picamera2 import MappedArray, Picamera2, Preview
from libcamera import controls
from picamera2.encoders import H264Encoder, Quality

from utils import generate_filename, convert_videos

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
def generate_frames():

    global cam_handler
    # time.sleep(0.1)  # allow the camera to warmup
    encoder = H264Encoder(10000000)
    while True:
        time.sleep(0.1)
        if not cam_handler.recording:
            break
        try:
            # array = cam_handler.cam.capture_array()
            
            cam_handler.cam.start_recording(encoder, 'test.h264')
            # _, jpeg = cv2.imencode('.jpg', array)
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            if not cam_handler.recording:
                break
        except Exception as e:
            print(f"Error: {e}")
            continue
    cam_handler.cam.stop_recording()
    print("Stopping frame generation")
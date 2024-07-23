import sys, os, cv2, base64
from PIL import Image
import numpy as np
from . import amcam
from cam.helper.functions import Functions

class AmscopeCamera:
    def __init__(self):
        self.hcam = None
        self.buf = None
        self.total = 0
        self.latest_frame = None
        self.resolutions = []
        self.selectedResolution = None
        self.snapResolution = None
        self.snapImage = None

    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == amcam.AMCAM_EVENT_IMAGE:
            ctx.CameraCallback(nEvent)

    def CameraCallback(self, nEvent):
        if nEvent == amcam.AMCAM_EVENT_IMAGE:
            try:
                self.hcam.PullImageV2(self.buf, 24, None)
                self.total += 1

            except amcam.HRESULTException as ex:
                print("pull image failed, hr")
        else:
            print("event callback: {}".format(nEvent))
        return b""

    def stop(self):
        if self.hcam == None:
            return False
        self.hcam.Close()
        self.hcam = None

    def isOpen(self):
        return self.hcam != None

    def snap(self):
        info = None  # Initialize FrameInfoV2 (you might need to adjust this)
        width, height = self.hcam.get_Size()

        sbmp = Image.new("RGB", (width, height))

        np_image = np.array(sbmp)
        self.hcam.PullStillImageV2(np_image.tobytes()[:3], 24, info)

        sbmp = Image.fromarray(np_image)
        self.snapImage = sbmp

    def snap_base64(self):
        width, height = self.hcam.get_Size()
        encoded_image = Functions.encodeBytesAsJPG(self.buf, width, height, 99)
        encoded_image_base64 = base64.b64encode(encoded_image).decode("utf-8")
        return encoded_image_base64
        
    def get_frame_rate(self):
        frame, nTime, totalFrame = self.hcam.get_FrameRate()
        return frame * 1000 / nTime

    def selectResolution(self, index: int):
        self.hcam.put_eSize(index)
        resolution = self.hcam.get_Size()
        self.selectResolution = resolution
        print(f"selected resolution is {self.selectedResolution}")

    def selectSnapResolution(self, index: int):
        self.snapResolution = self.resolutions[index]

    def run(self):
        a = amcam.Amcam.EnumV2()
        if len(a) > 0:
            print(
                "{}: flag = {:#x}, preview = {}, still = {}".format(
                    a[0].displayname,
                    a[0].model.flag,
                    a[0].model.preview,
                    a[0].model.still,
                )
            )
            self.resolutions = a[0].model.res
            for r in a[0].model.res:
                print("\t = [{} x {}]".format(r.width, r.height))
            self.hcam = amcam.Amcam.Open(a[0].id)
            if self.hcam:
                try:
                    self.snapResolution = self.resolutions[0]
                    self.hcam.put_eSize(0)
                    width, height = self.hcam.get_Size()
                    self.selectedResolution = self.hcam.get_Size()
                    print(f"selected resolution is {self.selectedResolution}")
                    bufsize = ((width * 24 + 31) // 32 * 4) * height
                    print(
                        "image size: {} x {}, bufsize = {}".format(
                            width, height, bufsize
                        )
                    )
                    self.buf = bytes(bufsize)
                    if self.buf:
                        try:
                            self.hcam.StartPullModeWithCallback(
                                self.cameraCallback, self
                            )
                        except amcam.HRESULTException as ex:
                            print("failed to start camera, hr=0x{:x}".format(ex.hr))
                    input("press ENTER to exit")
                finally:
                    print("failed to open the camera")
            else:
                print("failed to open camera")
        else:
            print("no camera found")

    def start_camera(self):
        a = amcam.Amcam.EnumV2()
        if len(a) > 0:
            self.hcam = amcam.Amcam.Open(a[0].id)
            if self.hcam:
                try:
                    width, height = self.hcam.get_Size()
                    bufsize = ((width * 24 + 31) // 32 * 4) * height
                    self.buf = bytes(bufsize)
                    if self.buf:
                        try:
                            self.hcam.StartPullModeWithCallback(
                                self.cameraCallback, self
                            )
                            return "Camera started successfully."
                        except amcam.HRESULTException as ex:
                            return f"Failed to start camera"
                except Exception as e:
                    return str(e)
        return "No camera found."

    def stop_camera(self):
        if self.hcam:
            self.hcam.Close()
            self.hcam = None
            self.buf = None
        cv2.destroyAllWindows()

    def get_image_base64(self):
        if self.current_image is not None:
            _, buffer = cv2.imencode(".jpg", self.current_image)
            img_base64 = base64.b64encode(buffer).decode("utf-8")
            return img_base64
        return None

    def set_resolution(self, width, height):
        if self.hcam:
            try:
                self.hcam.set_Size(width, height)
                return "Resolution set successfully."
            except amcam.HRESULTException as ex:
                return f"Failed to set resolution"
        return "Camera not started."

    def get_resolutions(self):
        if self.hcam:
            try:
                resolutions = self.hcam.get_Resolutions()
                return [{"width": r.width, "height": r.height} for r in resolutions]
            except amcam.HRESULTException as ex:
                return f"Failed to get resolutions"
        return "Camera not started."

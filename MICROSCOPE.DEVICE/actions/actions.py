from cam.AmscopeCamera import AmscopeCamera
from motion.motion import StageMotion
import asyncio


class Actions:
    def __init__(self, camera: AmscopeCamera):
        self.stage = StageMotion()
        self.camera = camera

    async def snap(self, steps: int):
        images = []
        indeces = []
        self.stage.move(4, steps / 2)
        for i in range(steps):
            images.append(self.camera.snap_base64())
            indeces.append(i)
            self.stage.move(5, i)
            asyncio.sleep(1)
        return (images, indeces)

    def generateMotionPattern(startpoint, endpoint):
        pass

    async def scan(self):
        pass
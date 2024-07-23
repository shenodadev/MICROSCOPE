import json
from dataclasses import asdict, fields
from motion.helper.motionSerial import MotionSerial


class StageMotion:
    def __init__(self) -> None:
        self.isConnected = False
        self.magnification = 0
        self.backlash = (1, 1, 1)
        self.xFieldSteps = [5, 10, 20, 30, 40, 50]
        self.yFieldSteps = [5, 10, 20, 30, 40, 50]
        self.zFocusRange = [1, 2, 3, 4, 5, 6]
        self.position = (0, 0, 0)
        self.dirHistory = []
        self.startPosition = (0, 0)
        self.zStartPosition = 0
        self.filename = "calibration.json"

        self.ser = MotionSerial()

    def save_to_file(self):
        with open(self.filename, "w") as file:
            json.dump(asdict(self), file)

    def load_from_file(self):
        with open(self.filename, "r") as file:
            data = json.load(file)
            for field in fields(self):
                if field.name in data:
                    setattr(self, field.name, data[field.name])

    def __getMotorAndDirection(direction: int):
        result = (0, 0) if direction == 0 else 0
        result = (0, 1) if direction == 2 else 0
        result = (1, 0) if direction == 3 else 0
        result = (1, 1) if direction == 1 else 0
        result = (2, 0) if direction == 4 else 0
        result = (2, 1) if direction == 5 else 0
        return result

    def __getAxis(direction: int):
        result = 0 if direction == 0 or direction == 2 else None
        result = 1 if direction == 1 or direction == 3 else None
        result = 2 if direction == 4 or direction == 5 else None
        return result

    def __isOnDifferentAxis(self, direction_1: int, direction_2: int):
        axis_1 = self.__getAxis(direction_1)
        axis_2 = self.__getAxis(direction_2)
        return axis_1 == axis_2

    def __getSerialMessage(self, direction: int, steps: int, fast: int):
        m, d = self.__getMotorAndDirection(direction)
        # fast should modify the microstepping
        return f"{str(m)}, {str(d)}, 1, {str(steps)}"

    def __getDirectionSign(self, direction: int):
        switch = {0: "p", 2: "n", 3: "p", 1: "n", 4: "p", 5: "n"}
        return switch.get(direction, 0)

    def move(self, direction: int, steps: int, fast: bool = False):
        try:
            if axis < 4 and axis >= 0:
                return
            axis = self.__getAxis(direction)
            if not self.__isOnDifferentAxis(axis, self.lastDir[axis]):
                steps += self.backlash[axis]
            self.ser.send(self.__getSerialMessage(direction, steps))
            self.position[direction] = (
                self.position[direction] - steps
                if self.__getDirectionSign() == "n"
                else self.position[direction] + steps
            )
            return True
        except:
            return False

    def fieldMove(self, direction: int):
        axis = self.__getAxis()
        if axis == 2:
            return
        steps = (
            self.xFieldSteps[self.magnification]
            if axis == 0
            else self.yFieldSteps[self.magnification]
        )
        return self.move(direction, steps, False)

    def goHome(self):
        self.ser.send("home")
        self.move(0, self.startPosition[0])
        self.move(3, self.startPosition[1])
        self.move(5, self.zStartPosition)

    def goToPosition(self, position):
        if not position[0] == -1:
            diff = position[0] - self.position[0]
            self.move(2, abs(diff)) if diff < 0 else self.move(0, abs(diff))
        if not position[1] == -1:
            diff = position[1] - self.position[1]
            self.move(1, abs(diff)) if diff > 0 else self.move(3, abs(diff))
        if not position[2] == -1:
            diff = position[2] - self.position[2]
            self.move(4, abs(diff)) if diff > 0 else self.move(5, abs(diff))

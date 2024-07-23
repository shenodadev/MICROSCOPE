from quart import Response, request, Blueprint, jsonify
from motion.motion import StageMotion

motion_bp = Blueprint("Motion", __name__)

motion = StageMotion()


@motion_bp.route("get-magnification", methods=["GET"])
async def getMagnification():
    return motion.magnification()


@motion_bp.route("get-position", methods=["GET"])
async def getPosition():
    position = motion.position
    return {"x": position[0], "y": position[1], "z": position[2]}


@motion_bp.route("move", methods=["POST"])
async def move():
    if not motion.isConnected:
        return False
    input = await request.get_json()
    direction = input.get("direction")
    steps = input.get("steps")
    fast = input.get("fast")
    return move(direction, steps, fast)


@motion_bp.route("field-move", methods=["POST"])
async def fieldMove():
    if not motion.isConnected:
        return False
    input = await request.get_json()
    direction = input.get("direction")
    return motion.fieldMove(direction)


@motion_bp.route("go-to-position", methods=["POST"])
async def goToPosition():
    if not motion.isConnected:
        return False
    input = await request.get_json()
    x = input.get("x")
    y = input.get("y")
    z = input.get("z")
    return motion.goToPosition((x, y, z))


@motion_bp.route("change-magnification", methods=["POST"])
async def changeMagnification():
    input = await request.get_json()
    magnification = input.get("magnification")
    motion.magnification = magnification


@motion_bp.route("goHome", methods=["POST"])
async def goHome():
    if not motion.isConnected:
        return False
    motion.goHome()

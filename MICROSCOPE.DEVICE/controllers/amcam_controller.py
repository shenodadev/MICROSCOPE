from quart import Blueprint, Response, jsonify, request
from cam.AmscopeCamera import AmscopeCamera
from cam.helper.functions import Functions

camera_bp = Blueprint("camera", __name__)


camera_app = AmscopeCamera()


def openCameraIfClosed():
    if not camera_app.isOpen():
        camera_app.start_camera()


@camera_bp.route("/start_camera", methods=["GET"])
async def start_camera():
    if camera_app.isOpen():
        return jsonify({"message:": "camera is already open"})
    message = camera_app.start_camera()
    return jsonify({"message": message})


@camera_bp.route("/stop_camera", methods=["POST"])
async def stop_camera():
    camera_app.stop_camera()
    return jsonify({"message": "Camera stopped successfully."})


@camera_bp.route("/set_resolution", methods=["POST"])
async def set_resolution():
    openCameraIfClosed()
    data = request.json
    width = data.get("width")
    height = data.get("height")
    if width and height:
        message = camera_app.set_resolution(width, height)
        return jsonify(message)
    return jsonify({"error": "Width and height required."})


@camera_bp.route("/get_resolutions", methods=["GET"])
async def get_resolutions():
    openCameraIfClosed()
    resolutions = camera_app.get_resolutions()
    return jsonify({"resolutions": resolutions})


@camera_bp.route("/video_feed")
async def video_feed():
    openCameraIfClosed()
    def generate_frames():
        while True:
            if camera_app.buf is not None:
                width, height = camera_app.hcam.get_Size()
                buffer = Functions.encodeBytesAsJPG(camera_app.buf, width, height, 100)
                frame = buffer.tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            else:
                break

    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

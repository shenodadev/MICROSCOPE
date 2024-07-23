from flask import Flask, jsonify, request, send_file, Response
import cam.amcam as amcam
from PIL import Image
import cv2, io, base64
import numpy as np
from cam.helper.functions import Functions
from cam.AmscopeCamera import AmscopeCamera

app = Flask(__name__)


camera_app = AmscopeCamera()
camera_app.start_camera()


@app.route("/start_camera", methods=["GET"])
def start_camera():
    message = camera_app.start_camera()
    return jsonify({"message": message})


@app.route("/stop_camera", methods=["POST"])
def stop_camera():
    camera_app.stop_camera()
    return jsonify({"message": "Camera stopped successfully."})


@app.route("/set_resolution", methods=["POST"])
def set_resolution():
    data = request.json
    width = data.get("width")
    height = data.get("height")
    if width and height:
        message = camera_app.set_resolution(width, height)
        return jsonify(message)
    return jsonify({"error": "Width and height required."})


@app.route("/get_resolutions", methods=["GET"])
def get_resolutions():
    resolutions = camera_app.get_resolutions()
    return jsonify({"resolutions": resolutions})


@app.route("/video_feed")
def video_feed():
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



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
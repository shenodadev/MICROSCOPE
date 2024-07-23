from quart import Quart
from controllers.amcam_controller import camera_bp
from controllers.motion_controller import motion_bp
from controllers.actions_controller import actions_bp
from motion.helper.motionSerial import MotionSerial


app = Quart(__name__)

# Register the blueprint
app.register_blueprint(camera_bp, url_prefix="/camera")
app.register_blueprint(motion_bp, url_prefix="/motion")
app.register_blueprint(actions_bp, url_prefix="/actions")

# motionSerial = MotionSerial()

# for i in range(1, 10):
#     motionSerial.send("0,1,1,500")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)

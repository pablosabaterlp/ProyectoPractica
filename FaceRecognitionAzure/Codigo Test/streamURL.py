from flask import Flask, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)
DefaultEndpointsProtocol=https;AccountName=chls1zu1stapocaaicrit001;AccountKey=/BedihAGA1pvMxv8MGVPpumEt0YQKxHPVtZPO7j9vm68h0JGGmBtKE/EbqWbjqaSZ5e0z+kbqtrL+AStW+==;EndpointSuffix=core.windows.net
def generateFrame():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            red, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(generateFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="IP", port=5000)

#http://localhost:5000/video_feed.

from flask import Flask, jsonify, send_file
from PIL import Image, ImageDraw
import threading
import time
import os

app = Flask(__name__)

def capture_photo(camera_index, output_file):
    image = Image.new('RGB', (640, 480), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), f"Camera {camera_index} - Placeholder", fill=(0, 0, 0))
    image.save(output_file)
    time.sleep(1)  

def capture_and_stitch():
    thread1 = threading.Thread(target=capture_photo, args=(0, 'camera0.jpg'))
    thread2 = threading.Thread(target=capture_photo, args=(1, 'camera1.jpg'))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    image1 = Image.open('camera0.jpg')
    image2 = Image.open('camera1.jpg')

    total_width = image1.width + image2.width
    max_height = max(image1.height, image2.height)
    combined_image = Image.new('RGB', (total_width, max_height))

    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (image1.width, 0))

    combined_image.save('combined.jpg')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        capture_and_stitch()
        return jsonify({"status": "success", "message": "Photo captured and stitched"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/image', methods=['GET'])
def get_image():
    try:
        return send_file('combined.jpg', mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

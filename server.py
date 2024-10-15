from flask import Flask, jsonify, send_file
import subprocess
from PIL import Image

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture_image():
    take_photo(0, 'camera0.jpg')
    take_photo(1, 'camera1.jpg')
    combine_photos('camera0.jpg', 'camera1.jpg', 'combined.jpg')
    return jsonify({'status': 'success', 'message': 'Photo captured'})

@app.route('/image', methods=['GET'])
def get_image():
    return send_file('combined.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

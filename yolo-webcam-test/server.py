from flask import Flask, request, jsonify
from flask_cors import CORS  # Ensure this import is present
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

model_path = 'C:/Users/saaso/Desktop/MachineVisionAR/objDetection/runs/models/best.pt'
model = YOLO(model_path)

@app.route('/detect', methods=['POST'])
def detect():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']
        if not file:
            return jsonify({'error': 'No image provided'}), 400

        image = Image.open(io.BytesIO(file.read()))
        results = model(image)
        
        detections = []

        if results:
            detection_tensor = results[0].boxes.xyxy[0]
            confs = results[0].boxes.conf
            print(f"Detections tensor: {detection_tensor}")
            print(("confs: ", confs, " confs type: ", type(confs), " confs[0]: ", confs[0]))
            # Assuming the tensor is [x1, y1, x2, y2] for a single detection
            if detection_tensor.numel() == 4:
                x1, y1, x2, y2 = detection_tensor.tolist()
                # Label for the single class
                label = results[0].names[0]  # Assuming the class name is stored here

                detections.append({
                    "xmin": int(x1),
                    "ymin": int(y1),
                    "xmax": int(x2),
                    "ymax": int(y2),
                    "confidence": float(max(confs)),
                    "name": label
                })

        return jsonify({'detections': detections})



if __name__ == '__main__':
    app.run(debug=True)

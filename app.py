import time
from absl import app, logging
import cv2
import numpy as np
import mysql.connector
from datetime import datetime
import tensorflow as tf
from yolotf2.models import (
    YoloV3
)
from yolotf2.dataset import transform_images
# from yolotf2.utils import draw_outputs
from flask import Flask, request, jsonify, abort,render_template
import os

# customize your API through the following parameters
classes_path = './data/labels/coco.names'
weights_path = 'parkingmodel.h5'
tiny = False                    # set to True if using a Yolov3 Tiny model
size = 416                      # size images are resized to for model
output_path = '/'   # path to output folder where images with detections are saved
num_classes = 1                # number of classes in model


yolo = YoloV3(classes=num_classes)

yolo.load_weights(weights_path)
print('weights loaded')

class_names = [c.strip() for c in open(classes_path).readlines()]
print('classes loaded')

# Initialize Flask application
app = Flask(__name__)

# Render HTML page for the root URL
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detections')
def show_detections():
    response_data = {
        'info': 'just send the payload image to hit this URL.'
    }
    return jsonify(response_data)

# API that returns JSON with classes found in images
@app.route('/detections', methods=['POST'])
def get_detections():
    raw_images = []
    images = request.files.getlist("images")
    print(images)
    image_names = []
    for image in images:
        image_name = image.filename
        image_names.append(image_name)
        image.save(os.path.join(os.getcwd(), image_name))
        img_raw = tf.image.decode_image(
            open(image_name, 'rb').read(), channels=3)
        raw_images.append(img_raw)
        
    num = 0
    
    # create list for final response
    response = []

    for j in range(len(raw_images)):
        # create list of responses for current image
        responses = []
        raw_img = raw_images[j]
        num+=1
        img = tf.expand_dims(raw_img, 0)
        img = transform_images(img, size)

        t1 = time.time()
        boxes, scores, classes, nums = yolo(img)
        t2 = time.time()
        print('time: {}'.format(t2 - t1))

        print('detections:')
        class_counts = {}

        for i in range(nums[0]):
            detected_class = class_names[int(classes[0][i])]
            confidence = float("{0:.2f}".format(np.array(scores[0][i]) * 100))

            # Print or process the detection information
            print('\t{}, {}, {}'.format(detected_class, confidence, np.array(boxes[0][i])))

            # Append the detection to the responses list
            responses.append({
                "class": detected_class,
                "confidence": confidence
            })

            # Update the count for the detected class
            class_counts[detected_class] = class_counts.get(detected_class, 0) + 1

        # Add the final response entry to the response list
        response_entry = {
            "image": image_names[j],
            "detections": responses
        }

        # Add the total counts for each class to the response
        class_totals = [{"class": cls, "total_count": count} for cls, count in class_counts.items()]
        response_entry["class_totals"] = class_totals

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="hitung_motor"
            )

            # Create a MySQL cursor
            cursor = connection.cursor()
            print("Connected to MySQL database!")
            
             # Get timestamp and date
            timestamp = datetime.now()
            date = timestamp.date()

            # Iterate over class counts and update the database
            for class_name, count in class_counts.items():
                # Assuming you have a table named 'parking_data' with columns 'id', 'date', 'time', and 'vehicle_count'
                insert_query = "INSERT INTO parking_data (date, time, vehicle_count) VALUES (%s, %s, %s)"
                insert_data = (date, timestamp, count)

                cursor.execute(insert_query, insert_data)
                connection.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and connection
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("Connection closed.")
                response.append(response_entry)
                
        # debugging yolov3 utilities
        # img = cv2.cvtColor(raw_img.numpy(), cv2.COLOR_RGB2BGR)
        # img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
        # cv2.imwrite(output_path + 'detection' + str(num) + '.jpg', img)
        # print('output saved to: {}'.format(output_path + 'detection' + str(num) + '.jpg'))

    #remove temporary images
    for name in image_names:
        os.remove(name)
    try:
        return jsonify({"response":response}), 200
    except FileNotFoundError:
        abort(404)
if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=5000)

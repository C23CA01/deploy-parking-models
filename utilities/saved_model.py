from absl import app, flags, logging
from absl.flags import FLAGS
import numpy as np
from yolotf2.models import YoloV3, YoloV3Tiny
from yolotf2.utils import load_darknet_weights

# move to app.py
flags.DEFINE_string('weights', './yolov3_training_final.weights', 'path to weights file')
flags.DEFINE_string('output', './parkingmodel.h5', 'path to output .h5 file')  # Modified file extension
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('num_classes', 1, 'number of classes in the model')

def main(_argv):
    if FLAGS.tiny:
        yolo = YoloV3Tiny(classes=FLAGS.num_classes)
    else:
        yolo = YoloV3(classes=FLAGS.num_classes)
    yolo.summary()
    logging.info('model created')

    load_darknet_weights(yolo, FLAGS.weights, FLAGS.tiny)
    logging.info('weights loaded')

    img = np.random.random((1, 320, 320, 3)).astype(np.float32)
    output = yolo(img)
    logging.info('sanity check passed')

    # Save the model's weights in HDF5 format
    yolo.save_weights(FLAGS.output, save_format='h5')  # Use save_weights method
    logging.info('model weights saved in HDF5 format')

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

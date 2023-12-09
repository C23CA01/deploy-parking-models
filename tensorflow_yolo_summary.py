from absl import app, flags, logging
from absl.flags import FLAGS
import numpy as np
from yolotf2.models import YoloV3, YoloV3Tiny
from yolotf2.utils import load_darknet_weights

# move to app.py
flags.DEFINE_string('weights', './parkingmodel.h5', 'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('num_classes', 1, 'number of classes in the model')

def main(_argv):
    if FLAGS.tiny:
        yolo = YoloV3Tiny(classes=FLAGS.num_classes)
    else:
        yolo = YoloV3(classes=FLAGS.num_classes)
    yolo.summary()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

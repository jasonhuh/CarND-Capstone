from styx_msgs.msg import TrafficLight

import rospy
import sys
import os
import numpy as np
import cv2
from PIL import Image
from glob import glob
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.models import load_model
import tensorflow as tf

CLASSIFICATION_THRESHOLD = 0.5
cur_dir = os.path.dirname(os.path.realpath(__file__))

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)    

class TLClassifier(object):
    def __init__(self):
        
        self.current_light = TrafficLight.UNKNOWN
        os.chdir(cur_dir)

        MODEL_NAME = 'letsdoit'
        PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'
        self.graph = tf.Graph()

        # Enable GPU
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True

        with self.graph.as_default():
            self.od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
                serialized_graph = fid.read()
                self.od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(self.od_graph_def, name='')

            self.image_tensor = self.graph.get_tensor_by_name('image_tensor:0')
            self.d_boxes = self.graph.get_tensor_by_name('detection_boxes:0')
            self.d_classes = self.graph.get_tensor_by_name('detection_classes:0')
            self.d_scores = self.graph.get_tensor_by_name('detection_scores:0')
            self.num_d = self.graph.get_tensor_by_name('num_detections:0')

        self.sess = tf.Session(graph=self.graph)


    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        rospy.loginfo('GET_CLASSIFICATION....')

        # image = adjust_gamma(image, 0.8)

        # Bounding Box Detection.
        with self.graph.as_default():
            # Expand dimension since the model expects image to have shape [1, None, None, 3].
            img_expanded = np.expand_dims(image, axis=0)  
            (boxes, scores, classes, num) = self.sess.run(
                [self.d_boxes, self.d_scores, self.d_classes, self.num_d],
                feed_dict={self.image_tensor: img_expanded})
        
        # create np arrays
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)

        self.current_light = TrafficLight.UNKNOWN

        if scores is not None and scores[0] > CLASSIFICATION_THRESHOLD:  # If highest score is above 50% it's a hit
            if classes[0] == 1:
                self.current_light = TrafficLight.GREEN
                rospy.loginfo('-------GREEN-------')
            elif classes[0] == 2:
                self.current_light = TrafficLight.RED
                rospy.loginfo('-------RED-------')
            elif classes[0] == 3:
                self.current_light = TrafficLight.YELLOW
                rospy.loginfo('-------YELLOW-------')
            else:
                rospy.loginfo('-------UNKNOWN-------')                
        
        return self.current_light


if __name__ == '__main__':
    def test_images():
        print('Green', TrafficLight.GREEN)
        print('Yellow', TrafficLight.YELLOW)
        print('Red', TrafficLight.RED)
        image_paths = glob(os.path.join('images/', '*.png'))
        for i, path in enumerate(image_paths, start=1):
            img = Image.open(path)
            img_np = load_image_into_numpy_array(img)
            # img_np = cv2.resize(img_full_np_copy[b[0]:b[2], b[1]:b[3]], (32, 32))
            result = tl_classifier.get_classification(img_np)
            print(i, path, result)
    try:
        
        # Supress  'The TensorFlow library wasn't compiled to use SSE instructions, ...' warning.
        # Reference: https://github.com/tensorflow/tensorflow/issues/7778
        os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
        tl_classifier = TLClassifier()
        test_images()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start traffic classifier.')
    

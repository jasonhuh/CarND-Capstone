from styx_msgs.msg import TrafficLight

import sys
import os
import tensorflow as tf

cur_dir = os.path.dirname(os.path.realpath(__file__))

class TLClassifier(object):
    def __init__(self):
        pass
        #TODO load classifier

        # Change directory to the current directory
        
        os.chdir(cur_dir)

        MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
        PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()

        # Enable GPU
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True

        with self.detection_graph.as_default():
            self.od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
                serialized_graph = fid.read()
                self.od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(self.od_graph_def, name='')
            with tf.Session() as sess:
                # Get handles to input and output tensors
                ops = tf.get_default_graph().get_operations()            

            self.image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
            self.detection_boxes = tf.get_default_graph().get_tensor_by_name('detection_boxes:0')
            self.detection_classes = tf.get_default_graph().get_tensor_by_name('detection_classes:0')
            self.detection_scores = tf.get_default_graph().get_tensor_by_name('detection_scores:0')


    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        return TrafficLight.UNKNOWN


if __name__ == '__main__':
    # def test_images():
    #     image_paths = glob(os.path.join('images/', '*.jpg'))
    #     for i, path in enumerate(image_paths):
    #         print(, path)
    try:
        
        # Supress  'The TensorFlow library wasn't compiled to use SSE instructions, ...' warning.
        # Reference: https://github.com/tensorflow/tensorflow/issues/7778
        os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
        tl_classifier = TLClassifier()
        #test_images()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start traffic classifier.')    
    

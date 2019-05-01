from tensorflow.python.client import device_lib
print ("TensorFlow List of deviced")
print ("="*80)
print (device_lib.list_local_devices())

import tensorflow as tf
print ("TensorFlow Test GPU")
print ("="*80)
if tf.test.gpu_device_name():
	print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
   print("MIKE... GPU does not seem to be working")

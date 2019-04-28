cat dataset_train_rgb.zip* > dataset_train_rgb.zip
unzip dataset_train_rgb.zip
python dataSet2TFEformat.py
creates one huge dataFile in output/myOuput
had to add to PYTHONPATH in .bashrc to the /usr/local/lib/python2.7/dist-packages/tensorflow/models/research/object_detection (which was added in one of the install steps)


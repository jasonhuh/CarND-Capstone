CarND-Capstone\BoschTlDataSet\README.txt

https://hci.iwr.uni-heidelberg.de/node/6132
  - here you need to apply for a link to data download area...
  - Once you have the access to the download site... 
  - Download all 4 files 
    - dataset_train_rgb.zip 001-to-004

$ cat dataset_train_rgb.zip* > dataset_train_rgb.zip
$ unzip dataset_train_rgb.zip
$ python dataSet2TFEformat.py
  - creates one huge dataFile in output/myOuput
  - had to add to PYTHONPATH in .bashrc to the /usr/local/lib/python2.7/dist-packages/tensorflow/models/research/object_detection (which was added in one of the install steps)


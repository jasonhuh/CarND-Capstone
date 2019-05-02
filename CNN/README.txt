CarND-Capstone\CNN\README.txt


The following is the command to start training the model... You need to populate many files in this directory structure to support the training (tensorflow training)

MODEL
=====
models/research/object_detection/g3doc/detection_model_zoo.md
  - download a model  
  - I choose 
    - rfcn_resnet101_coco
  - copy 3 model.ckpt.* files to CarND-Capstone\CNN\models\.

CONFIG FILE
===========
rfcn_resnet101_coco.config
  - models/model.ckpt  : original trained model to start from (transfer training)
    - from tensorflow models/research/object_detection... 
    - need to download, then copy over
  - data/letsDoIt.pbtxt : 1='Red' 2='Yellow'...
  - data/trainData      : from BOSCH TL data (see CarND-Capstone\BoschTlDataSet\README.txt)
  - data/evalData       : (same)
  - num_steps: 200000   : length of training  

TRAIN (legacy)
=====
just run the train.py script... This was copied from models/research/object_detection/legacy... There is a newer way to do this as well...  (Perhaps I will switch over once things are working better)
  - models/research/object_detection/legacy/train.py  #copied from here
$ python train.py --logtostderr --train_dir=./models/train --pipeline_config_path=rfcn_resnet101_coco.config

TRAIN/EVAL
==========
Need to try the better approach... FIXME
python model_main.py --pipeline_config_path=rfcn_resnet101_coco.config --model_dir=models --num_train_steps=50000 --sample_1_of_n_eval_examples=1 --logtostderr

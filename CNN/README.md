# CarND-Capstone\CNN\README.md


The following is the command to start training the model... You need to populate many files in this directory structure to support the training (tensorflow training)

## Step 1 - Augment pre-built rfcn_resnet101_coco with Bosch images

### MODEL
***


https://github.com/tensorflow/models/blob/dc78c0853b8a0684801c8b849b5605077de9ee9e/research/object_detection/g3doc/detection_model_zoo.md (The models in this link are compatible with Tensorflow 1.3.)

  - download a model  
  - I choose 
    - rfcn_resnet101_coco
  - copy 3 model.ckpt.* files to CarND-Capstone\CNN\models\.

### CONFIG FILE
***
rfcn_resnet101_coco.config
  - models/model.ckpt  : original trained model to start from (transfer training)
    - from tensorflow models/research/object_detection... 
    - need to download, then copy over
  - data/bosch.pbtxt : 1='Green' 2='Gred' 3='Yellow' 4='Off' ...
  - data/trainData      : from BOSCH TL data (see CarND-Capstone\BoschTlDataSet\README.txt)
  - data/evalData       : (same)
  - num_steps: 100000   : length of training  

### TRAIN

***
just run the train.py script... This was copied from models/research/object_detection/legacy... There is a newer way to do this as well...  (Perhaps I will switch over once things are working better)
  - models/research/object_detection/legacy/train.py  #copied from here
```  
$ python train.py --logtostderr --train_dir=./models/bosch_train --pipeline_config_path=rfcn_resnet101_coco.config
```

### TRAIN/EVAL - Boasch image files (Works only with Tensorflow 1.12 and above)
Note: The `train.py` has been moved to `lelgacy` folder in the Tensorflow Models, and the `model_main.py` is a modern way of performing training and evaluating. Unfortunately, this does not work with Tensorflow 1.3. For this project, the team used the `train.py` instead.
***
Need to try the better approach... FIXME
$ python model_main.py --pipeline_config_path=rfcn_resnet101_coco.config --model_dir=models --num_train_steps=50000 --sample_1_of_n_eval_examples=1 --logtostderr

Alternative command:
$ python model_main.py --logtostderr --pipeline_config_path=rfcn_resnet101_coco.config --model_dir=models/train 

### Tensorboard
***
```bash
$ cd models/bosch_train
$ tensorboard --logdir=./
```

### Save a Checkpoint Model (.ckpt) as a .pb File
***
```bash
python export_inference_graph.py --input_type image_tensor --pipeline_config_path ./rfcn_resnet101_coco.config --trained_checkpoint_prefix ./models/bosch_train/model.ckpt-50000 --output_directory ./fine_tuned_model/bosch
```
## Step 2 - Furthur Augment model from Step 1 with with TL bag file images


### TRAIN

***
Train the TL Bag images using the Bosch model created from Step 1.

```  
$ python train.py --logtostderr --train_dir=./models/letsdoit_train --pipeline_config_path=letsdoit.config
```



### TRAIN/EVAL - TlBagFile files
Note: The `train.py` has been moved to `lelgacy` folder in the Tensorflow Models, and the `model_main.py` is a modern way of performing training and evaluating. Unfortunately, this does not work with Tensorflow 1.3. For this project, the team used the `train.py` instead.
***
```bash
$ python model_main.py --pipeline_config_path=letsdoit.config --model_dir=models/letsdoit_train --num_train_steps=20000 --sample_1_of_n_eval_examples=1 --logtostderr
```



### Tensorboard - TlBagFile files
***
```bash
$ cd models/letsdoit_train
$ tensorboard --logdir=./
```

### Save a Checkpoint Model (.ckpt) as a .pb File
***
```bash
python export_inference_graph.py --input_type image_tensor --pipeline_config_path ./letsdoit.config --trained_checkpoint_prefix ./models/letsdoit_train/model.ckpt-20000 --output_directory ./fine_tuned_model/letsdoit
```
This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

[//]: # (Image References)

[image1]: ./imgs/bosch_detected_image1.png "Bosch TL Detection"
[image2]: ./imgs/tlbag_detected_image.png "Drive test TL Detection"
[image3]: ./imgs/training_loss_results.png "Training Loss Results"

### Team LetsDoIt

#### Members
* Jason Huh jasonhuh@hotmail.com
* Prashant Aravind Borse paborse@outlook.com
* Michael LachMayr mlachmayr@gmail.com
* Guruprasad Ayyaswamy guruplace04@gmail.com
#### Team Lead

Guruprasad Ayyaswamy guruplace04@gmail.com

#### Development

The following are the major components developed part of the final capstone project
by following the class walkthrough:
1. **Waypoint updater(Partial)**:

    In this section we subscribed to `/base_waypoints`, `/current_pose` get the list of waypoints and the current vehicle position to determine the waypoints ahead of the vehicle.
    The computed ahead waypoints are published to `/final_waypoints`. One limitation observed using VM during this step
    is no of `LOOKAHEAD_WPS` need to be 50 or less to accommodate the delay in communication between simulator and VM.
    
    Refer `ros/src/waypoint_updater/waypoint_updater.py` for details. 
1. **Drive By Wire (DBW Node)**:
    
    This node of the project accomplishes the computation of throttle, break and steering command to be issued to
    the vehicle. The controllers provided part of the Yaw Controller, PID and low pass filter is used by following
    the walkthrough. The following subscribed messages `/current_velocity`, `/vehicle/dbw_enabled` and `/twist_command`
    are used in this node. The `/twist_cmd` is subscribed to read linear and angular velocity by using the controllers
    these values `throttle`, `break` and `steering` are computed. These computed values are published using `./publish`
    of the topic commands `/vehicle/steering_cmd`, `/vehicle/throttle_cmd` and `/vehicle/break_cmd`respectively.
    
    Refer the following code for details:
    ```python
    /ros/src/twist_controller/dbw_node.py
    /ros/src/twist_controller/pid.py
    /ros/src/twist_controller/twist_controller.py
    /ros/src/twist_controller/yaw_contoller.py
 
    ```
1. **Traffic Light Classification and Detection**
    The major part of our effort for this project is on detecting the traffic lights using tensforflow. The approach taken is
    similar to the step by step approach discussed in [Object Detection Part 1 ](https://medium.com/@WuStangDan/step-by-step-tensorflow-object-detection-api-tutorial-part-1-selecting-a-model-a02b6aabe39e).
    
    **Data Collection and Pre-processing**
    
    We decided to use [Bosch Traffic Data](https://hci.iwr.uni-heidelberg.de/node/6132) as it had comprehensive traffic 
    light dataset of size ~ *6G* images to train the model. Also the traffic light images had the necessary classification
    of 14 different labels including **Red, Yellow and Green** which are required for this project defined in YAML format.
    Refer `./BoschTlDataSet/train.yaml` for details about the metadata. This dataset is then converted to **tfrecord**
    file in order to feed into tensorflow for training the model as discussed here in [Object Detection Part 2](https://medium.com/@WuStangDan/step-by-step-tensorflow-object-detection-api-tutorial-part-2-converting-dataset-to-tfrecord-47f24be9248d)
    
    The second dataset that was used to train the model is from the [Udacity drive test](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip)
    and the images are annotated using **LabelImg** as **Red, Yellow and Green** by following the steps mentioned in
    [Object detection Part 3](https://medium.com/@WuStangDan/step-by-step-tensorflow-object-detection-api-tutorial-part-3-creating-your-own-dataset-6369a4d30dfd).
    The annotated images are then converted to **trecordfile** further in order to feed into tensorflow for training.
    
    Refer the following files for details
    ```python
       ./BoschTlDataSet/*.*
       ./TlBagFile/traffic_light_bag_file/*.*
    ```
     
    **Model Training**
    
    We decided to use **Faster R-CNN** model to train and detect for both bosch and drive test traffic light images using
    tensorflow object detection API. Model is initially trained for Bosch data with following parameters:
        
     **HyperParameters:**
         
         * epochs: 50,000
         * learning rate: 0.0003

    Here are some of the detected image samples for bosch traffic light data set
   ![image1]
    
    The same model is used to train drive test traffic images [Udacity drive test](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip)
    with the following parameters
    
     **HyperParameters:**
         
         * epochs: 20,000
         * learning rate: 0.00003
     Here are some of the detected image samples for drive test traffic light data set
    ![image2]
     
    **Training Results:**
    
    ![image3]
    
    
1. **Waypoint Updater(Complete)**

    With the frozen **R-FCN** model `/CNN/fine_tuned_model/letsdoit` obtained from previous step the traffic lights
    were detected correctly. Based on the detected state **Red, Green, Yellow** target waypoints velocities are updated
    either to decelerate the vehicle stopping at **RED** or is to accelerate the vehicle gradually on detection
    of **GREEN**. The following methods provided part of the project are used to achieve gradual deceleration
    
    ```python
    get_waypoint_velocity(self, waypoint):
    set_waypoint_velocity(self, waypoints, waypoint, velocity):
    distance(self, waypoints, wp1, wp2):

    ```

    Refer `ros/src/waypoint_updater/waypoint_updater.py` for details.


Please use **one** of the two installation options, either native **or** docker installation.


### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Install `git-lfs`. The project repository contains a large file. Install `git-lfs` 
prior to cloning the project repository.
```bash
# Download deb file 
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
# Install git-lfs
$ sudo apt-get install git-lfs
```

2. Clone the project repository
```bash
git clone https://github.com/jasonhuh/CarND-Capstone
```

3. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
4. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
5. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```

3. (Optional) Launch rviz
```bash
rosrun rviz rviz
```

3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

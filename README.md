# Warning

This repository is under construction. Consinstent changes will be done soon!

# MPOSE2021 Dataset for Short-time Human Action Recognition

This repository contains the MPOSE2021 Dataset for short-time pose-based Human Action Recognition (HAR). 
MPOSE2021 is specifically designed to perform short-time Human Action Recognition.

MPOSE2021 is developed as an evolution of the MPOSE Dataset [1-3]. It is made by human pose data detected by 
[OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) [4] (and [Posenet](https://github.com/tensorflow/tfjs-models/tree/master/posenet), coming soon!) 
on popular datasets for HAR, i.e. Weizmann [5], i3DPost [6], IXMAS [7], KTH [8], UTKinetic-Action3D (RGB only) [9] and UTD-MHAD (RGB only) [10], alongside original video datasets, i.e. ISLD and ISLD-Additional-Sequences [1].
Since these datasets had heterogenous action labels, each dataset labels were remapped to a common and homogeneous list of actions.
Overall, MPOSE2021 contains 15428 samples, divided into 20 actions, performed by 100 subjects.

This repository allows users to generate RGB+POSE data for MPOSE2021 in a python-friendly format. 
Generated RGB+POSE sequences have a number of frames between 20 and 30. 
Sequences are obtained cutting Precursor VIDEOS, belonging to the above-mentioned datasets, 
with non-overlapping sliding windows.
RGB data contains the target ROI obtained from POSE sequences. 

The overview of the processing to generate MPOSE2021 is the following:
![alt text](https://github.com/FedericoAngelini/MPOSE2021_Dataset/blob/master/docs/pipeline.png?raw=true)

1A. allows the user to generate precurso VIDEO data. For licence-related reasons, the user must download the Former Datasets Archives from the original sources,
as explanined in the following documentation. Former datasets archives must be downloaded in order to encode the precursor VIDEO data. 
Therefore, precursor VIDEO data are processed via OpenPose, and the output (JSON files) is stored.

2A. allows the user to generate RGB+POSE data for MPOSE2021. On the basis of JSON files (provided to the user for convenience), 
  RGB and POSE data for MPOSE2021 are generated. Therefore, a post-processing step is needed to discard/amend defective sequences.

B. allows the user to generate POSE data only, ignoring RGB data.

Below, the instructions to perform 1A., 2A. or B. are explained.

The overview of the action composition of MPOSE2021 is provided [here](https://github.com/FedericoAngelini/MPOSE2021_Dataset/blob/master/docs/mpose2021_summary.pdf?raw=true).


## Citations
MPOSE2021 is intended for scientific research purposes.
The user that wants to use MPOSE2021 for publications, please cite [1-10].

## Requirements
The following requirements are needed to generate RGB data for MPOSE2021 (tested on Ubuntu 20.04).
* around 380 GB free disk space (for storing archives, temporary files);
* around 8 GB free disk space (for storing generated MPOSE2021 RGB data):
* Python 3.8;

## 1A. Generate precursor VIDEO data
The following procedure initialise the dataset variables and generates video data starting from the above-mentioned datasets. Generated video sequences are consistently named according to MPOSE2021 format and are used as precursor of subsequent processing steps.

1. Clone the repository.

2. (Optional, but recommented) Create virtual environment.
    * Create virtual environment following commands for your distribution;
    * Make sure to use Python 3.8. Previous versions are not tested.
    * Activate virtual environment.

3. Download RGB archives from the following third-party repositories:
    * [IXMAS Dataset](https://www.epfl.ch/labs/cvlab/data/data-ixmas10).
        * Download "original IXMAS ROIs" archive;
        * Save the archive into "archives_path"/ixmas/.
    * [Weizmann Dataset](http://www.wisdom.weizmann.ac.il/~vision/SpaceTimeActions.html).
        * Download actions: Walk, Run, Jump, Bend, One-hand wave, Two-hands wave, Jump in place;
        * Save the archive into "archives_path"/weizmann/.
    * [i3DPost Dataset](http://kahlan.eps.surrey.ac.uk/i3dpost_action/) (subject to password request!).
        * Download all archives related to actions: Walk, Run, Jump, Bend, Hand-wave, Jump in place;
        * Save the archive into "archives_path"/i3DPost/.
    * [KTH Dataset](https://www.csc.kth.se/cvap/actions/).
        * Download archives "walking.zip", "jogging.zip", "running.zip", "boxing.zip", "handwaving.zip", "handclapping.zip";
        * Save the archive into "archives_path"/kth/.
    * [ISLD Dataset](https://doi.org/10.25405/data.ncl.14061806.v1)
        * Download archive;
        * Save the archive into "archives_path"/isld/.
    * [ISLD-Additional-Sequences Dataset](https://drive.google.com/file/d/1L1AvAP56fUwHQO6QvRGuYxfAHllw5PLe/view?usp=sharing)
        * Download archive;
        * Save the archive into "archives_path"/isldas/.
    * [UTKinect-Action3D Dataset](http://cvrc.ece.utexas.edu/KinectDatasets/HOJ3D.html)
        * Download archive (RGB images only);
        * Save the archive into "archives_path"/utkinect/.
    * [UTD-MHAD Dataset](https://personal.utdallas.edu/~kehtar/UTD-MHAD.html)
        * Downlad archive (RGB images only);
        * Save the archive into "archives_path"/utdmhad/  

4. Install python requirements:
    * `pip3 install -r requirements.txt`

5. Check and setup variables in "init_vars.py":
    * "dataset_path": where you want the dataset to be exported;
    * "archives_path": where you want to save the former dataset archives (see below point 5.);
    * "temporary_path": where temporary files will be stored (see below point 7.);

6. Run variables initialization
    * `python init_vars.py`

7. Extract archives:
    * `python extract_formers.py`
    *  Archives are extracted into the "temporary_path" folder.
  
8. Create precursor VIDEO data:
    * `python create_video.py`
    * VIDEO data for generating MPOSE2021 are located in "dataset_path"/video.
    
9. (Optional) Check integrity of VIDEO data (to make sure that the json files in "archives_path"/json are compatible, see "Generate POSE data" instructions below, point 2.):
    * `python check_integrity.py video`
    * You should get the following message: "Test against misc/cksum_video.csv passed!";

## 2A. Generate RGB+POSE data
The following procedure generates MPOSE2021 sequences (RGB + POSE). Each sequence will have a variable number of frames f, such that "min_frame_length" <= f <= "max_frame_length" (default: 20 <= f <= 30).

1. Download detected poses (by OpenPose) as JSON files:
    * Download [json](https://drive.google.com/file/d/1gmq5q4Ck5VVDVn1HZuiXXmPkFbF0GldF/view?usp=sharing) obtained by using [OpenPose v1.6.0](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases) portable demo for Windows running on MPOSE2021 precursor VIDEO data;
    * Save the archive into "archives_path"/json/.
   
2. Extract json data:
    * `python extract_json.py`
    * The archive is extracted into the "dataset_path"/json folder.
    
3. Generate RGB+POSE data:
    * `python create_rgb_pose.py`
    * RGB data is stored into "dataset_path"/rgb folder;
    * POSE data is stored into "dataset_path"/pose folder.
   
4. Refine generated RGB+POSE data:
    * `python refine_dataset.py`
    * Refined RGB data is stored into "dataset_path"/rgb folder;
    * Refined POSE data is stored into"dataset_path"/pose folder.

NOTE: This procedure applies the following transformations: 1) remove samples such that the RGB encoding failed due to corrupted data; 2) renaming "outliers", i.e. sequences that, due to the above processing, do not contain the target action anymore; 3) remove sequences judjed to be non-sense. The script `find_outliers.py` was used to manually scan RGB files and find which sequence should have been considered an outlier. The results of this search are located into 'misc/refine_dataset/'.

5. (Optional) Check integrity of RGB+POSE data (to make sure that generated sequences are in compliance with MPOSE2021 official sequences):
    * `python check_integrity.py rgb_pose`
    * You should get the following message: "Test against misc/cksum_rgb.csv passed!";
    * You should get the following message: "Test against misc/cksum_pose.csv passed!".

6. Generate meta data containing the 3 default splits list.
    * `python create_splits.py`
    * Splits files are stored into "dataset_path" folder.
   
7. Generate dataset summary figures:
    * `python export_figures.py`
    * Figures are stored into "dataset_path"/figures folder.

## B. Generate POSE data only

Coming soon.

# References
[1] F. Angelini, Z. Fu, Y. Long, L. Shao and S. M. Naqvi, "2D Pose-based Real-time Human Action Recognition with Occlusion-handling," in IEEE Transactions on Multimedia. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8853267&isnumber=4456689

[2] F. Angelini, J. Yan and S. M. Naqvi, "Privacy-preserving Online Human Behaviour Anomaly Detection Based on Body Movements and Objects Positions," ICASSP 2019 - 2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Brighton, United Kingdom, 2019, pp. 8444-8448. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8683026&isnumber=8682151

[3] F. Angelini and S. M. Naqvi, "Joint RGB-Pose Based Human Action Recognition for Anomaly Detection Applications," 2019 22th International Conference on Information Fusion (FUSION), Ottawa, ON, Canada, 2019, pp. 1-7. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9011277&isnumber=9011156

[4] Cao, Zhe, et al. "OpenPose: realtime multi-person 2D pose estimation using Part Affinity Fields." IEEE transactions on pattern analysis and machine intelligence 43.1 (2019): 172-186.

[5] Gorelick, Lena, et al. "Actions as space-time shapes." IEEE transactions on pattern analysis and machine intelligence 29.12 (2007): 2247-2253.

[6] Starck, Jonathan, and Adrian Hilton. "Surface capture for performance-based animation." IEEE computer graphics and applications 27.3 (2007): 21-31.

[7] Weinland, Daniel, Mustafa Özuysal, and Pascal Fua. "Making action recognition robust to occlusions and viewpoint changes." European Conference on Computer Vision. Springer, Berlin, Heidelberg, 2010.

[8] Schuldt, Christian, Ivan Laptev, and Barbara Caputo. "Recognizing human actions: a local SVM approach." Proceedings of the 17th International Conference on Pattern Recognition, ICPR 2004. Vol. 3. IEEE, 2004.

[9] L. Xia, C.C. Chen and JK Aggarwal. "View invariant human action recognition using histograms of 3D joints", 2012 IEEE Computer Society Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 20-27, 2012.

[10] C. Chen, R. Jafari, and N. Kehtarnavaz. "UTD-MHAD: A Multimodal Dataset for Human Action Recognition Utilizing a Depth Camera and a Wearable Inertial Sensor". Proceedings of IEEE International Conference on Image Processing, Canada, 2015. 

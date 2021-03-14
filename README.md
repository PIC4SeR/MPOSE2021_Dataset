# Warning

This repository is under construction. Consinstent changes will be done soon!

# MPOSE2021 Dataset for Short-time Human Action Recognition

This repository contains the MPOSE2021 Dataset for short-time pose-based Human Action Recognition (HAR). 

MPOSE2021 is developed as an evolution of the MPOSE Dataset [1-3]. It is made by human pose data detected by 
[OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) [4] (and [Posenet](https://github.com/tensorflow/tfjs-models/tree/master/posenet), coming soon!) 
on popular datasets for HAR, i.e. Weizmann [5], i3DPost [6], IXMAS [7], and KTH [8] alongside original video datasets, i.e. ISLD and ISLD-Additional-Sequences [1]. 
Since these datasets had heterogenous action labels, each dataset labels were remapped to a common and homogeneous list of actions.

This repository allows users to generate RGB+POSE data for MPOSE2021 in a python-friendly format. The pipeline is the following:

FORMER DATASETS ARCHIVES --> Precursor VIDEO Data --> OpenPose --> RGB+POSE
                                                  
Precursor VIDEO data for MPOSE2021 are generated from the former datasets archives. Therefore, precursor VIDEO data are processed via OpenPose, and the output (JSON files) is stored. In this repository, generated JSON files are provided, to allow the users to skip the time consuming OpenPose step, and to provide a fair benchmark platform for methods comparison. On the basis of JSON files, RGB and POSE data for MPOSE2021 are generated.

For licence-related reasons, the user must download the FORMER DATASETS ARCHIVES from the original sources, as explanined in the following documentation.

MPOSE2021 is specifically designed to perform short-time Human Action Recognition. RGB+POSE sequences have a number of frames between 20 and 30. Sequences are obtained cutting the precursor videos with non-overlapping sliding windows. RGB data contains the target ROI obtained from POSE sequences. 

## Requirements
The following requirements are needed to generate RGB data for MPOSE2021 (tested on Ubuntu 20.04).
* around 380 GB free disk space (for storing archives, temporary files);
* around 8 GB free disk space (for storing generated MPOSE2021 RGB data):
* Python 3.8;

## 1. Generate precursor VIDEO data
The following procedure initialise the dataset variables and generates video data starting from the above-mentioned datasets. Generated video sequences are consistently named according to MPOSE2021 format and are used as precursor of subsequent processing steps.

1. Clone the repository.

2. Create virtual environment (optional, but recommended).
    * Create virtual environment following commands for your distribution;
    * Make sure to use Python 3.8. Previous versions are not tested.
    * Activate virtual environment.

3. Check and setup variables in "init_vars.py":
    * "dataset_path": where you want the dataset to be exported;
    * "archives_path": where you want to save the former dataset archives (see below point 5.);
    * "temporary_path": where temporary files will be stored (see below point 7.);
    * "max_frame_length": maximum frame length of each MPOSE2021 sequence (default 30, don't change for reproducibility);
    * "min_frame_length": minimum frame length for a sequence of poses to be accepted (default 20, don't change for reproducibility).

4. Run variables initialization
    * `python init_vars.py`

5. Download RGB archives from the following third-party repositories:
    * [IXMAS Dataset](https://www.epfl.ch/labs/cvlab/data/data-ixmas10).
        * Download "original IXMAS ROIs" archive;
        * Save the archive into "arhives_path"/ixmas/.
    * [Weizmann Dataset](http://www.wisdom.weizmann.ac.il/~vision/SpaceTimeActions.html).
        * Download actions: Walk, Run, Jump, Bend, One-hand wave, Two-hands wave, Jump in place;
        * Save the archive into "arhives_path"/weizmann/.
    * [i3DPost Dataset](http://kahlan.eps.surrey.ac.uk/i3dpost_action/) (subject to password request!).
        * Download all archives related to actions: Walk, Run, Jump, Bend, Hand-wave, Jump in place;
        * Save the archive into "arhives_path"/i3DPost/.
    * [KTH Dataset](https://www.csc.kth.se/cvap/actions/).
        * Download archives "walking.zip", "jogging.zip", "running.zip", "boxing.zip", "handwaving.zip", "handclapping.zip";
        * Save the archive into "arhives_path"/kth/.
    * [ISLD Dataset](https://doi.org/10.25405/data.ncl.14061806.v1)
        * Download archive;
        * Save the archive into "arhives_path"/isld/.
    * [ISLD-Additional-Sequences Dataset](https://drive.google.com/file/d/1L1AvAP56fUwHQO6QvRGuYxfAHllw5PLe/view?usp=sharing)
        * Download archive;
        * Save the archive into "arhives_path"/isldas/.

6. Install python requirements:
    * `pip3 install -r requirements.txt`

7. Extract archives:
    * `python extract_formers.py`
    *  Archives are extracted into the "temporary_path" folder.
  
8. Create RGB data:
    * `python create_video.py`
    * RGB data for MPOSE2021 are located in "dataset_path"/video.
    
9. Check integrity of RGB data (to make sure that the json files in "archives_path"/json are compatible, see "Generate POSE data" instructions below, point 2.):
    * `python check_integrity.py`

## 2. Generate RGB and POSE data
The following procedure generates MPOSE2021 sequences (RGB + POSE). Each sequence will have a variable number of frames f, such that "min_frame_length" <= f <= "max_frame_length" (default: 20 <= f <= 30).

1. Download detected data:
    * Download [json](https://drive.google.com/file/d/1wgkgN6dPcHL7-zZsAj73CUgZm5GJamYT/view?usp=sharing) obtained by using [OpenPose v1.6.0](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases) portable demo for Windows running on MPOSE2021 precursor VIDEO data;
    * Save the archive into "arhives_path"/json/.
   
2. Extract json data:
    * `python extract_json.py`
    * The archive is extracted into the "dataset_path"/json folder.
    
3. Generate RGB+POSE data:
    * `python create_rgb_pose.py`
    * RGB data is available in the "dataset_path"/rgb folder;
    * POSE data is available in the "dataset_path"/pose folder.

## 3. Refine RGB and POSE data and finalise dataset
1. Refine generated RGB and POSE:
    * `python refine_dataset.py`

NOTE: This procedure applies the following transformations:
    - remove samples such that the RGB encoding failed due to corrupted data;
    - renaming "outliers", i.e. sequences that, due to the above processing, do not contain the target action anymore;
    - remove sequences judjed to be non-sense;
    - convert "pick-up" action labels to "bend" action labels (due to their strong similarity);
    - convert "turn" action labels to "walk" action labels (due to their strong similarity); 

2. Generate dataset meta and summary figures:
    * `python generate_meta_and_figures.py`

# References
[1] F. Angelini, Z. Fu, Y. Long, L. Shao and S. M. Naqvi, "2D Pose-based Real-time Human Action Recognition with Occlusion-handling," in IEEE Transactions on Multimedia. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8853267&isnumber=4456689

[2] F. Angelini, J. Yan and S. M. Naqvi, "Privacy-preserving Online Human Behaviour Anomaly Detection Based on Body Movements and Objects Positions," ICASSP 2019 - 2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Brighton, United Kingdom, 2019, pp. 8444-8448. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8683026&isnumber=8682151

[3] F. Angelini and S. M. Naqvi, "Joint RGB-Pose Based Human Action Recognition for Anomaly Detection Applications," 2019 22th International Conference on Information Fusion (FUSION), Ottawa, ON, Canada, 2019, pp. 1-7. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9011277&isnumber=9011156

[4] Cao, Zhe, et al. "OpenPose: realtime multi-person 2D pose estimation using Part Affinity Fields." IEEE transactions on pattern analysis and machine intelligence 43.1 (2019): 172-186.

[5] Gorelick, Lena, et al. "Actions as space-time shapes." IEEE transactions on pattern analysis and machine intelligence 29.12 (2007): 2247-2253.

[6] Starck, Jonathan, and Adrian Hilton. "Surface capture for performance-based animation." IEEE computer graphics and applications 27.3 (2007): 21-31.

[7] Weinland, Daniel, Mustafa Özuysal, and Pascal Fua. "Making action recognition robust to occlusions and viewpoint changes." European Conference on Computer Vision. Springer, Berlin, Heidelberg, 2010.

[8] Schuldt, Christian, Ivan Laptev, and Barbara Caputo. "Recognizing human actions: a local SVM approach." Proceedings of the 17th International Conference on Pattern Recognition, 2004. ICPR 2004.. Vol. 3. IEEE, 2004.

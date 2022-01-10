[![arXiv](http://img.shields.io/badge/arXiv-2001.09136-B31B1B.svg)](https://arxiv.org/abs/2107.00606)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
<h1 align="center">  MPOSE2021 <br> A Dataset for Short-Time Human Action Recognition
</h1>


This repository contains the MPOSE2021 Dataset for short-time Human Action Recognition (HAR). 

MPOSE2021 is developed as an evolution of the MPOSE Dataset [1-3]. It is made by human pose data detected by 
[OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) [4] and [Posenet](https://github.com/google-coral/project-posenet/tree/master/models) [11]
on popular datasets for HAR, i.e. Weizmann [5], i3DPost [6], IXMAS [7], KTH [8], UTKinetic-Action3D (RGB only) [9] and UTD-MHAD (RGB only) [10], alongside original video datasets, i.e. ISLD and ISLD-Additional-Sequences [1].
Since these datasets had heterogenous action labels, each dataset labels were remapped to a common and homogeneous list of 20 actions.

This repository allows users to directly access the POSE dataset (Section A.) or generate RGB and POSE data for MPOSE2021 in a python-friendly format (Section B.). 
Generated RGB and POSE sequences have a number of frames between 20 and 30. 
Sequences are obtained by cutting the so-called "precursor videos" (videos from the above-mentioned datasets), with non-overlapping sliding windows.
Frames where OpenPose/PoseNet cannot detect any subject are automatically discarded. Resulting samples contain one subject at the time, performing a fraction of a single action. 

Overall, MPOSE2021 contains 15429 samples, divided into 20 actions performed by 100 subjects. 
The overview of the action composition of MPOSE2021 is provided in the following image:
<p align="center">
  <img src="https://raw.githubusercontent.com/PIC4SeRCentre/MPOSE2021_Dataset/master/docs/mpose2021_summary.png" alt="MPOSE2021 Summary" width="600">
</p>

## A. Access POSE Data Only
To get only MPOSE2021 POSE data, install our light and simple [pip package](https://pypi.org/project/mpose/)

```
pip install mpose
```

And use the MPOSE class to download, extract, and process POSE data (Openpose/PoseNet).

```
# import package
import mpose

# initialize and download data
dataset = mpose.MPOSE(pose_extractor='openpose', 
                      split=1, 
                      transform='scale_and_center', 
                      data_dir='./data/')

# print data info 
dataset.get_info()

# get data samples (as numpy arrays)
X_train, y_train, X_test, y_test = dataset.get_dataset()
```

Check out the package documentation and [this Colab Notebook Tutorial](https://colab.research.google.com/drive/1_v3DYwgZPMCiELtgiwMRYxQzcYGdSWFH?usp=sharing) for more hands-on examples <a href="https://colab.research.google.com/drive/1_v3DYwgZPMCiELtgiwMRYxQzcYGdSWFH?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>. The source code can be found in the [mpose_api](https://github.com/PIC4SeRCentre/MPOSE2021/edit/master/mpose_api/) subfolder.

## B. Generate RGB and POSE Data
### Requirements
&nbsp;&nbsp;&nbsp;  The following requirements are needed to generate RGB data for MPOSE2021 (tested on Ubuntu):
  * around 340 GB free disk space (330 GB for archives and temporary files, 10 GB for VIDEO, RGB and POSE data)
  * Python 3.6+


You can get both RGB and the corresponding POSE data running a simple python script.
For licence-related reasons, the user must manually download precursor dataset archives from the original sources, as explanined in the following steps.

1. Clone this repository.

2. Create a virtual environment (optional, but recommended).

3. Download RGB archives from the following third-party repositories:
    * [IXMAS Dataset](https://www.epfl.ch/labs/cvlab/data/data-ixmas10)
        * Download "original IXMAS ROIs" archive
        * Save the archive into "archives_path"/ixmas/
    * [Weizmann Dataset](http://www.wisdom.weizmann.ac.il/~vision/SpaceTimeActions.html)
        * Download actions: Walk, Run, Jump, Bend, One-hand wave, Two-hands wave, Jump in place
        * Save the archives into "archives_path"/weizmann/
    * [i3DPost Dataset](http://kahlan.eps.surrey.ac.uk/i3dpost_action/)
        * Request ID and Password to the authors
        * Download all archives related to actions: Walk, Run, Jump, Bend, Hand-wave, Jump in place
        * Save the archives into "archives_path"/i3DPost/
    * [KTH Dataset](https://www.csc.kth.se/cvap/actions/)
        * Download archives "walking.zip", "jogging.zip", "running.zip", "boxing.zip", "handwaving.zip", "handclapping.zip"
        * Save the archives into "archives_path"/kth/
    * [ISLD Dataset](https://doi.org/10.25405/data.ncl.14061806.v1)
        * Download archive
        * Save the archive into "archives_path"/isld/
    * [ISLD-Additional-Sequences Dataset](https://drive.google.com/file/d/1L1AvAP56fUwHQO6QvRGuYxfAHllw5PLe/view?usp=sharing)
        * Download archive
        * Save the archive into "archives_path"/isldas/
    * [UTKinect-Action3D Dataset](http://cvrc.ece.utexas.edu/KinectDatasets/HOJ3D.html)
        * Download archive (RGB images only)
        * Save the archive into "archives_path"/utkinect/
    * [UTD-MHAD Dataset](https://personal.utdallas.edu/~kehtar/UTD-MHAD.html)
        * Downlad archive (RGB images only)
        * Save the archive into "archives_path"/utdmhad/  

4. Download POSE archives:
    * [OpenPose](https://www.dropbox.com/s/pdel0462lfuqxfr/json.zip) (obtained by using [OpenPose v1.6.0](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases) portable demo for Windows to process MPOSE2021 precursor VIDEO data)
        * Download "json.zip" archive
        * Save the archive into "archives_path"/json/
    * [PoseNet](https://www.dropbox.com/s/sk0z66hemzyq2ze/posenet.zip) (obtained by using [PoseNet ResNet-50 (288x416x3)](https://coral.ai/models/pose-estimation/) running on a Coral accelerator to process MPOSE2021 precursor VIDEO data)
        * Download "posenet.zip" archive
        * Save the archive into "archives_path"/posenet/
        
5. Install python requirements:
    * `pip install -r requirements.txt`

6. Setup variables in "init_vars.py":
    * "dataset_path": where you want the dataset to be exported
    * "data_path": where you want to store all the data (leave as default)

7. Run dataset extraction and processing:
    * `python main.py`
    * Arguments:
      * `--mode` `-m`: operation to perform
        * `init`: initialize folders, files and variables
        * `extract`: init + extract archives and prepare them for dataset generation
        * `generate`: extract + generate RGB and POSE data (+ 3 different .csv files for train/test splitting)
        * `check`: init + check data integrity and generate summary figures
      * `--pose` `-p`: pose detector
        * `openpose`: OpenPose
        * `all`: OpenPose + PoseNet
      * `--force` `-f`: force the execution of unnecessary operations
      * `--verbose` `-v`: print more information


## Citations
MPOSE2021 is intended for scientific research purposes.
If you want to use MPOSE2021 for publications, please cite our work ([Action Transformer: A Self-Attention Model for Short-Time Pose-Based Human Action Recognition](https://arxiv.org/abs/2107.00606)) as well as [1-11].

```
@article{mazzia2021action,
  title={Action Transformer: A Self-Attention Model for Short-Time Pose-Based Human Action Recognition},
  author={Mazzia, Vittorio and Angarano, Simone and Salvetti, Francesco and Angelini, Federico and Chiaberge, Marcello},
  journal={Pattern Recognition},
  pages={108487},
  year={2021},
  publisher={Elsevier}
}
```

# References
[1] Angelini, F., Fu, Z., Long, Y., Shao, L., & Naqvi, S. M. (2019). 2D Pose-Based Real-Time Human Action Recognition With Occlusion-Handling. IEEE Transactions on Multimedia, 22(6), 1433-1446.

[2] Angelini, F., Yan, J., & Naqvi, S. M. (2019, May). Privacy-preserving Online Human Behaviour Anomaly Detection Based on Body Movements and Objects Positions. In ICASSP 2019-2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 8444-8448). IEEE.

[3] Angelini, F., & Naqvi, S. M. (2019, July). Joint RGB-Pose Based Human Action Recognition for Anomaly Detection Applications. In 2019 22th International Conference on Information Fusion (FUSION) (pp. 1-7). IEEE.

[4] Cao, Z., Hidalgo, G., Simon, T., Wei, S. E., & Sheikh, Y. (2019). OpenPose: Realtime Multi-Person 2D Pose Estimation Using Part Affinity Fields. IEEE transactions on pattern analysis and machine intelligence, 43(1), 172-186.

[5] Gorelick, L., Blank, M., Shechtman, E., Irani, M., & Basri, R. (2007). Actions as Space-Time Shapes. IEEE transactions on pattern analysis and machine intelligence, 29(12), 2247-2253.

[6] Starck, J., & Hilton, A. (2007). Surface Capture for Performance-Based Animation. IEEE computer graphics and applications, 27(3), 21-31.

[7] Weinland, D., Özuysal, M., & Fua, P. (2010, September). Making Action Recognition Robust to Occlusions and Viewpoint Changes. In European Conference on Computer Vision (pp. 635-648). Springer, Berlin, Heidelberg.

[8] Schuldt, C., Laptev, I., & Caputo, B. (2004, August). Recognizing Human Actions: a Local SVM Approach. In Proceedings of the 17th International Conference on Pattern Recognition, 2004. ICPR 2004. (Vol. 3, pp. 32-36). IEEE.

[9] Xia, L., Chen, C. C., & Aggarwal, J. K. (2012, June). View Invariant Human Action Recognition using Histograms of 3D Joints. In 2012 IEEE computer society conference on computer vision and pattern recognition workshops (pp. 20-27). IEEE.

[10] Chen, C., Jafari, R., & Kehtarnavaz, N. (2015, September). UTD-MHAD: A Multimodal Dataset for Human Action Recognition utilizing a Depth Camera and a Wearable Inertial Sensor. In 2015 IEEE International conference on image processing (ICIP) (pp. 168-172). IEEE.

[11] Papandreou, G., Zhu, T., Chen, L. C., Gidaris, S., Tompson, J., & Murphy, K. (2018). Personlab: Person Pose Estimation and Instance Segmentation with a Bottom-Up, Part-Based, Geometric Embedding Model. In Proceedings of the European Conference on Computer Vision (ECCV) (pp. 269-286).

[12] Mazzia, V., Angarano, S., Salvetti, F., Angelini, F., & Chiaberge, M. (2021). Action Transformer: A Self-Attention Model for Short-Time Pose-Based Human Action Recognition. Pattern Recognition, 108487.

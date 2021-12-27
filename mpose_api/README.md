# MPOSE2021
#### A Dataset for Short-time Pose-based Human Action Recognition

This repository contains the MPOSE2021 Dataset for short-time pose-based Human Action Recognition (HAR). 
MPOSE2021 is specifically designed to perform short-time Human Action Recognition.

MPOSE2021 is developed as an evolution of the MPOSE Dataset [1-3]. It is made by human pose data detected by 
[OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) [4] and [Posenet](https://github.com/tensorflow/tfjs-models/tree/master/posenet) [11] on popular datasets for HAR, i.e. Weizmann [5], i3DPost [6], IXMAS [7], KTH [8], UTKinetic-Action3D (RGB only) [9] and UTD-MHAD (RGB only) [10], alongside original video datasets, i.e. ISLD and ISLD-Additional-Sequences [1].
Since these datasets have heterogenous action labels, each dataset labels are remapped to a common and homogeneous list of actions.

This repository allows users to generate pose data for MPOSE2021 in a python-friendly format. 
Generated sequences have a number of frames between 20 and 30. 
Sequences are obtained by cutting the so-called Precursor videos (from the above-mentioned datasets), with non-overlapping sliding windows.
Frames where OpenPose/PoseNet cannot detect any subject are automatically discarded. Resulting samples contain one subject at a time, performing a fraction of a single action. Overall, MPOSE2021 contains 15429 samples, divided into 20 actions, performed by 100 subjects. 

The overview of the action composition of MPOSE2021 is provided in the following image:

<p align="center">
  <img src="https://raw.githubusercontent.com/PIC4SeR/MPOSE2021_Dataset/master/docs/mpose2021_summary.png" alt="MPOSE2021 Summary" width="600">
</p>

Below, the steps to install the ```mpose``` library and obtain sequences are explained. Source code can be found in the [MPOSE2021 repository](https://github.com/PIC4SeRCentre/MPOSE2021_Dataset).

### Installation

Install MPOSE2021 as python package from [PyPi](https://pypi.org/project/mpose)
```
pip install mpose
```

### Getting Started

```python
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

[![asciicast](https://asciinema.org/a/4dXzjbZUoxXM6d3o0aNumGLr7.svg)](https://asciinema.org/a/4dXzjbZUoxXM6d3o0aNumGLr7)

Check out our [Colab Notebook Tutorial](https://colab.research.google.com/drive/1_v3DYwgZPMCiELtgiwMRYxQzcYGdSWFH?usp=sharing) for quick hands-on examples.

### References

MPOSE2021 is part of a [paper published by the Pattern Recognition Journal](https://authors.elsevier.com/a/1eH6s77nKcvmg) (Elsevier), and is intended for scientific research purposes.
If you want to use MPOSE2021 for your research work, please also cite [1-11].

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
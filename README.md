# MPOSE2021 Dataset

This repository contains the MPOSE2021 Dataset for short-time pose-based Human Action Recognition (HAR). 

MPOSE2021 is developed as an evolution of the MPOSE Dataset [1-3]. It is made by human pose data detected by OpenPose [4] on popular datasets for HAR, i.e. Weizmann [5], i3DPost [6], IXMAS [7], and KTH [8] alongside original video dataset, i.e. ISLD and ISLD-Additional-Sequences [1]. Since these datasets had heterogenous action labels, each dataset labels were remapped to a common and homogeneous list of actions.

This repository contains pose data in a python-friendly format. Moreover, it also contains the scripts to generate MPOSE2021 dataset (RGB data) starting from the original RGB sequences belonging to the above-mentioned dataset. For licence-related reasons, the user must download RGB data from the original sources, as explanined in the manual.

External Repositories (no unzip!):
* [IXMAS Dataset](https://www.epfl.ch/labs/cvlab/data/data-ixmas10). Download "original IXMAS ROIs" archive.
* [Weizmann Dataset](http://www.wisdom.weizmann.ac.il/~vision/SpaceTimeActions.html). Download actions: Walk, Run, Jump, Bend, One-hand wave, Two-hands wave, Jump in place.
* [i3DPost Dataset](http://kahlan.eps.surrey.ac.uk/i3dpost_action/) (subject to password request!). Download all archives related to actions: Walk, Run, Jump, Bend, Hand-wave, Jump in place.
* [KTH Dataset](https://www.csc.kth.se/cvap/actions/). Download archives "walking.zip", "jogging.zip", "running.zip", "boxing.zip", "handwaving.zip", "handclapping.zip"
* [ISLD Dataset]()
* [ISLD-Additional-Sequences Dataset]()

# References
[1] F. Angelini, Z. Fu, Y. Long, L. Shao and S. M. Naqvi, "2D Pose-based Real-time Human Action Recognition with Occlusion-handling," in IEEE Transactions on Multimedia. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8853267&isnumber=4456689

[2] F. Angelini, J. Yan and S. M. Naqvi, "Privacy-preserving Online Human Behaviour Anomaly Detection Based on Body Movements and Objects Positions," ICASSP 2019 - 2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Brighton, United Kingdom, 2019, pp. 8444-8448. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8683026&isnumber=8682151

[3] F. Angelini and S. M. Naqvi, "Joint RGB-Pose Based Human Action Recognition for Anomaly Detection Applications," 2019 22th International Conference on Information Fusion (FUSION), Ottawa, ON, Canada, 2019, pp. 1-7. URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9011277&isnumber=9011156

import os
import cv2

# path where the dataset will be exported
dataset_path = '/home/federico/Documents/MPOSE2021/'

# paths where the formers dataset archives will be stored
# which requires ??? free space
archives_path = dataset_path + 'archives/'
## TODO: specify the space
## TODO: create scripts to free the space up

# temporary folder, which requires ??? free space
# it will contain unzipped archives
temp_path = dataset_path + 'temp/'
## TODO: specify the space

# maximum frame length for each MPOSE2021 sequence
max_frame_length = 30  # deault 30
min_frame_length = 20  # default 20

'''
########################################################################
################ do NOT modify after this point ########################
########################################################################
'''
if max_frame_length == 30 and min_frame_length == 20:
    print('MPOSE2021 with default frame_length parameters')
else:
    print('MPOSE2021 with NON-default frame_length parameters!!!')

archives_paths = dict(kth=archives_path + 'kth/',
                      ixmas=archives_path + 'ixmas/',
                      i3dpost=archives_path + 'i3dpost/',
                      weizmann=archives_path + 'weizmann/',
                      isld=archives_path + 'isld/',
                      isldas=archives_path + 'isldas/',
                      json=archives_path + 'json/')
del archives_path

former_paths = dict(kth=temp_path + 'kth/',
                    ixmas=temp_path + 'ixmas/',
                    i3dpost=temp_path + 'i3dpost/',
                    weizmann=temp_path + 'weizmann/',
                    isld=temp_path + 'isld/',
                    isldas=temp_path + 'isldas/')

paths = dict(video=dataset_path + 'video/',
             pose=dataset_path + 'pose/',
             json=dataset_path + 'json/',
             figures=dataset_path + 'figures/')

actions = {'standing': 0,
           'check-watch': 1,
           'cross-arms': 2,
           'scratch-head': 3,
           'sit-down': 4,
           'get-up': 5,
           'turn': 6,
           'walk': 7,
           'wave1': 8,
           'box': 9,
           'kick': 10,
           'point': 11,
           'pick-up': 12,
           'bend': 13,
           'hands-clap': 14,
           'wave2': 15,
           'jog': 16,
           'jump': 17,
           'pjump': 18,
           'run': 19}

fps = dict(kth=25,
           ixmas=25,
           i3dpost=25,
           weizmann=25,
           isld=25,
           isldas=19)

former_frame_size = dict(kth=(160, 120),
                         ixmas=(64, 48),
                         i3dpost=(1920, 1080),
                         weizmann=(180, 144),
                         isld=(1920, 1080),
                         isldas=(960, 600))

frame_size = dict(kth=(160, 120),
                  ixmas=(48, 64),
                  i3dpost=(480, 270),
                  weizmann=(180, 144),
                  isld=(480, 270),
                  isldas=(480, 300))
resize_interpolation = cv2.INTER_CUBIC

misc_paths = dict(kth='misc/kth_splitter.csv',
                  ixmas='misc/ixmas_exclude.csv',
                  i3dpost='misc/i3dpost_archives.csv',
                  weizmann=None,
                  isld='misc/isld_truth.xlsx',
                  isldas=None,
                  checksum='misc/cksum_mpose2021.csv')

video_extention = '.avi'
codec = cv2.VideoWriter_fourcc(*'MPEG')

# OpenPose keypoints index
openpose_parts = dict(head=[0, 15, 16, 17, 18],
                      right_foot=[11, 22, 23, 24],
                      left_foot=[14, 19, 20, 21])


if __name__ == '__main__':
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    for i in archives_paths.keys():
        if not os.path.exists(archives_paths[i]):
            os.makedirs(archives_paths[i])
    for i in paths.keys():
        if not os.path.exists(paths[i]):
            os.makedirs(paths[i])
    for i in former_paths.keys():
        if not os.path.exists(former_paths[i]):
            os.makedirs(former_paths[i])

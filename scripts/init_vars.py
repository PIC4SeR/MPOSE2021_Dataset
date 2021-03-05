import os
import cv2


dataset_path = '/home/federico/Documents/MPOSE2021/'
temp_paths = dict(kth='temp/kth/',
                  ixmas='temp/ixmas/',
                  i3dpost='temp/i3dpost/',
                  weizmann='temp/weizmann/',
                  isld='temp/isld/',
                  isldas='temp/isldas/')
max_frame_length = 30
min_frame_length = 20

'''
########################################################################
################ do NOT modify after this point ########################
########################################################################
'''

former_paths = dict(kth=dataset_path + 'former_data/kth/',
                    ixmas=dataset_path + 'former_data/ixmas/',
                    i3dpost=dataset_path + 'former_data/i3dpost/',
                    weizmann=dataset_path + 'former_data/weizmann/',
                    isld=dataset_path + 'former_data/isld/',
                    isldas=dataset_path + 'former_data/isldas/')

paths = dict(video=dataset_path + 'video/',
             pose=dataset_path + 'pose/',
             json=dataset_path + 'json/',
             former=dataset_path + 'former_data/',
             meta=dataset_path + 'meta/')

actions = ['stand',
           'check-watch',
           'cross-arms',
           'scratch-head',
           'sit-down',
           'get-up',
           'turn',
           'walk',
           'wave1',
           'box',
           'kick',
           'point',
           'pick-up',
           'throw',
           'bend',
           'hands-clap',
           'wave2',
           'jog',
           'jump',
           'pjump',
           'run']

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

gt_paths = dict(kth='misc/kth_splitter.csv',
                ixmas='misc/ixmas_exclude.csv',
                i3dpost='misc/i3dpost_archives.csv',
                weizmann=None,
                isld='misc/isld_truth.xlsx',
                isldas=None)

video_extention = '.avi'
codec = cv2.VideoWriter_fourcc(*'MPEG')

checksum_file_for_integrity_check = dataset_path + 'meta/cksum_mpose2021.csv'

# json related vars
min_conf_threshold = 0.2

if __name__ == '__main__':
    for i in temp_paths.keys():
        if not os.path.exists(temp_paths[i]):
            os.mkdir(temp_paths[i])
    for i in paths.keys():
        if not os.path.exists(paths[i]):
            os.mkdir(paths[i])
    for i in former_paths.keys():
        if not os.path.exists(former_paths[i]):
            os.mkdir(former_paths[i])
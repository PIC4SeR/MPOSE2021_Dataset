from init_vars import *
import os
import cv2
import pandas as pd


def process_former_dataset(dataset):
    if dataset == 'weizmann':
        print('WEIZMANN DATASET PRE-PROCESSING:')
        samples = [f for f in os.listdir(former_paths[dataset]) if os.path.isfile(os.path.join(former_paths[dataset], f))]
        unique_id = 0
        for i in samples:
            action = i[i.find('_')+1:i.find('.')]
            actor = i[:i.find('_')]
            if action in ['bend', 'jump', 'pjump', 'run', 'walk', 'wave1', 'wave2']:
                new_name = '{}_{}_{}'.format(dataset, actor, action)
                print('\tSplitting: {}'.format(i))
                # split former video
                vidcap = cv2.VideoCapture(former_paths[dataset] + i)
                success, image = vidcap.read()
                frame_num = 0
                out = cv2.VideoWriter('{}{}_{}{}'.format(paths['video'], new_name, unique_id, video_extention),
                                      codec,
                                      fps[dataset],
                                      frame_size[dataset])
                while success:
                    if frame_num % max_frame_length == 0 and frame_num != 0:
                        out.release()
                        unique_id += 1
                        frame_num = 0
                        out = cv2.VideoWriter('{}{}_{}{}'.format(paths['video'], new_name, unique_id, video_extention),
                                              codec,
                                              fps[dataset],
                                              frame_size[dataset])
                    elif frame_num % max_frame_length < max_frame_length:
                        out.write(cv2.resize(image, frame_size[dataset]))
                    success, image = vidcap.read()
                    frame_num += 1
                out.release()
                vidcap.release()
    
    elif dataset == 'isldas':
        print('{} pre-processing:'.format(dataset))
        samples = [f for f in os.listdir(former_paths[dataset]) if os.path.isfile(os.path.join(former_paths[dataset], f))]
        for unique_id, file in enumerate(samples):
            res = [j for j in range(len(file)) if file.startswith('_', j)]
            actor = file[res[0]+1:res[1]]
            action = file[res[1]+1:res[2]]
            if action == '7':
                action = 'walk'
            elif action == '8':
                action = 'wave1'
            elif action == '9':
                action = 'box'
            elif action == '10':
                action = 'kick'
            elif action == '11':
                action = 'point'
            elif action == '15':
                action = 'bend'
            elif action == '16':
                action = 'hands-clap'
            elif action == '17':
                action = 'wave2'
            elif action == '21':
                action = 'run'
            else:
                continue
            new_name = '{}_{}_{}_{}{}'.format(dataset, actor, action, unique_id, video_extention)
            print('\tCopying: {}'.format('{}{}'.format(former_paths[dataset], file)))
            video = cv2.VideoCapture('{}{}'.format(former_paths[dataset], file))
            out = cv2.VideoWriter('{}{}'.format(paths['video'], new_name), codec, fps[dataset], frame_size[dataset])
            while True:
                success, frame = video.read()
                if success:
                    out.write(cv2.resize(frame, frame_size[dataset], fx=0, fy=0, interpolation=resize_interpolation))
                else:
                    break
            video.release()
            out.release()

    elif dataset == 'isld':
        print('{} pre-processing:'.format(dataset))
        samples = [f for f in os.listdir(former_paths[dataset]) if os.path.isfile(os.path.join(former_paths[dataset], f))]
        unique_id = 0
        for i in samples:
            print('\tSplitting: {}'.format(i))
            actor = i[:i.find('_')]
            gt = pd.read_excel(gt_paths[dataset], sheet_name=actor, header=1, usecols='A:F')
            gt = gt.sort_values(by='start')
            vidcap = cv2.VideoCapture(former_paths[dataset] + i)
            success, image = vidcap.read()
            frame_num = 1
            count = 0
            index = gt.index[count]
            start = gt.loc[index, 'start']
            while success:
                if frame_num >= start+max_frame_length:
                    out.release()
                    start = frame_num
                if frame_num == start:
                    if gt.loc[index, 'Action'] == 'checkwatch':
                        action = 'check-watch'
                    elif gt.loc[index, 'Action'] == 'scratchhead':
                        action = 'scratch-head'
                    elif gt.loc[index, 'Action'] == 'crossarms':
                        action = 'cross-arms'
                    elif gt.loc[index, 'Action'] == 'hclap':
                        action = 'hands-clap'
                    elif gt.loc[index, 'Action'] == 'hwav2':
                        action = 'wave2'
                    elif gt.loc[index, 'Action'] == 'hwav1':
                        action = 'wave1'
                    elif gt.loc[index, 'Action'] == 'sitdown':
                        action = 'sit-down'
                    elif gt.loc[index, 'Action'] == 'getup':
                        action = 'get-up'
                    elif gt.loc[index, 'Action'] == 'nothing':
                        action = 'standing'
                    else:
                        action = gt.loc[index, 'Action']
                    new_name = '{}_{}_{}'.format(dataset, actor.lower(), action)
                    unique_id += 1
                    out = cv2.VideoWriter('{}{}_{}{}'.format(paths['video'], new_name, unique_id, video_extention),
                                          codec,
                                          fps[dataset],
                                          frame_size[dataset])
                if start <= frame_num < start+max_frame_length:
                    out.write(cv2.resize(image, frame_size[dataset], fx=0, fy=0, interpolation=resize_interpolation))
                if frame_num == gt.loc[index, 'end']:
                    out.release()
                    count += 1
                    try:
                        index = gt.index[count]
                        start = gt.loc[index, 'start']
                    except:
                        break
                success, image = vidcap.read()
                frame_num += 1
            vidcap.release()

    elif dataset == 'ixmas':
        print('{} pre-processing:'.format(dataset))
        samples = [f for f in os.listdir(former_paths[dataset]) if
                   os.path.isfile(os.path.join(former_paths[dataset], f)) and f[-4:] == '.avi'
                   and f not in pd.read_csv(gt_paths['ixmas'])['samples'].values]
        count = 1
        for i, file in enumerate(samples):
            res = [j for j in range(len(file)) if file.startswith('_', j)]
            actor = file[:res[0]]
            action = file[res[1]+1:res[2]]
            if action == 'wave':
                action = 'wave1'
            elif action == 'turn-around':
                action = 'turn'
            elif action == 'punch':
                action = 'box'
            new_name = '{}_{}_{}'.format(dataset, actor, action)
            print('\tSplitting: {}{}'.format(former_paths[dataset], file))
            vidcap = cv2.VideoCapture('{}{}'.format(former_paths[dataset], file))
            success, image = vidcap.read()
            frame_num = 0
            out = cv2.VideoWriter('{}{}_{}{}'.format(paths['video'], new_name, count, video_extention),
                                  codec,
                                  fps[dataset],
                                  frame_size[dataset])
            while success:
                if frame_num % max_frame_length == 0 and frame_num != 0:
                    out.release()
                    count += 1
                    frame_num = 0
                    out = cv2.VideoWriter('{}{}_{}{}'.format(paths['video'], new_name, count, video_extention),
                                          codec,
                                          fps[dataset],
                                          frame_size[dataset])
                elif frame_num % max_frame_length < max_frame_length:
                    out.write(cv2.resize(image, frame_size[dataset], fx=0, fy=0, interpolation=resize_interpolation))
                success, image = vidcap.read()
                frame_num += 1
            out.release()
            vidcap.release()

    elif dataset == 'kth':
        print('{} pre-processing:'.format(dataset))
        gt = pd.read_csv(gt_paths[dataset], header=0)
        convert_gt = pd.DataFrame(columns=['sample', 'start', 'end'])
        for i, row in gt.iterrows():
            for k in ['Seq1', 'Seq2', 'Seq3', 'Seq4']:
                if not row[k] == 'None':
                    convert_gt = convert_gt.append({'sample': row['Sample'],
                                                    'start': int(row[k][:row[k].find('-')]),
                                                    'end': int(row[k][row[k].find('-')+1:])}, ignore_index=True)
    
        samples = [f for f in os.listdir(former_paths[dataset]) if
                   os.path.isfile(os.path.join(former_paths[dataset], f))]
        unique_id = 0
        for i in samples:
            print('\t', 'Splitting: {}'.format(i))
            res = [j for j in range(len(i)) if i.startswith('_', j)]
            actor = i[:res[0]]
            action = i[res[0]+1:res[1]]
            if action == 'running':
                action = 'run'
            elif action == 'walking':
                action = 'walk'
            elif action == 'handwaving':
                action = 'wave2'
            elif action == 'boxing':
                action = 'box'
            elif action == 'hwav2':
                action = 'wave2'
            elif action == 'jogging':
                action = 'jog'
            elif action == 'handclapping':
                action = 'hands-clap'
            bool = convert_gt['sample'] == i
    
            vidcap = cv2.VideoCapture(former_paths[dataset] + i)
            success, image = vidcap.read()
            frame_num = 1
            count = 0
            index = convert_gt.loc[bool].index[count]
            start = convert_gt.loc[index, 'start']
            while success:
                if frame_num >= start+max_frame_length:
                    out.release()
                    start = frame_num
                if frame_num == start:
                    new_name = '{}_{}_{}'.format(dataset, actor.lower(), action)
                    unique_id += 1
                    filename = '{}{}_{}{}'.format(paths['video'], new_name, unique_id, video_extention)
                    out = cv2.VideoWriter(filename,
                                          codec,
                                          fps[dataset],
                                          frame_size[dataset])
                if start <= frame_num < start+max_frame_length:
                    out.write(cv2.resize(image, frame_size[dataset], fx=0, fy=0, interpolation=resize_interpolation))
                if frame_num == convert_gt.loc[index, 'end']:
                    out.release()
                    count += 1
                    try:
                        index = convert_gt.loc[bool].index[count]
                        start = convert_gt.loc[index, 'start']
                    except:
                        break
                success, image = vidcap.read()
                frame_num += 1
            vidcap.release()

    elif dataset == 'i3dpost':
        print('{} pre-processing:'.format(dataset))
        gt = pd.read_csv(gt_paths[dataset], header=0, dtype=str)
        actors = os.listdir(former_paths[dataset])
        unique_id = 0
        for actor in actors:
            child_dir = os.listdir(os.path.join(former_paths[dataset], actor))[0]
            sets = os.listdir(os.path.join(former_paths[dataset], actor, child_dir))
            for s in sets:
                action = gt.loc[(gt['Code'] == s) & (gt['Actor'] == actor), 'Action'].values[0].lower()
                if action == 'Hand-wave':
                    action = 'wave1'
                elif action == 'jump in place':
                    action = 'pjump'
                path = os.path.join(former_paths[dataset], actor, child_dir, s)
                point_of_views = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
                for pov in point_of_views:
                    folder = os.path.join(path, pov)
                    tot_frames = len([f for f in os.listdir(folder) if f.endswith('.png')])
                    num_clips_per_vid = 3
    
                    start = round((tot_frames - (num_clips_per_vid*max_frame_length)) / 2)
                    end = start + max_frame_length
                    new_name = '{}_{}_{}'.format(dataset, actor.lower(), action)
                    for count in range(num_clips_per_vid):
                        unique_id += 1
                        print('\tEncoding: {}_{}{}'.format(new_name, unique_id, video_extention))
                        out = cv2.VideoWriter('{}{}_{}{}'.format(paths['video'], new_name, unique_id, video_extention),
                                              codec,
                                              fps[dataset],
                                              frame_size[dataset])
                        for frame_num in range(start, end):
                            image = cv2.imread(folder+'/'+'0'*(5-len(str(frame_num)))+str(frame_num)+'.png')
                            out.write(cv2.resize(image, frame_size[dataset], fx=0, fy=0, interpolation=resize_interpolation))
                        out.release()
                        start = end
                        end = start + max_frame_length


def remove_short_clips():
    print('Removing short clips (less than {} frames)'.format(min_frame_length))
    to_drop = []
    for sample in os.listdir(paths['video']):
        video = cv2.VideoCapture(os.path.join(paths['video'], sample))
        if int(video.get(cv2.CAP_PROP_FRAME_COUNT)) < min_frame_length:
            to_drop.append(sample)

    for sample in to_drop:
        os.remove(os.path.join(paths['video'], sample))
        print('\t Removed: {}'.format(sample))
    print('Removed {} files'.format(len(to_drop)))

    return None


if __name__ == '__main__':
    process_former_dataset('weizmann')
    process_former_dataset('isldas')
    process_former_dataset('isld')
    process_former_dataset('ixmas')
    process_former_dataset('kth')
    process_former_dataset('i3dpost')
    remove_short_clips()













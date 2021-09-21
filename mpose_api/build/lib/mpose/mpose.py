import os
import numpy as np
from tqdm import tqdm
import numpy as np
from .utils import download_file, unzip, read_yaml
import importlib_resources as pkg_resources
import mpose

#----

class MPOSE():

    def __init__(self,
                 pose_extractor,
                 split='1',
                 transform=None,
                 verbose=False,
                 data_dir='./',
                 config_file=None,
                 velocities=False,
                 remove_zip=False
                 ):
        
        """
        :param pose_extractor: the method used to extract 2D poses (OpenPose or PoseNet)
        :param split: data train/test division (1, 2 or 3)
        :param transform: list of transformations function applied to the raw data
        :param bool verbose: verbosity flag
        :param config_file: path of the configuration file
        :param bool velocities: whether to include velocities in data 
        :param string normalization: type of normalization to apply to data
        :param shape: desired data shape
        :param bool remove_zip: whether to remove zip after download (if True, data_reset() is not available)
        """

        if verbose:
            print(f"Initializing MPOSE2021: Pose Extractor is {pose_extractor}, Split is {split}")
            
        # Configuration
        self.pose_extractor = pose_extractor
        self.split = split
        self.verbose = verbose
        self.remove_zip = remove_zip
        
        if config_file is None:
            with pkg_resources.path(mpose, 'config.yaml') as config:
                self.config_file = config
        
        self.get_config()
        
        self.T = self.config['DATASET']['T']
        self.F = self.config['DATASET']['F']
        self.K = self.config['DATASET'][pose_extractor]['K']
        self.center_keypoint_1 = self.config['DATASET'][pose_extractor]['center_1']
        self.center_keypoint_2 = self.config['DATASET'][pose_extractor]['center_2']
        self.module_keypoint = self.config['DATASET'][pose_extractor]['module_keypoint']
            
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.train_ids = None
        self.test_ids = None
        
        # Get Data
        self.download_data()
        self.download_list()
        self.load_data()
        self.load_list()
        
        # Transformations
        if velocities:
            self.add_velocities()
            
        if transform == 'scale_and_center':
            self.scale_and_center()
        elif transform == 'scale_to_unit':
            self.scale_to_unit()
        elif callable(transform):
            self.transform(transform)

#----            
            
    # Configuration         
    def get_config(self):
        self.config = read_yaml(self.config_file)
   
    # Get Data
    def download_data(self):
        print(f"Downloading Data...")
        data_url = self.config['URLS'][self.pose_extractor]['split_' + self.split]
        download_path = self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        download_file(data_url, download_path + '.zip')
        print(f"Extracting Archive to {download_path}...")
        unzip(download_path + '.zip', download_path)
        if self.remove_zip is True:
            print(f"Removing Archive...")
            os.remove(download_path + '.zip')

    def download_list(self):
        print(f"Downloading txt Files...")
        data_url = self.config['URLS'][self.pose_extractor]['txt_' + self.split]
        download_path = self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        download_file(data_url, download_path + '/' + self.split + '.txt')
        
    def load_data(self):
        self.X_train = np.load(self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split + '/X_train.npy')
        self.y_train = np.load(self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split + '/y_train.npy')
        self.X_test = np.load(self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split + '/X_test.npy')
        self.y_test = np.load(self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split + '/y_test.npy')
    
    def load_list(self):
        test_list = []
        train_list = []
        end = 0
        list_path = self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split
        f = open(list_path + '/' + self.split + '.txt', "r")
        while not end:
            line = f.readline().split('\t')
            if line == ['']:    
                end = 1
            elif line[1].startswith('test'):
                test_list.append(line[0])
            elif line[1].startswith('train'):
                train_list.append(line[0])        
        self.train_ids = np.stack(train_list)
        self.test_ids = np.stack(test_list)
        
    # Transformations
    def transform(self, transform=None, target='X'):
        if not callable(transform):
            print('Error! "transform" must be a valid function having "target" (X or y) as argument and return')
        if target == 'X':
            self.X_train = transform(self.X_train)
            self.X_test = transform(self.X_test)
        elif target == 'y':
            self.y_train = transform(self.y_train)
            self.y_test = transform(self.y_test)
    
    def scale_and_center(self):
        for X in [self.X_train, self.X_test]:
            seq_list = []
            for seq in X:
                pose_list = []
                for pose in seq:
                    zero_point = (pose[self.center_keypoint_1, :2] + pose[self.center_keypoint_2,:2]) / 2
                    scale_mag = np.linalg.norm(zero_point - pose[self.module_keypoint,:2])
                    if scale_mag < 1:
                        scale_mag = 1
                    pose[:,:2] = (pose[:,:2] - zero_point) / scale_mag
                    pose_list.append(pose)
                seq = np.stack(pose_list)
                seq_list.append(seq)
            X = np.stack(seq_list)
            
    def scale_to_unit(self):
        for X in [self.X_train, self.X_test]:
            seq_list = []
            for seq in X:
                pose_list = []
                for pose in seq:
                    bbox = np.array([[np.min(pose[:,0]), np.max(pose[:,0])], [np.min(pose[:,1]), np.max(pose[:,1])]])
                    max_dim = np.max(bbox[:,1] - bbox[:,0])
                    if max_dim < 1:
                        max_dim = 1
                    pose[:,:2] = (pose[:,:2] - bbox[:,0]) / max_dim
                    pose_list.append(pose)
                seq = np.stack(pose_list)
                seq_list.append(seq)
            X = np.stack(seq_list)

    def add_velocities(self):
        seq_list = []
        for seq in self.X_train:
            v1 = np.zeros((self.T+1, self.K, self.F-1))
            v2 = np.zeros((self.T+1, self.K, self.F-1))
            v1[1:,...] = seq[:,:,:2]
            v2[:self.T,...] = seq[:,:,:2]
            vel = (v2-v1)[:-1,...]
            data = np.concatenate((seq[:,:,:2], vel), axis=-1)
            data = np.concatenate((data, seq[:,:,-1:]), axis=-1)       
            seq_list.append(data)
        self.X_train = np.stack(seq_list)

        seq_list = []
        for seq in self.X_test:
            v1 = np.zeros((self.T+1, self.K, self.F-1))
            v2 = np.zeros((self.T+1, self.K, self.F-1))
            v1[1:,...] = seq[:,:,:2]
            v2[:self.T,...] = seq[:,:,:2]
            vel = (v2-v1)[:-1,...]
            data = np.concatenate((seq[:,:,:2], vel), axis=-1)
            data = np.concatenate((data, seq[:,:,-1:]), axis=-1)
            seq_list.append(data)
        self.X_test = np.stack(seq_list)
             
    def reset_data(self):
        if self.remove_zip is True:
            print('Error! The zip file was removed from disk because remove_zip = True')
        else:
            self.load_data()
        
    # Utilities        
    def get_dataset(self, seq_id=False):
        if seq_id:
            return self.X_train, self.y_train, self.train_ids, self.X_test, self.y_test, self.test_ids
        return self.X_train, self.y_train, self.X_test, self.y_test
    
    def get_info(self):
        print('----Dataset Information----')
        print(f'Pose Extractor: {self.pose_extractor}')
        print(f'Split: {self.pose_extractor}') 
        print(f'X_train shape: {self.X_train.shape}')
        print(f'X_test shape: {self.X_test.shape}')
        print('Min-Max feature ranges:')
        print(f'x: {[np.min(self.X_train[:,:,:,0]), np.max(self.X_train[:,:,:,0])]}')
        print(f'y: {[np.min(self.X_train[:,:,:,1]), np.max(self.X_train[:,:,:,1])]}')
        if self.X_train.shape[-1] > 3:
            print(f'Vx: {[np.min(self.X_train[:,:,:,2]), np.max(self.X_train[:,:,:,2])]}')
            print(f'Vy: {[np.min(self.X_train[:,:,:,3]), np.max(self.X_train[:,:,:,3])]}')
        print(f'p: {[np.min(self.X_train[:,:,:,-1]), np.max(self.X_train[:,:,:,-1])]}')

    def get_labels(self):
        return self.config['DATASET']['labels']
#----            
        
if __name__ == '__main__':
    MPOSE(pose_extractor, split=1, transform=None, verbose=False, root=None)
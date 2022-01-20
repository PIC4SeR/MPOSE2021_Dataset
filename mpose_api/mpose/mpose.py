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
                 pose_extractor='openpose',
                 split=1,
                 preprocess=None,
                 config_file=None,
                 velocities=False,
                 remove_zip=False,
                 overwrite=False,
                 verbose=True
                 ):
        
        """
        :param pose_extractor: the method used to extract 2D poses (openpose or posenet)
        :param split: the train/test split to use
        :param preprocess: preprocess function to apply to the raw data
        :param config_file: path of the configuration file
        :param bool velocities: whether to include velocities in data 
        :param string normalization: type of normalization to apply to data
        :param shape: desired data shape
        :param bool remove_zip: whether to remove zip after download (if True, data_reset() is not available)
        :param bool overwrite: whether to overwrite previously downloaded files
        """
            
        # Configuration
        self.pose_extractor = pose_extractor
        self.split = str(split)
        self.preprocess = preprocess
        self.config_file = config_file
        self.velocities = velocities
        self.remove_zip = remove_zip
        self.overwrite = overwrite
        self.verbose = verbose
        
        self.get_config()
        
        self.T = self.config['DATASET']['T']
        self.C = self.config['DATASET']['C']
        self.K = self.config['DATASET'][pose_extractor]['K']
        self.center_1 = self.config['DATASET'][pose_extractor]['center_1']
        self.center_2 = self.config['DATASET'][pose_extractor]['center_2']
        self.module_keypoint_1 = self.config['DATASET'][pose_extractor]['module_keypoint_1']
        self.module_keypoint_2 = self.config['DATASET'][pose_extractor]['module_keypoint_2']
        self.h = self.config['DATASET'][self.pose_extractor]['head']
        self.rf = self.config['DATASET'][self.pose_extractor]['right_foot']
        self.lf = self.config['DATASET'][self.pose_extractor]['left_foot']
        
        
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.train_ids = None
        self.test_ids = None
        
        # Get Data
        self.download_data()
        self.load_data()
        self.load_list()
        
        # Transforms
        self.apply_transforms()
         
            
    # Configuration         
    def get_config(self):
        if self.verbose:
            print(f"Initializing MPOSE2021 with {self.pose_extractor} Pose Extractor")
        if self.config_file is None:
            with pkg_resources.path(mpose, 'config.yaml') as config:
                self.config_file = config
        self.config = read_yaml(self.config_file)
   

    # Get Data
    def download_data(self):
        if self.verbose:
            print(f"Downloading Data...")
        if not os.path.exists(self.config['CACHE_DIR']):
            os.makedirs(self.config['CACHE_DIR'])
        download_file(self.config['URLS'][self.pose_extractor], self.config['CACHE_DIR']+self.pose_extractor+'.zip',
                      overwrite=self.overwrite, verbose=self.verbose)
        if self.verbose:
            print(f"Extracting Data...")
        if not os.path.exists(self.config['CACHE_DIR']+self.pose_extractor+'/'+self.split+'/'):
            if self.verbose:
                print(f"Extracting Archive to {self.config['CACHE_DIR']}...")
            unzip(self.config['CACHE_DIR']+self.pose_extractor+'.zip', self.config['CACHE_DIR'])
        elif self.verbose:
            print(f"File exists in {self.config['CACHE_DIR']+self.pose_extractor+'/'}. specify overwrite=True if intended")
        if self.remove_zip:
            if self.verbose:
                print(f"Removing Archive...")
            os.remove(self.config['CACHE_DIR']+self.pose_extractor+'.zip')
        
    def load_data(self):
        self.X_train = np.load(self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split + '/X_train.npy')
        self.y_train = np.load(self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split + '/y_train.npy')
        self.X_test = np.load(self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split + '/X_test.npy')
        self.y_test = np.load(self.config['CACHE_DIR'] + self.pose_extractor + '/' + self.split + '/y_test.npy')
        self.scaled = False
        
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
        
        
    # Transforms
    def apply_transforms(self):
        if self.velocities:
            self.add_velocities() 
        if self.preprocess == 'scale_and_center':
            self.scale_and_center()
        elif self.preprocess == 'scale_to_unit':
            self.scale_to_unit()   
        elif callable(self.preprocess):
            self.transform_fn(self.preprocess)
    
    def transform(self, fn=None, target='X'):
        if not callable(fn):
            print('Error! "transform" must be a valid function having "target" (X or y) as argument and return')
        if target == 'X':
            self.X_train = fn(self.X_train)
            self.X_test = fn(self.X_test)
        elif target == 'y':
            self.y_train = fn(self.y_train)
            self.y_test = fn(self.y_test)
            
    def reduce_keypoints(self):
        if self.X_train.shape[2] <= 15:
            print('Keypoint number has already been reduced!')
            return
        elif self.scaled:
            print('Poses already scaled. Please call reduce_keypoints() only before scale_and_center()!')
            return
        seq_list = []
        to_prune = []
        
        for group in [self.h, self.rf, self.lf]:
            if len(group) > 1:
                to_prune.append(group[1:])
        to_prune = [item for sublist in to_prune for item in sublist]
        
        for seq in self.X_train:
            seq[:,self.h[0],:] = np.true_divide(seq[:,self.h,:].sum(1), (seq[:,self.h,:] != 0).sum(1)+1e-9)
            seq[:,self.rf[0],:] = np.true_divide(seq[:,self.rf,:].sum(1), (seq[:,self.rf,:] != 0).sum(1)+1e-9)
            seq[:,self.lf[0],:] = np.true_divide(seq[:,self.lf,:].sum(1), (seq[:,self.lf,:] != 0).sum(1)+1e-9)
            seq_list.append(seq)
        self.X_train = np.stack(seq_list)
        self.X_train = np.delete(self.X_train, to_prune, 2)
        
        seq_list = []
        for seq in self.X_test:
            seq[:,self.h[0],:] = np.true_divide(seq[:,self.h,:].sum(1), (seq[:,self.h,:] != 0).sum(1)+1e-9)
            seq[:,self.rf[0],:] = np.true_divide(seq[:,self.rf,:].sum(1), (seq[:,self.rf,:] != 0).sum(1)+1e-9)
            seq[:,self.lf[0],:] = np.true_divide(seq[:,self.lf,:].sum(1), (seq[:,self.lf,:] != 0).sum(1)+1e-9)
            seq_list.append(seq)           
        self.X_test = np.stack(seq_list)
        self.X_test = np.delete(self.X_test, to_prune, 2)
        
    def scale_and_center(self):
        if self.scaled:
            print('Poses already scaled!')
            return
       
        for X in [self.X_train, self.X_test]:
            seq_list = []
            for seq in X:
                pose_list = []
                for pose in seq:
                    zero_point = (pose[self.center_1, :2] + pose[self.center_2,:2]) / 2
                    module_keypoint = (pose[self.module_keypoint_1, :2] + pose[self.module_keypoint_2,:2]) / 2
                    scale_mag = np.linalg.norm(zero_point - module_keypoint)
                    if scale_mag < 1:
                        scale_mag = 1
                    pose[:,:2] = (pose[:,:2] - zero_point) / scale_mag
                    pose_list.append(pose)
                seq = np.stack(pose_list)
                seq_list.append(seq)
            X = np.stack(seq_list)
        
        self.X_train = np.delete(self.X_train, self.config['DATASET'][self.pose_extractor]['prune'], 2)
        self.X_test = np.delete(self.X_test, self.config['DATASET'][self.pose_extractor]['prune'], 2)
        self.scaled = True
        
        if self.X_train.shape[-1] > 3:
            self.add_velocities(overwrite=True)
        
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
            
        if self.X_train.shape[-1] > 3:
            self.add_velocities(overwrite=True)
        
    def add_velocities(self, overwrite=False):
        if self.X_train.shape[-1] > 3:
            if not overwrite:
                print('Velocities already added, specify overwrite=True to recompute them!')
                return
            self.remove_velocities()
        
        seq_list = []
        for seq in self.X_train:
            v1 = np.zeros((self.T+1, seq.shape[1], self.C-1))
            v2 = np.zeros((self.T+1, seq.shape[1], self.C-1))
            v1[1:,...] = seq[:,:,:2]
            v2[:self.T,...] = seq[:,:,:2]
            vel = (v2-v1)[:-1,...]
            data = np.concatenate((seq[:,:,:2], vel), axis=-1)
            data = np.concatenate((data, seq[:,:,-1:]), axis=-1)       
            seq_list.append(data)
        self.X_train = np.stack(seq_list)

        seq_list = []
        for seq in self.X_test:
            v1 = np.zeros((self.T+1, seq.shape[1], self.C-1))
            v2 = np.zeros((self.T+1, seq.shape[1], self.C-1))
            v1[1:,...] = seq[:,:,:2]
            v2[:self.T,...] = seq[:,:,:2]
            vel = (v2-v1)[:-1,...]
            data = np.concatenate((seq[:,:,:2], vel), axis=-1)
            data = np.concatenate((data, seq[:,:,-1:]), axis=-1)
            seq_list.append(data)
        self.X_test = np.stack(seq_list)
            
    def remove_velocities(self):
        if self.X_train.shape[-1] <= 3:
            print('Velocities already removed!')
            return
        
        self.X_train = np.delete(self.X_train, [2,3], -1)
        self.X_test = np.delete(self.X_test, [2,3], -1)
        
    def remove_confidence(self):
        self.X_train = self.X_train[...,:-1]
        self.X_test = self.X_test[...,:-1]
            
    def flatten_features(self):
        self.X_train = self.X_train.reshape(self.X_train.shape[0], self.T, -1)
        self.X_test = self.X_test.reshape(self.X_test.shape[0], self.T, -1)
    
    def reduce_labels(self):
        for i in range(len(self.y_train)):
            self.y_train[i] = self.config['DATASET']['red_lab'][str(self.y_train[i])]
        for i in range(len(self.y_test)):
            self.y_test[i] = self.config['DATASET']['red_lab'][str(self.y_test[i])]
    
    def reset_data(self):
        if self.remove_zip is True:
            print('Error! The zip file was removed from disk!')
            return
        self.load_data()
        
        
    # Utilities        
    def get_data(self, seq_id=False):
        if seq_id:
            return self.X_train, self.y_train, self.train_ids, self.X_test, self.y_test, self.test_ids
        return self.X_train.copy(), self.y_train.copy(), self.X_test.copy(), self.y_test.copy()
    
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
        if self.X_train.shape[-1] % 2:
            print(f'p: {[np.min(self.X_train[:,:,:,-1]), np.max(self.X_train[:,:,:,-1])]}')

    def get_labels(self):
        return self.config['DATASET']['labels']
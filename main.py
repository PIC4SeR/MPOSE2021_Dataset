import argparse

import scripts.init_vars
import scripts.extract_formers
import scripts.extract_json
import scripts.extract_posenet_pose
import scripts.create_video
import scripts.create_rgb_pose
import scripts.create_splits
import scripts.refine_dataset
import scripts.check_integrity
import scripts.generate_figures


def get_args():
    parser = argparse.ArgumentParser(description='Script to automatically generate MPOSE2021 Dataset (RGB+POSE)',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--mode', '-m', default='init', help='Operation to be performed (init, extract, generate, check)')
    parser.add_argument('--pose', '-p', default='all', help='Poses to extract (openpose, all)')
    parser.add_argument('--force','-f', action='store_true', help='Whether to force data extraction') 
    parser.add_argument('--verbose','-v', action='store_true', help='Whether to force data extraction') 
    
    return parser.parse_args()

def main():
    args = get_args()

    # Initialization
    scripts.init_vars.init_vars(args.verbose)
    if args.mode == 'init':
        return
    
    if args.mode != 'check':
        # Data Extraction
        scripts.extract_formers.extract_formers(force=args.force, verbose=args.verbose)
        scripts.extract_json.extract_json(force=args.force, verbose=args.verbose)
        if args.pose == 'all':
            scripts.extract_posenet_pose.extract_posenet_pose(force=args.force, verbose=args.verbose)
        if args.mode == 'extract':
            return
    
        # Data Processing
        scripts.create_video.create_video(force=args.force, verbose=args.verbose)
        scripts.create_rgb_pose.create_rgb_pose(force=args.force, verbose=args.verbose)
        scripts.refine_dataset.refine_dataset(verbose=args.verbose)
        scripts.create_splits.create_splits(force=args.force, verbose=args.verbose)
    
    # Data Checking
    scripts.check_integrity.check_integrity('video')
    scripts.check_integrity.check_integrity('rgb')
    scripts.check_integrity.check_integrity('pose')
    scripts.generate_figures.generate_figures(force=args.force, verbose=args.verbose)
    
if __name__ == '__main__':
    main()
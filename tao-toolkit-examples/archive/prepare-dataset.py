import os
import shutil
from random import sample, seed
import argparse

def prepare_output_directories(output_dir_path):
    output_dirs = ['train', 'val', 'test']
    for d in output_dirs:
        target_dir = os.path.join(output_dir_path, d)        
        if not os.path.exists(target_dir):
            print(f"Creating directory: {target_dir}")
            os.makedirs(target_dir)

def prepare_image_lists(input_dir, split_pct):

    # base set of files    
    img_files = [i for i in os.listdir(input_dir) if i.endswith('.jpg') or i.endswith('.png')]
    test_files = img_files.copy()

    # determine which files go to which location
    seed(42) # set random seed for reproducibility
    train_count = int(round(split_pct * len(img_files), 0))
    val_count = len(img_files) - train_count
    val_files = sample(img_files, val_count)

    # filter the training files
    train_files = [i for i in img_files if i not in val_files]    

    # make sure we didn't lose anything
    assert len(train_files) + len(val_files) == len(test_files)

    return (train_files, val_files, test_files)
    
def copy_files_to_dir(input_dir, output_dir, file_lst):
    for f in file_lst:
        src_file = os.path.join(input_dir, f)
        target_file = os.path.join(output_dir, f)       

        if src_file.endswith('.jpg'):
            json_src = src_file.replace('.jpg', '.json')
            json_target = target_file.replace('.jpg', '.json')
        elif src_file.endswith('.png'):
            json_src = src_file.replace('.png', '.json')
            json_target = target_file.replace('.png', '.json')
        
        if not os.path.exists(json_src):
            print(f'[WARN] annotation for file does not exist for {json_src}. Skipping... ')
        else:
            shutil.copyfile(src_file, target_file)
            shutil.copyfile(json_src, json_target)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument('--train_pct', help="Percentage represented as decimal for how to split dat into train and validation set", type=float,default=.9)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    print(args.input_dir)
    print(args.output_dir)
    print(args.train_pct)   

    input_dir = args.input_dir
    output_dir = args.output_dir
    TRAIN_PCT = args.train_pct


    prepare_output_directories(output_dir)


    train_files, val_files, test_files = prepare_image_lists(input_dir, TRAIN_PCT)

    print(f"Training image count: {len(train_files)}")
    print(f"Validation image count: {len(val_files)}")
    print(f"Testing image count: {len(test_files)}")

    train_dir_path = os.path.join(output_dir, "train")
    val_dir_path = os.path.join(output_dir, "val")
    test_dir_path = os.path.join(output_dir, "test")

    copy_files_to_dir(input_dir, train_dir_path, train_files)
    copy_files_to_dir(input_dir, val_dir_path, val_files)
    copy_files_to_dir(input_dir, test_dir_path, test_files)    



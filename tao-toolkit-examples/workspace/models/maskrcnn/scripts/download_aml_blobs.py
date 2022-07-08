import argparse
import os
import os.path as osp
import sys
import collections
import datetime
import shutil
from random import sample, seed
import glob
import json
import configparser

# Import the client object from the SDK library
from azure.storage.blob import BlobClient, ContainerClient
from azure.storage.blob import ContentSettings

def download_aml_images(images_names_list, continer_client, out_dir):

    # Initialize the connection to Azure storage account
    for x in images_names_list:
        dest_filename = x
        index = dest_filename.rfind('/')
        dest_file = dest_filename[(index+1):]
        # print(f"input file = {dest_filename}")

        blob_client = container_client.get_blob_client(x)

        # Open a local file and upload its contents to Blob Storage
        dest_fullpath = os.path.join(out_dir, dest_file)        
        with open(dest_fullpath, "wb") as my_blob:
            print(f"Saving blob to: {dest_fullpath}")
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())

def read_coco_file(coco_file):
    with open(coco_file) as f_in:
        return json.load(f_in)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--storage_account_url", default="https://storagebt2l2ppiwh3sa.blob.core.windows.net")
    parser.add_argument("--container_name", default="training-data")
    parser.add_argument("--sas_token", default="sp=r&st=2022-06-30T04:12:43Z&se=2022-12-31T13:12:43Z&spr=https&sv=2021-06-08&sr=c&sig=2%2Fw%2FIwAPdKKDB4Oo7Vr0SvtfkFfDL%2BJqLiO2hJKQdLM%3D")
    parser.add_argument("--annotations_file", default="workspace/data/annotations.json")
    parser.add_argument("--output_dir")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
     
    # parse args
    ACCOUNT_URL = args.storage_account_url
    CONTAINER_NAME = args.container_name
    SAS_READ_ACCESS = args.sas_token    
    annotations_json = args.annotations_file
    output_dir = args.output_dir
    
    print("Reading COCO annotations file")    
    coco_annotations = read_coco_file(annotations_json)

    image_names = [i['file_name'] for i in coco_annotations['images']]

    file_count = len(image_names)
    print(f"Number of files to be downloaded: {file_count}")


    if not os.path.exists(output_dir):
        print("[INFO] Output directory does not exist. Creating now")
        os.makedirs(output_dir)
        
    container_client = ContainerClient(account_url=ACCOUNT_URL, container_name=CONTAINER_NAME, credential=SAS_READ_ACCESS)
    download_aml_images(image_names, container_client, output_dir)




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

def download_aml_images(images_names_list, conn_string, blob_container_id, out_dir):

    # Initialize the connection to Azure storage account
    for x in images_names_list:
        dest_filename = x
        index = dest_filename.rfind('/')
        dest_file = dest_filename[(index+1):]
        # print(f"input file = {dest_filename}")
        print(f"output file = {dest_file}")

        blob_client = BlobClient.from_connection_string(conn_string,
        container_name=blob_container_id, blob_name=x)

        # Open a local file and upload its contents to Blob Storage
        dest_fullpath = os.path.join(out_dir, dest_file)
        with open(dest_fullpath, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())

def read_coco_file(coco_file):
    with open(coco_file) as f_in:
        return json.load(f_in)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_config_file")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    print(args.input_config_file)
 
    # read config
    config = configparser.ConfigParser()
    config.read(args.input_config_file)
    conn_string = config.get('section', 'connection_string')
    container_id = config.get('section', 'Blob_Container_id')
    aml_label_json = config.get('Path', 'aml_exported_coco_json')
    output_dir = config.get('Path', 'output_dir')

    # print(f"conn_string = {conn_string}")
    print(f"container_id = {container_id}")

    input_file = aml_label_json

    coco_data = read_coco_file(input_file)
    # print(f"coco data = {coco_data}")

    file_count = len(coco_data["images"])
    print(f"counts of files = {file_count}")

    images_names = []
    for i in range(0, len(coco_data["images"])):
        coco_file_name = coco_data["images"][i]["file_name"]
        images_names.append(coco_file_name)

    # get the output folder
    index = aml_label_json.rfind('/')
    # out_dir = aml_label_json[:index]
    print(f"output_dir = {output_dir}")

    download_aml_images(images_names, conn_string, container_id, output_dir)




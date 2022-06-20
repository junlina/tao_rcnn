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

# CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=amlwalmsdwus2d8436142290;AccountKey=IrD/MOSsO342xQ0COSLc/7tZAgTHsMSx2TzC9XwKugvSisCZqiQwNB45Ok1Kp50WgcnzXi6jvATomwmEfcPm4Q==;EndpointSuffix=core.windows.net"
# BLOB_CONTAINER = "azureml-blobstore-f62d7dac-3360-48d1-9530-e20a65fb87a7"

def download_aml_images(images_names_list, conn_string, blob_container_id, out_dir):

    # Initialize the connection to Azure storage account
    for x in images_names_list:
        dest_filename = x
        index = dest_filename.rfind('/')
        dest_file = dest_filename[(index+1):]
        print(f"input file = {dest_filename}")

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
    # print(f"conn_string = {conn_string}")
    print(f"container_id = {container_id}")
    # print(f"aml_label_json = {aml_label_json}")

    # input_file = "../d02242f7-038a-4090-b39c-922e1542d0aa.json"
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
    out_dir = aml_label_json[:index]
    print(f"out_dir = {out_dir}")

    download_aml_images(images_names, conn_string, container_id, out_dir)




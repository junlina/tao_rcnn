
# Mask RCNN

## Scheme-1: Using Azure ML label tool for model training
## ------------------------------------------------------

## step 1: Label item images
Using Azure ML label tool to label the images for model training. please read the document of "Azure ML labeling and data training for mask RCNN.pdf" for details.
After done with labeling, export the container blobs json file. proceed to step 2.

## step 2: Download blob images using Azure storage SDK
Run python3 'download-aml_blobs.py' aml_coco_config.ini 
- input configuration ini file. it's located at the same folder as the one of this python file.
Here is an example: the configuration data includes three parameters: (a). connection_string (b). Blob_Container_id (c).aml_exported_coco_json.

[section]
connection_string = DefaultEndpointsProtocol=https;AccountName=amlwalmsdwus2d8436142290;AccountKey=IrD/MOSsO342xQ0COSLc/7tZAgTHsMSx2TzC9XwKugvSisCZqiQwNB45Ok1Kp50WgcnzXi6jvATomwmEfcPm4Q==;EndpointSuffix=core.windows.net
Blob_Container_id = azureml-blobstore-f62d7dac-3360-48d1-9530-e20a65fb87a7
[Path]
aml_exported_coco_json: ~/repos/manufacturing-demo/workspace/data/inputs/d02242f7-038a-4090-b39c-922e1542d0aa.json

- Output the blob images are stored at the same folder as input json file.

## Step 3: Split all the images into train, val and test subsets
sudo python3 split_aml_exported_coco.py json_file image_folder output --train_pct
- input
json_file  an Azure ML coco json file. e.g. ~/repos/manufacturing-demo/workspace/data/inputs/d02242f7-038a-4090-b39c-922e1542d0aa.json 
image_folder e.g. ~/repos/manufacturing-demo/workspace/data/inputs 

- train_pct percentage of data for training set. Default is 0.8

- output store the train, test and validation set. they are stored in ~/repos/manufacturing-demo/workspace/models/mask_rcnn/workspace/data/outputs

## convert train/test/val/ subset coco files into TFRecord data format
sudo ./process-labels-aml.sh
the script is located int workspace/models/mask_rcnn    
- output: ./workspace/models/mask_rcnn/workspace/data/outputs/TFRecords

## train model
make train-mrcnn-adhoc to train model
- output: ./workspace/models/mask_rcnn/experiment_unpruned

## scheme-2 Using Labelme tool for model training
## ------------------------------------------------------

## Step 1: Label images
We used labelme to label the images for model training
After done with labeling, please proceed to step 2 to prepare datasets for integration with the TAO toolkit

## Step 2: Split into train, val
Run the `prepare-dataset.py` script to split all images into train, test, validation

Inputs to script
- input directory with all image files and json file annotations
- output directory to store your train, test, and validation sets
- percentage of data to use for training set. Default is .9

## Step 3: Convert labels into TFRecords expected by TAO Toolkit
- Update the value in process-labels.sh script located in workspace/models/mask_rcnn folder to point to where your annotated images are stored.

## Run the `process-labels.sh` script found in the workspace/models/mask_rcnn folder
This script goes through two steps:
1) Converts from labelme annotation format to COCO format
2) Converts from COCO format to TFRecords

## Step 4: Run make commands based on needs
make train-mrcnn-adhoc to train model
 
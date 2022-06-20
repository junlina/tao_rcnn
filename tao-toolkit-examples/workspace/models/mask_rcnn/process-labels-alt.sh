#!/bin/bash
# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Script to download and preprocess the COCO data set for detection.
#
# The outputs of this script are TFRecord files containing serialized
# tf.Example protocol buffers. See create_coco_tf_record.py for details of how
# the tf.Example protocol buffers are constructed and see
# http://cocodataset.org/#overview for an overview of the dataset.
#
# usage:
#  bash download_and_preprocess_coco.sh /data-dir/coco
set -e
set -x

PWD="$(pwd)"
BASE_DIR="${PWD}/workspace/data/maskrcnn_images"
TRAIN_DIR="${BASE_DIR}/train"
VAL_DIR="${BASE_DIR}/val"
TEST_DIR="${BASE_DIR}/test"

TRAIN_IMAGE_DIR="${TRAIN_DIR}/coco/JPEGImages"
VAL_IMAGE_DIR="${VAL_DIR}/coco/JPEGImages"
TEST_IMAGE_DIR="${TEST_DIR}/coco/JPEGImages"
# VAL_IMAGE_DIR="/home/edwin/repos/manufacturing-demo/workspace/data/maskrcnn_images/val/coco/JPEGImages"
TRAIN_ANNOTATION_FILE="${TRAIN_DIR}/coco/annotations.json"
VAL_ANNOTATION_FILE="${VAL_DIR}/coco/annotations.json"
TESTDEV_ANNOTATION_FILE="${TEST_DIR}/coco/annotations.json"
OUTPUT_DIR="${BASE_DIR}/tfrecords"
echo $TRAIN_IMAGE_DIR
echo $VAL_IMAGE_DIR
echo $TRAIN_ANNOTATION_FILE
echo $VAL_ANNOTATION_FILE



#sudo apt install -y protobuf-compiler python-pil python-lxml\
#  python-pip python-dev git unzip

#pip install Cython git+https://github.com/cocodataset/cocoapi#subdirectory=PythonAPI

echo "Cloning Tensorflow models directory (for conversion utilities)"
if [ ! -e tf-models ]; then
  git clone http://github.com/tensorflow/models tf-models
fi

(cd tf-models/research && protoc object_detection/protos/*.proto --python_out=.)

CURRENT_DIR=$(pwd)
echo "Current directory is: $CURRENT_DIR"

# # Build TFRecords of the image data.
cd "${CURRENT_DIR}"

# Setup packages
touch tf-models/__init__.py
touch tf-models/research/__init__.py

# Run our conversion
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
echo "Script Directory is: $SCRIPT_DIR"

PYTHONPATH="tf-models:tf-models/research" python $SCRIPT_DIR/create_coco_tf_record.py \
  --logtostderr \
  --include_masks \
  --train_image_dir="${TRAIN_IMAGE_DIR}" \
  --val_image_dir="${VAL_IMAGE_DIR}" \
  --test_image_dir="${TEST_IMAGE_DIR}" \
  --train_object_annotations_file="${TRAIN_ANNOTATION_FILE}" \
  --val_object_annotations_file="${VAL_ANNOTATION_FILE}" \
  --testdev_annotations_file="${TESTDEV_ANNOTATION_FILE}" \
  --output_dir="${OUTPUT_DIR}"

# mv ${SCRATCH_DIR}/annotations/ ${OUTPUT_DIR}

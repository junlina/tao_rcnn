#!/usr/bin/env bash
PWD="$(pwd)"
BASE_DIR="${PWD}/workspace/data/maskrcnn_images"
TRAIN_DIR="${BASE_DIR}/train"
VAL_DIR="${BASE_DIR}/val"
TEST_DIR="${BASE_DIR}/test"

echo "Cloning Tensorflow models directory (for conversion utilities)"
if [ ! -e tf-models ]; then
  git clone http://github.com/tensorflow/models tf-models
fi

(cd tf-models/research && protoc object_detection/protos/*.proto --python_out=.)

# Setup packages
touch tf-models/__init__.py
touch tf-models/research/__init__.py



source ~/deepstream/deepstream_env/bin/activate

LABELME_PARSER_LOCATION="${PWD}/workspace/models/mask_rcnn"


python3 $LABELME_PARSER_LOCATION/labelme2coco.py \
    $TRAIN_DIR \
    "$TRAIN_DIR/coco" \
    --labels workspace/models/mask_rcnn/labels.txt

python3 $LABELME_PARSER_LOCATION/labelme2coco.py \
    $VAL_DIR \
    "$VAL_DIR/coco" \
    --labels workspace/models/mask_rcnn/labels.txt

python3  $LABELME_PARSER_LOCATION/labelme2coco.py \
    $TEST_DIR \
    "$TEST_DIR/coco" \
    --labels workspace/models/mask_rcnn/labels.txt

TRAIN_IMAGE_DIR="${TRAIN_DIR}/coco/JPEGImages"
VAL_IMAGE_DIR="${VAL_DIR}/coco/JPEGImages"
TEST_IMAGE_DIR="${TEST_DIR}/coco/JPEGImages"
# VAL_IMAGE_DIR="/home/edwin/repos/manufacturing-demo/workspace/data/maskrcnn_images/val/coco/JPEGImages"
TRAIN_COCO_ANNOTATION_FILE="${TRAIN_DIR}/coco/annotations.json"
VAL_ANNOTATION_FILE="${TRAIN_DIR}/coco/annotations.json"
TESTDEV_ANNOTATION_FILE="${TEST_DIR}/coco/annotations.json"

echo $TRAIN_IMAGE_DIR
echo $VAL_IMAGE_DIR
echo $TRAIN_COCO_ANNOTATION_FILE
echo $VAL_ANNOTATION_FILE




OUTPUT_DIR="${BASE_DIR}/tfrecords"

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
echo $SCRIPT_DIR

#PYTHONPATH="tf-models:tf-models/research" python $PWD/tf-models/research/object_detection/dataset_tools/create_coco_tf_record.py \
PYTHONPATH="tf-models:tf-models/research" python $PWD/workspace/models/mask_rcnn/specs/create_coco_tf_record.py \
  --logtostderr \
  --include_masks \
  --train_image_dir="${TRAIN_IMAGE_DIR}" \
  --val_image_dir="$VAL_IMAGE_DIR" \
  --test_image_dir="${TEST_IMAGE_DIR}" \
  --train_object_annotations_file="${TRAIN_COCO_ANNOTATION_FILE}" \
  --val_object_annotations_file="${VAL_ANNOTATION_FILE}" \
  --testdev_annotations_file="${TESTDEV_ANNOTATION_FILE}" \
  --output_dir="${OUTPUT_DIR}" \


#   PYTHONPATH="tf-models:tf-models/research" python $SCRIPT_DIR/create_coco_tf_record.py \
#   --logtostderr \
#   --include_masks \
#   --train_image_dir="${TRAIN_IMAGE_DIR}" \
#   --val_image_dir="${VAL_IMAGE_DIR}" \
#   --test_image_dir="${TEST_IMAGE_DIR}" \
#   --train_object_annotations_file="${TRAIN_OBJ_ANNOTATIONS_FILE}" \
#   --val_object_annotations_file="${VAL_OBJ_ANNOTATIONS_FILE}" \
#   --train_caption_annotations_file="${TRAIN_CAPTION_ANNOTATIONS_FILE}" \
#   --val_caption_annotations_file="${VAL_CAPTION_ANNOTATIONS_FILE}" \
#   --testdev_annotations_file="${TESTDEV_ANNOTATIONS_FILE}" \
#   --output_dir="${OUTPUT_DIR}"

# mv ${SCRATCH_DIR}/annotations/ ${OUTPUT_DIR}
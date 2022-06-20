#!/usr/bin/env bash

source ~/deepstream/deepstream_env/bin/activate

sudo rm -r $HOME/repos/manufacturing-demo/workspace/models/unet/experiment_unpruned
mkdir ~/repos/manufacturing-demo/workspace/models/unet/experiment_unpruned

tao unet train \
-k nvidia_tlt \
-r ~/repos/manufacturing-demo/workspace/models/unet/experiment_unpruned \
-e ~/repos/manufacturing-demo/workspace/models/unet/model_config_multiclass.txt \
-m ~/repos/manufacturing-demo/workspace/models/unet/pretrained_resnet18/pretrained_semantic_segmentation_vresnet18/resnet_18.hdf5

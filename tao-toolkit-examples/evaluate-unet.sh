#!/usr/bin/env bash

source ~/deepstream/deepstream_env/bin/activate

sudo rm -r $HOME/repos/manufacturing-demo/workspace/models/unet/evaluate/
mkdir ~/repos/manufacturing-demo/workspace/models/unet/evaluate/

tao unet evaluate \
    -k nvidia_tlt \
    -m ~/repos/manufacturing-demo/workspace/models/unet/experiment_unpruned/weights/model.tlt \
    -e ~/repos/manufacturing-demo/workspace/models/unet/model_config_multiclass.txt \
    -o ~/repos/manufacturing-demo/workspace/models/unet/evaluate/
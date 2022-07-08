SHELL := /bin/bash

clean-outputs:
	sudo rm -rf ~/workspace/models/unet/outputs

unet-pipeline:
	bash ./train-unet.sh
	bash ./evaluate-unet.sh
	bash ./run-inference.sh	

mask-rcnn-pipeline:
	rm -rf ./workspace/data/maskrcnn_images
	source ~/deepstream/deepstream_env/bin/activate
	sudo python3 split_aml_exported_coco.py ./workspace/data/inputs/d02242f7-038a-4090-b39c-922e1542d0aa.json ./workspace/data/inputs  ./workspace/tao-experiments/mask_rcnn/workspace/data/outputs --train_pct 0.8

train-mrcnn-adhoc:
	sudo rm -rf ~/repos/manufacturing-demo3/mask_rcnn/experiment_dir_unpruned
	sudo mkdir ~/repos/manufacturing-demo3/mask_rcnn/experiment_dir_unpruned
	source ~/deepstream/deepstream_env/bin/activate

	tao mask_rcnn train -e /workspace/tao-experiments/mask_rcnn/specs/maskrcnn_train_resnet50.txt \
						-d /experiment_dir_unpruned \
						-k nvidia_tlt \
						--gpus 1	

eval-mrcnn-adhoc:
	source ~/deepstream/deepstream_env/bin/activate

	sudo rm -rf $(HOME)/repos/manufacturing-demo/workspace/models/mask_rcnn/evaluate/
	mkdir ~/repos/manufacturing-demo/workspace/models/mask_rcnn/evaluate/
	
	tao mask_rcnn evaluate \
	 	-e ~/repos/manufacturing-demo/workspace/models/mask_rcnn/maskrcnn_train_resnet50.txt \
		-m ~/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_unpruned/model.step-25000.tlt \
		-k nvidia_tlt

infer-mrcnn-adhoc:
	source ~/deepstream/deepstream_env/bin/activate

	sudo rm -rf $(HOME)/repos/manufacturing-demo/workspace/models/mask_rcnn/outputs/
	mkdir ~/repos/manufacturing-demo/workspace/models/mask_rcnn/outputs/
	
	tao mask_rcnn inference \
		-i ~/repos/manufacturing-demo/workspace/data/images/test \
	 	-o ~/repos/manufacturing-demo/workspace/models/mask_rcnn/outputs \
	 	-e ~/repos/manufacturing-demo/workspace/models/mask_rcnn/maskrcnn_train_resnet50.txt \
		-m ~/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_unpruned/model.step-25000.tlt \
		-l ~/repos/manufacturing-demo/workspace/models/mask_rcnn/maskrcnn_labels.txt \
		-k nvidia_tlt \
		-t .6 \
		--include_mask

prune-mrcnn:
	sudo rm -rf $(HOME)/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_pruned/
	mkdir ~/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_pruned/

	tao mask_rcnn prune \
		-m ~/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_unpruned/model.step-25000.tlt \
		-o ~/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_pruned \
		-pth 0.7 \
		-k nvidia_tlt
	
retrain-pruned-mrcnn:
	sudo rm -rf $(HOME)/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_retrained/
	mkdir ~/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_retrained/	

	tao mask_rcnn train \
		-e ~/repos/manufacturing-demo/workspace/models/mask_rcnn/maskrcnn_retrain_resnet50.txt \
		-d ~/repos/manufacturing-demo/workspace/models/mask_rcnn/experiment_retrained \
		-k nvidia_tlt \
		--gpus 1

tao-export-mrcnn:
	sudo rm -rf $(PWD)/workspace/models/mask_rcnn/export/
	mkdir $(PWD)/workspace/models/mask_rcnn/export/		

	tao mask_rcnn export \
		-m $(PWD)/workspace/models/mask_rcnn/experiment_retrained/model.step-25000.tlt \
		-k nvidia_tlt \
		-e $(PWD)/workspace/models/mask_rcnn/maskrcnn_retrain_resnet50.txt #\
		# --batch_size 1 \
		# --data_type int8 \
		# --cal_image_dir $(PWD)/workspace/data/maskrcnn_images/val/coco/JPEGImages \
		# --batches 10 \
		# --cal_cache_file $(PWD)/workspace/models/mask_rcnn/export/maskrcnn.cal \
		# --cal_data_file $(PWD)/workspace/models/mask_rcnn/export/maskrcnn.tensorfile

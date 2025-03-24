#!/bin/bash

echo "Labeling setup"
echo "Activate conda environment"
source activate label-studio


video_name="tolabel_copie"

echo "Changing settings"
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT="/Users/martin.dejaeghere/Microsint2/yolo/datasets_${video_name}"
export CONVERTER_DOWNLOAD_RESOURCES=1

echo "Running label-studio-converter import yolo"
label-studio-converter import yolo \
    -i "/Users/martin.dejaeghere/Microsint2/yolo/datasets_${video_name}/one" \
    -o "/Users/martin.dejaeghere/Microsint2/yolo/datasets_${video_name}/one/output.json" \
    --image-root-url "/data/local-files/?d=one/images"


echo "Starting label-studio ..."
label-studio start

# Pause equivalent in bash
read -p "Press any key to stop label-studio and continue..."

echo "Stopping label-studio ..."
label-studio stop

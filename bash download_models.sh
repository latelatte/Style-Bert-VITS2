#!/bin/bash

echo "Downloading model files..."
mkdir -p model_assets

# Google Drive方式
gdown https://drive.google.com/drive/folders/1pePr_0dj_f77NXngyFBAscbruWpKgwG3?usp=sharing -O model_assets


echo "Download complete."

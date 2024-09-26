#!/bin/bash
echo "Downloading checkpoints for segment-anything-2"
cd segment-anything-2/checkpoints
chmod +x ./download_ckpts.sh
./download_ckpts.sh

#!/usr/bin/env bash
# Download the ds007067 fieldmaps from OpenNeuro's public S3 bucket
set -euo pipefail

DATA=./data/ds007067
S3=https://s3.amazonaws.com/openneuro.org/ds007067
source "$(dirname "$0")/subjects.sh" "$@"
FILES="magnitude1 magnitude2 phasediff"

for SUB in $SUBJECTS; do
    echo "=========== $SUB ==========="
    mkdir -p "$DATA/$SUB/fmap"
    for F in $FILES; do
        for EXT in nii.gz json; do
            NAME=${SUB}_${F}.${EXT}
            curl -sSf -o "$DATA/$SUB/fmap/$NAME" "$S3/$SUB/fmap/$NAME"
            echo "  $NAME"
        done
    done
done

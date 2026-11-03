DATA=./data/ds007067
source "$(dirname "$0")/subjects.sh" "$@"

for SUB in $SUBJECTS; do
    echo "=========== $SUB ==========="
    IN=$DATA/$SUB
    PHASEDIFF=${IN}/fmap/${SUB}_phasediff.nii.gz
    MAG1=${IN}/fmap/${SUB}_magnitude1.nii.gz
    MAG2=${IN}/fmap/${SUB}_magnitude2.nii.gz

    st_prepare_fieldmap $PHASEDIFF \
        --mag "$MAG1" \
        --output "$DATA/$SUB/fmap/fmap.nii.gz" \
        --threshold 0.008 \
        --gaussian-filter True \
        --sigma 1 

done
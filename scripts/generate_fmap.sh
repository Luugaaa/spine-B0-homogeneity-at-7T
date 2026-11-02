DATA=./data/ds007067
SUBJECTS="sub-093 sub-094 sub-095 sub-096 sub-098 sub-099 sub-100 sub-101 sub-102 sub-103 sub-104 sub-105 sub-106 sub-107"

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
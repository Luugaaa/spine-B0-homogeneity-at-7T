DATA=./data/ds007067
source "$(dirname "$0")/subjects.sh" "$@"

for SUB in $SUBJECTS; do
    echo "=========== $SUB ==========="
    IN=$DATA/$SUB
    PHASEDIFF=${IN}/fmap/${SUB}_phasediff.nii.gz
    MAG1=${IN}/fmap/${SUB}_magnitude1.nii.gz
    sct_deepseg spinalcord -i $MAG1 -o $IN/fmap/Mask.nii.gz
    sct_maths -i $IN/fmap/Mask.nii.gz -dilate 2 -shape ball -o $IN/fmap/Mask.nii.gz

done
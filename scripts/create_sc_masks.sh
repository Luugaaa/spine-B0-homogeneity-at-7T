DATA=./data/ds007067
SUBJECTS="sub-093 sub-094 sub-095 sub-096 sub-098 sub-099 sub-100 sub-101 sub-102 sub-103 sub-104 sub-105 sub-106 sub-107"

for SUB in $SUBJECTS; do
    echo "=========== $SUB ==========="
    IN=$DATA/$SUB
    PHASEDIFF=${IN}/fmap/${SUB}_phasediff.nii.gz
    MAG1=${IN}/fmap/${SUB}_magnitude1.nii.gz
    #sct_deepseg spinalcord -i $MAG1 -o $IN/fmap/Mask.nii.gz
    sct_maths -i $IN/fmap/Mask.nii.gz -dilate 2 -shape ball -o $IN/fmap/Mask.nii.gz

done
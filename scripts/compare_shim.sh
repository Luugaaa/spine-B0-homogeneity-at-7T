DATA=./data/ds007067
SUBJECTS="sub-093 sub-094 sub-095 sub-096 sub-098 sub-099 sub-100 sub-101 sub-102 sub-103 sub-104 sub-105 sub-106 sub-107"

for SUB in $SUBJECTS; do
    echo "=========== $SUB ==========="
    IN=$DATA/$SUB
    FMAP=${IN}/fmap/fmap.nii.gz
    MASK=${IN}/fmap/Mask.nii.gz
    echo "--- 1. Volume shim ---"
    st_b0shim dynamic \
        --fmap "$FMAP" \
        --target "$FMAP" \
        --mask "$MASK" \
        --output "${IN}/shim/volume" \
        --slices 'volume' \
        --optimizer-method "lin_lsq" \
        --mask-dilation-kernel-size 3 \
        --scanner-coil-order '0,1'\

    echo "--- 2. Slice wise ---"
    st_b0shim dynamic \
        --fmap "$FMAP" \
        --target "$FMAP" \
        --mask "$MASK" \
        --output "${IN}/shim/slice_wise" \
        --slices 'auto' \
        --optimizer-method "lin_lsq" \
        --mask-dilation-kernel-size 3 \
        --scanner-coil-order '0,1'\

done
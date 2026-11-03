DATA=./data/ds007067
source "$(dirname "$0")/subjects.sh" "$@"

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
        --optimizer-method "pseudo_inverse" \
        --mask-dilation-kernel-size 3 \
        --scanner-coil-order '0,1'\

    echo "--- 2. Slice wise ---"
    st_b0shim dynamic \
        --fmap "$FMAP" \
        --target "$FMAP" \
        --mask "$MASK" \
        --output "${IN}/shim/slice_wise" \
        --slices 'auto' \
        --optimizer-method "pseudo_inverse" \
        --mask-dilation-kernel-size 3 \
        --scanner-coil-order '0,1'\

done
# Subject selection shared by the pipeline scripts, sourced with the script's arguments.
# Usage: bash scripts/<script>.sh [-n N | -s SUB [SUB ...]]
#   -n N     run on the first N subjects
#   -s SUB   run on the given subjects only (e.g. -s sub-093 sub-100, or -s 093 100)
# Without flag, all 14 subjects are used.

ALL_SUBJECTS="sub-093 sub-094 sub-095 sub-096 sub-098 sub-099 sub-100 sub-101 sub-102 sub-103 sub-104 sub-105 sub-106 sub-107"
SUBJECTS=$ALL_SUBJECTS

if [[ $# -gt 0 ]]; then
    case "$1" in
        -n)
            if [[ ! "${2:-}" =~ ^[1-9][0-9]*$ ]]; then
                echo "-n expects a positive integer" >&2
                exit 1
            fi
            SUBJECTS=$(echo $ALL_SUBJECTS | tr ' ' '\n' | head -n "$2" | tr '\n' ' ')
            ;;
        -s)
            shift
            if [[ $# -eq 0 ]]; then
                echo "-s expects at least one subject" >&2
                exit 1
            fi
            SUBJECTS=""
            for SUB in "$@"; do
                [[ $SUB == sub-* ]] || SUB="sub-$SUB"
                if [[ " $ALL_SUBJECTS " != *" $SUB "* ]]; then
                    echo "Unknown subject: $SUB (available: $ALL_SUBJECTS)" >&2
                    exit 1
                fi
                SUBJECTS="$SUBJECTS $SUB"
            done
            ;;
        *)
            echo "Usage: bash $0 [-n N | -s SUB [SUB ...]]" >&2
            exit 1
            ;;
    esac
fi

echo "Subjects:" $SUBJECTS

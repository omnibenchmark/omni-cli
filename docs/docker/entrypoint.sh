#!/bin/sh
ARGS=
if [ $OMNICLI_DIRTY -eq 1 ]; then
    ARGS="--no-commit"
    rm -rf work && cp -r orig work
fi
cd work && omni_cli workflow run $ARGS

#!/bin/bash
for f in ../pipeline_generator/workflows/horses-all-workflows/*; do
    python3.10 general_pipeline_translator.py --keep "$f" "${HOME}/Desktop/knime-workspace/horses-all-workflows/$(basename $f)"
done
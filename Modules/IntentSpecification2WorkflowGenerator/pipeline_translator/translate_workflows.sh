#!/bin/bash
for f in ../pipeline_generator/workflows/titanic-optimized-workflows/*; do
    python3.10 general_pipeline_translator.py --keep "$f" "${HOME}/Desktop/knime-workspace/titanic-optimized-workflows/$(basename $f)"
done
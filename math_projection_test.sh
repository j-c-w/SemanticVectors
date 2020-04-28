#!/bin/bash

echo "Starting test..."

. /etc/profile.d/modules.sh
# Get python
module load python/3.4.3

cd CodeModels/SemanticVectors/
# Then use it to execute the thing.
parallel -j 10 python3 math_projection_test.py --test {} ::: 100000 10000 100 10000001 10000272 1 3 1015

echo "Test done!"
